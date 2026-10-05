import shutil, subprocess, sys, os
from pathlib import Path
S = Path(sys.argv[1]); BASE = S / "mut"
ACT_OLD = ('states = [((result["runs"].get(r["id"]) or {}).get("criteria") or {}).get("deterministic activation", "NOT_EVALUATED")\n'
           '                  for r in expected.values() if r["profile_key_sha256"] == key and r["entry_stratum"] == "deterministic"]')
ACT_NEW = 'states = [r["criteria"]["deterministic activation"] if r else "NOT_EVALUATED" for r in deterministic]'
NEEDED = 'needed = (["bytes"] if "bytes" in open_questions and byte_available else []) + ["owner-floor"]'
MUTS = [
 ("R1 replacement ignores its own owner floor", NEEDED, 'needed = (["bytes"] if "bytes" in open_questions and byte_available else [])'),
 ("R2 replacement ignores open byte question", NEEDED, 'needed = ["owner-floor"]'),
 ("G1 no open-question guard", "        if answers not in open_questions:", "        if False:"),
 ("G2 hard-failed original not refused", "        if hard_failure(o):", "        if False:"),
 ("G3 replacement block never stands", "        standing_failure = blocks_rerun(r)", "        standing_failure = False"),
 ("G4 standing needs eligible original", "        standing_failure = blocks_rerun(r)", "        standing_failure = blocks_rerun(r) and original_eligible"),
 ("G5 unresolved dispositions do not block", "    return hard_failure(row) or not other_criteria_clear(", "    return hard_failure(row) or False and not other_criteria_clear("),
 ("G6 fail disposition not a hard failure", 'or any(d.get("result") == "fail" for d in dispositions))', ")"),
 ("G7 activation scored-only", ACT_OLD, ACT_NEW),
 ("G8 T7 standing dispositions not counted", 'if record.get("standing_failure") and rid not in scored_ids and rid in result["runs"]:', "if False:"),
 ("G9 not-applicable bars", 'd.get("result") in ("pass", "not-applicable") for d in dispositions', 'd.get("result") in ("pass",) for d in dispositions'),
 ("G10 attempts not counted", '        tally("replacements")', "        pass"),
]
for name, old, new in MUTS:
    dst = S / "mutwork"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(BASE, dst)
    f = dst / "qualification" / "ssdp70" / "eval" / "batch_assess70.py"
    text = f.read_text()
    if old not in text:
        print(name, "PATTERN-NOT-FOUND", flush=True)
        continue
    f.write_text(text.replace(old, new, 1))
    p = subprocess.run([sys.executable, "-m", "unittest", "test_batch_cli"], cwd=dst / "qualification" / "ssdp70" / "eval",
                       capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    failed = [l.split(" (")[0] for l in p.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    print(name, "KILLED" if p.returncode else "SURVIVED", failed[:2], flush=True)
