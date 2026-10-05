#!/usr/bin/env python3
"""Mechanical verifier for the independently reviewed frozen-source premise witness.

Hashes authenticate bindings, not semantic warrants. An opaque or unreviewed source stays
UNRESOLVED. No decoder list is used as proof of absence. Development construction witnesses
exercise this owner but cannot satisfy qualification admission.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

SCHEMA = 1
_SCAN_CACHE = {}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def inventory(root):
    root = Path(root)
    paths = [root] if root.is_file() else sorted(root.rglob("*"))
    result = {}
    for path in paths:
        rel = "." if path == root else path.relative_to(root).as_posix()
        if path.is_symlink():
            result[rel] = {"type": "symlink", "target": os.readlink(path)}
        elif path.is_file():
            result[rel] = {"type": "file", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    return result


def source_manifest(sources):
    return {name: inventory(path) if isinstance(path, Path) else
            {".": {"type": "value", "sha256": hashlib.sha256(path).hexdigest()}}
            for name, path in sorted(sources.items())}


def development_witness(package_manifest, sources, *, construction_record, mounts):
    """Fixture-custodian input for known test constructions; never a production acceptance."""
    return {"schema": SCHEMA, "purpose": "development", "package": package_manifest,
            "sources": sources, "mounts": mounts, "construction_record": construction_record,
            "nodes": {name: {"inputs": [], "warrant": construction_record} for name in sources},
            "envelope_warrant": construction_record}


def check(package, sources, mounts, witness=None, *, owner_name, line_floor=48,
          qualification=False, accepted_witness_sha256=None):
    """Verify complete bindings and structural predicates before package marks are installed."""
    package = Path(package)
    package_manifest = inventory(package)
    actual_sources = source_manifest(sources)
    failures, unresolved = [], []
    owners = [p for p in package.rglob(owner_name) if p.is_file()]
    if not owners:
        unresolved.append("owner source is absent")
    # Segment owner lines exactly as the accounting does (strict UTF-8, str.splitlines); a copy the accounting
    # cannot decode would contribute no owner lines there, so it cannot be verified here either.
    lines = set()
    for path in owners:
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            unresolved.append(f"owner copy is not valid UTF-8: {path.relative_to(package)}")
            continue
        lines.update(line.encode() for line in text.splitlines() if len(line.encode()) >= line_floor)
    pattern = re.compile(b"|".join(re.escape(line) for line in sorted(lines))) if lines else None
    for path in package.rglob("*"):
        if path.is_symlink():
            failures.append(f"package symlink: {path.relative_to(package)}")
        elif path.is_file() and path.stat().st_nlink != 1:
            failures.append(f"package hard link: {path.relative_to(package)}")
        elif path.is_file() and path.name != owner_name and pattern and pattern.search(path.read_bytes()):
            failures.append(f"whole owner line in non-owner package file: {path.relative_to(package)}")
    package_binds = [m for m in mounts if m.get("source") == "package"]
    if len(package_binds) != 1 or package_binds[0].get("read_only") is not True:
        failures.append("package must have exactly one read-only bind")
    mounted_sources = {m.get("source") for m in mounts}
    if mounted_sources - set(sources) - {"package"}:
        unresolved.append("mount source outside frozen input envelope")
    for name, root in sources.items():
        manifest = actual_sources[name]
        key = (digest(package_manifest), digest(manifest), digest(mounts), line_floor, owner_name)
        if key not in _SCAN_CACHE:
            hits = []
            for rel, row in manifest.items():
                if row["type"] == "symlink":
                    target = row["target"]
                    # Absolute targets must resolve inside the enumerated sandbox mount envelope.
                    destinations = [m.get("destination", "") for m in mounts]
                    if target.startswith("/"):
                        if not any(d and (target == d or target.startswith(d.rstrip("/")+"/")) for d in destinations):
                            hits.append(f"escaping symlink: {name}/{rel}")
                    elif isinstance(root, Path):
                        resolved = ((root if root.is_dir() else root.parent) / rel).parent.joinpath(target).resolve()
                        if not any(isinstance(p, Path) and (resolved == p.resolve() or p.resolve() in resolved.parents)
                                   for p in sources.values()):
                            hits.append(f"escaping symlink: {name}/{rel}")
                    continue
                data = root if isinstance(root, bytes) else (root if rel == "." else root/rel).read_bytes()
                if pattern and pattern.search(data):
                    hits.append(f"whole owner line in other source: {name}/{rel}")
                if row.get("sha256") in {r["sha256"] for r in package_manifest.values() if r["type"] == "file"}:
                    hits.append(f"byte-identical package file in other source: {name}/{rel}")
            _SCAN_CACHE[key] = hits
        failures.extend(_SCAN_CACHE[key])
    if not isinstance(witness, dict):
        unresolved.append("frozen-source provenance witness missing")
    else:
        if witness.get("schema") != SCHEMA or witness.get("package") != package_manifest or witness.get("sources") != actual_sources or witness.get("mounts") != mounts:
            unresolved.append("witness package/source identities or coverage differ")
        nodes = witness.get("nodes")
        if not isinstance(nodes, dict) or set(nodes) != set(actual_sources):
            unresolved.append("construction nodes do not cover the complete source envelope")
            nodes = {}
        def warranted(value):
            return (isinstance(value, dict) and isinstance(value.get("record"), str) and bool(value["record"].strip())
                    and isinstance(value.get("evidence"), str) and bool(value["evidence"].strip()))
        if not warranted(witness.get("envelope_warrant")):
            unresolved.append("joint source envelope exclusion warrant missing")
        visited, active = set(), set()
        def visit(name):
            if name in active:
                unresolved.append("construction graph is cyclic")
                return
            if name in visited:
                return
            node = nodes.get(name)
            if not isinstance(node, dict) or not isinstance(node.get("inputs"), list) or not warranted(node.get("warrant")):
                unresolved.append(f"source/construction exclusion warrant missing: {name}")
                return
            active.add(name)
            for parent in node["inputs"]:
                if not isinstance(parent, str) or parent not in nodes:
                    unresolved.append(f"unclosed construction input: {name}")
                else:
                    visit(parent)
            active.remove(name); visited.add(name)
        for name in nodes:
            visit(name)
        if qualification:
            if witness.get("purpose") != "qualification" or digest(witness) != accepted_witness_sha256:
                unresolved.append("independent pre-run acceptance does not bind this witness")
    return {"schema": SCHEMA, "package": package_manifest, "sources": actual_sources,
            "mounts": mounts, "witness": witness, "witness_sha256": digest(witness),
            "qualification": qualification, "line_floor": line_floor,
            "failures": sorted(set(failures)), "unresolved": sorted(set(unresolved)),
            "state": "FAIL" if failures else "UNRESOLVED" if unresolved else "PASS"}


def verify_report(report, *, qualification=False, accepted_witness_sha256=None):
    """Evaluator binding check; does not convert a warrant label into independent acceptance."""
    if not isinstance(report, dict) or report.get("schema") != SCHEMA or report.get("state") != "PASS":
        return ["package-access premise was not established"]
    if report.get("failures") != [] or report.get("unresolved") != []:
        return ["package-access premise report contradicts its PASS state"]
    witness = report.get("witness")
    if not isinstance(witness, dict) or witness.get("package") != report.get("package") or witness.get("sources") != report.get("sources") or witness.get("mounts") != report.get("mounts"):
        return ["package-access premise witness/report binding differs"]
    if report.get("witness_sha256") != digest(witness):
        return ["package-access premise witness digest differs"]
    if qualification and (witness.get("purpose") != "qualification" or digest(witness) != accepted_witness_sha256):
        return ["development/unaccepted premise witness cannot qualify a profile"]
    return []


def main(argv=None):
    import argparse
    import base64
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True,
                        help="JSON map from source id to {path:...} or {value_b64:...}")
    parser.add_argument("--mounts", type=Path, required=True)
    parser.add_argument("--witness", type=Path)
    parser.add_argument("--qualification", action="store_true")
    parser.add_argument("--accepted-witness-sha256")
    parser.add_argument("--owner-name", default="scientific-inspectability-and-initiative.md")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    rows = json.loads(args.sources.read_text())
    sources = {name: Path(row["path"]) if set(row)=={"path"} else
               base64.b64decode(row["value_b64"], validate=True) for name,row in rows.items()}
    report = check(args.package,sources,json.loads(args.mounts.read_text()),
        json.loads(args.witness.read_text()) if args.witness else None, owner_name=args.owner_name,
        qualification=args.qualification,accepted_witness_sha256=args.accepted_witness_sha256)
    with args.output.open("x") as stream:
        json.dump(report,stream,sort_keys=True,indent=2);stream.write("\n")
    return 0 if report["state"]=="PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
