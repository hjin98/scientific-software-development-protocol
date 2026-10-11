#!/usr/bin/env python3
"""Read-only coherence scan of the SSDP skills text (analyst tool; changes nothing).

  skills_coherence_scan.py REPO [--rev REV] [--base REV] --out OUT.json

Scans the markdown under `source/` at REV (default the working tree) and, when --base is given, reports per-file growth against BASE.
Metrics per file: bytes, sentence-length distribution, heavy sentences (long, conditional-dense, semicolon-chained), conditional and
parenthesis density, near-duplicate sentences across files. These are indicators of cognitive load for a reader, not verdicts: the
report ranks hotspots for human reading. Code blocks, tables and link targets are excluded from the sentence statistics.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

COND = re.compile(r"\b(if|unless|only if|except|otherwise|when|whenever|whether|provided|else|until|absent|without|never|no|not)\b", re.I)
SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\*`\[(])")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


def files_at(repo: Path, rev: str | None) -> dict[str, str]:
    if rev is None:
        return {str(p.relative_to(repo)): p.read_text(errors="replace") for p in sorted((repo / "source").rglob("*.md"))}
    names = [n for n in git(repo, "ls-tree", "-r", "--name-only", rev, "source").splitlines() if n.endswith(".md")]
    return {n: git(repo, "show", f"{rev}:{n}") for n in names}


def clean(text: str) -> list[str]:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^---\n.*?\n---\n", " ", text, flags=re.S)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    units = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("|") or s.startswith("#") or re.fullmatch(r"[-=*_ ]+", s):
            continue
        s = re.sub(r"^([-*+]|\d+[.)])\s+", "", s)
        units.extend(u.strip() for u in SPLIT.split(s) if u.strip())
    return units


def paragraphs(text: str) -> list[str]:
    """The unit a reader meets: one markdown line/bullet (before sentence splitting), without code, tables, headings or link targets."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^---\n.*?\n---\n", " ", text, flags=re.S)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith(("|", "#"))]


def depth(s: str) -> int:
    d = m = 0
    for ch in s:
        if ch == "(":
            d += 1
            m = max(m, d)
        elif ch == ")":
            d = max(0, d - 1)
    return m


def sentence_stats(s: str) -> dict:
    w = len(s.split())
    return {"w": w, "cond": len(COND.findall(s)), "semi": s.count(";"), "paren": depth(s), "commas": s.count(",")}


def heavy(st: dict) -> bool:
    return st["w"] >= 80 or (st["w"] >= 50 and (st["cond"] >= 5 or st["semi"] >= 3 or st["paren"] >= 2))


def norm(s: str) -> list[str]:
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def scan(files: dict[str, str]) -> dict:
    per, allsent = {}, []
    for name, text in files.items():
        units = clean(text)
        stats = [sentence_stats(u) for u in units]
        lw = sorted(len(l.split()) for l in paragraphs(text))
        ws = sorted(s["w"] for s in stats)
        words = sum(ws)
        n = len(ws)
        per[name] = {"bytes": len(text.encode()), "sentences": n, "words": words,
                     "median_w": ws[n // 2] if n else 0, "p95_w": ws[int(n * 0.95)] if n else 0, "max_w": ws[-1] if n else 0,
                     "over60": sum(1 for w in ws if w > 60), "over100": sum(1 for w in ws if w > 100),
                     "heavy": sum(1 for s in stats if heavy(s)),
                     "lines_over120": sum(1 for w in lw if w > 120), "lines_over200": sum(1 for w in lw if w > 200), "max_line_w": lw[-1] if lw else 0,
                     "cond_per_100w": round(100 * sum(s["cond"] for s in stats) / words, 1) if words else 0,
                     "semi_per_100w": round(100 * sum(s["semi"] for s in stats) / words, 2) if words else 0}
        for u, s in zip(units, stats):
            allsent.append((name, u, s))
    # near-duplicate sentences (5-word shingles, inverted index)
    shingles: dict[tuple, list[int]] = collections.defaultdict(list)
    sets = []
    for i, (_, u, s) in enumerate(allsent):
        t = norm(u)
        sh = {tuple(t[j:j + 5]) for j in range(max(0, len(t) - 4))} if len(t) >= 12 else set()
        sets.append(sh)
        for g in sh:
            shingles[g].append(i)
    pairs = collections.Counter()
    for ids in shingles.values():
        if 1 < len(ids) <= 12:
            for a in range(len(ids)):
                for b in range(a + 1, len(ids)):
                    pairs[(ids[a], ids[b])] += 1
    dups = []
    for (a, b), c in pairs.items():
        if allsent[a][0] == allsent[b][0] and allsent[a][1] == allsent[b][1]:
            continue
        jac = c / (len(sets[a]) + len(sets[b]) - c)
        if jac >= 0.55:
            dups.append({"jaccard": round(jac, 2), "a": [allsent[a][0], allsent[a][1][:200]], "b": [allsent[b][0], allsent[b][1][:200]]})
    dups.sort(key=lambda d: -d["jaccard"])
    plist = sorted(((len(l.split()), n, l) for n, t in files.items() for l in paragraphs(t)), reverse=True)[:40]
    top = sorted(allsent, key=lambda x: -(x[2]["w"] + 6 * x[2]["cond"] + 4 * x[2]["semi"] + 8 * x[2]["paren"]))[:60]
    return {"files": per,
            "totals": {"files": len(per), "bytes": sum(p["bytes"] for p in per.values()), "words": sum(p["words"] for p in per.values()),
                       "sentences": sum(p["sentences"] for p in per.values()), "over100": sum(p["over100"] for p in per.values()), "lines_over120": sum(p["lines_over120"] for p in per.values()),
                       "lines_over200": sum(p["lines_over200"] for p in per.values()),
                       "heavy": sum(p["heavy"] for p in per.values())},
            "longest_paragraphs": [{"file": n, "words": w, "text": l[:300]} for w, n, l in plist], "near_duplicates": dups[:80], "near_duplicate_count": len(dups),
            "heaviest_sentences": [{"file": f, "words": s["w"], "cond": s["cond"], "semi": s["semi"], "paren": s["paren"], "text": u[:420]} for f, u, s in top]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", type=Path)
    ap.add_argument("--rev")
    ap.add_argument("--base")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    cur = scan(files_at(a.repo, a.rev))
    out = {"rev": a.rev or "working-tree", "current": cur}
    if a.base:
        base = scan(files_at(a.repo, a.base))
        out["base"] = {"rev": a.base, "totals": base["totals"]}
        growth = {}
        for name, p in cur["files"].items():
            b = base["files"].get(name)
            growth[name] = {"bytes": p["bytes"], "base_bytes": b["bytes"] if b else 0, "delta": p["bytes"] - (b["bytes"] if b else 0),
                            "new_file": b is None}
        out["growth"] = growth
    a.out.write_text(json.dumps(out, indent=1) + "\n")
    t = cur["totals"]
    print(json.dumps({"files": t["files"], "bytes": t["bytes"], "sentences": t["sentences"], "over100_words": t["over100"], "heavy": t["heavy"], "lines_over120": t["lines_over120"], "lines_over200": t["lines_over200"],
                      "near_duplicate_pairs": cur["near_duplicate_count"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
