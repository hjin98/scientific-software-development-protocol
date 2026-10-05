import shutil, subprocess, sys, os
from pathlib import Path
S = Path(sys.argv[1]); BASE = S/"mut"
MUTS = [
 ("W1 upper edge uses position not position-1", "package_ledger.py", "hi = position(later[0]) - 1 if later", "hi = position(later[0]) if later"),
 ("W2 unpositioned later request treated as trace start", "package_ledger.py", "hi = position(later[0]) - 1 if later and position(later[0]) is not None else end", "hi = (position(later[0]) or start) - 1 if later else end"),
 ("W3 empty window not widened", "package_ledger.py", "    if hi < lo:\n        lo, hi = start, end", "    if False:\n        lo, hi = start, end"),
 ("W4 no earlier request widens the end (old M4)", "package_ledger.py", "    if hi < lo:\n        lo, hi = start, end", "    if hi < lo or not earlier:\n        lo, hi = start, end"),
 ("W5 unpositioned earlier request not trace start", "package_ledger.py", "lo = position(earlier[-1]) if earlier and position(earlier[-1]) is not None else start", "lo = (position(earlier[-1]) or 10**9) if earlier else start"),
 ("W6 adapter text-only turn keeps numeric position", "adapters/omp.py", "positions.append(min(seqs) if seqs and expected else None)", "positions.append(min(seqs) if seqs and expected else 1)"),
 ("W7 adapter unverified pairing keeps position", "adapters/omp.py", '"position": positions[k] if verified else None,', '"position": positions[k],'),
 ("R1 replacement ignores open owner question", "batch_assess70.py", 'needed = [q for q in open_questions if q == "owner-floor" or byte_available] or', 'needed = [q for q in open_questions if q == "bytes" and byte_available] or'),
 ("R2 replacement ignores open byte question", "batch_assess70.py", 'needed = [q for q in open_questions if q == "owner-floor" or byte_available] or', 'needed = [q for q in open_questions if q == "owner-floor"] or'),
 ("R3 rerun after scored replacement allowed", "batch_assess70.py", 'if any(v["original"]==original and v["scored"] for v in report["records"]):', 'if False:'),
]
for name, fname, old, new in MUTS:
    dst = S/"mutwork"
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(BASE, dst)
    f = dst/"qualification"/"ssdp70"/"eval"/fname
    text = f.read_text()
    if old not in text:
        print(name, "PATTERN-NOT-FOUND", flush=True); continue
    f.write_text(text.replace(old, new, 1))
    p = subprocess.run([sys.executable, "-m", "unittest", "test_package_ledger", "test_batch_cli", "test_package_premise"], cwd=dst/"qualification"/"ssdp70"/"eval", capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    failed = [l.split(" (")[0] for l in p.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    print(name, "KILLED" if p.returncode else "SURVIVED", failed[:3], flush=True)
