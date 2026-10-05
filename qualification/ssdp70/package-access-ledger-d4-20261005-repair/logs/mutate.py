import shutil, subprocess, sys, os, json
from pathlib import Path
S = Path(sys.argv[1]); BASE = S/"mut"/"qualification"/"ssdp70"/"eval"
MUTS = [
 ("M1 single long line positive", "package_ledger.py", "(positive if len(matched) >= 2 and row", "(positive if len(matched) >= 1 and row"),
 ("M2 error-status excluded from owner supply", "package_ledger.py", "for seq, text, event in _result_events(events, errors=True):\n        matched", "for seq, text, event in _result_events(events, errors=False):\n        matched"),
 ("M3 provably-post-R2 off by one (start<boundary)", "core70.py", 'window"]["start"] <= boundary', 'window"]["start"] < boundary'),
 ("M4 no-earlier-request not conservative", "package_ledger.py", "if hi < lo or not earlier:", "if hi < lo:"),
 ("M5 taint not persistent", "package_ledger.py", "                tainted = True\n                reasons.append(f\"clock divergence", "                tainted = False\n                reasons.append(f\"clock divergence"),
 ("M6 owner_floor_exact ignores timing", "package_ledger.py", "and not (owner_rows and timing_reasons)", ""),
 ("M7 mutation flags tolerated", "package_ledger.py", "bad = flags - READ_FLAGS - {\"overflow\"}", "bad = set()"),
 ("M8 path-linkage always true", "package_ledger.py", "elif _names_path(event, rel, mount):", "elif True:"),
 ("M9 whole-file-in-window ignores window", "package_ledger.py", 'any(\n                    r["window"]["start"] <= sequence <= r["window"]["end"] for r in rows)', 'True'),
 ("M10 pre uses upper edge", "package_ledger.py", "pre = cut_ns is None or lower is None or lower < cut_ns", "pre = cut_ns is None or upper is None or upper < cut_ns"),
 ("M11 positive FAIL requires exactness", "core70.py", "if any(r[\"sequence\"] < boundary for r in accounting.get(\"owner_read_observed\", [])):", "if accounting.get(\"owner_floor_exact\") and any(r[\"sequence\"] < boundary for r in accounting.get(\"owner_read_observed\", [])):"),
 ("M12 hi uses position not position-1", "package_ledger.py", 'hi = later[0].get("position", start) - 1', 'hi = later[0].get("position", start)'),
 ("M13 request monotonicity unchecked", "package_ledger.py", "or (previous is not None and (rt < previous[0] or mono < previous[1]))", ""),
 ("M14 owner line floor strict", "package_ledger.py", 'if len(line.encode()) >= parameters["owner_line_floor"]}', 'if len(line.encode()) > parameters["owner_line_floor"]}'),
 ("M16 owner copy by substring", "package_ledger.py", 'rel.rsplit("/", 1)[-1] == owner_name', 'owner_name in rel'),
 ("M17 owner_floor_exact ignores global reasons", "package_ledger.py", "result[\"owner_floor_exact\"] = not global_reasons and owner_name", "result[\"owner_floor_exact\"] = owner_name"),
 ("M18 owner lines counted per occurrence", "package_ledger.py", "matched = {line for line in lines if any(line in output for output in text.splitlines())}", "matched = [line for line in lines for output in text.splitlines() if line in output]"),
 ("M19 minor exposure ignored by floor", "core70.py", 'or accounting.get("owner_minor_exposure")\n', '\n'),
 ("M20 unknown candidate=0 (swap)", "batch_assess70.py", "value = float('inf') if opportunity['arm']==candidate else 0", "value = 0 if opportunity['arm']==candidate else float('inf')"),
 ("M21 positive FAIL needs adjudication removed->no", "core70.py", "if not r2_adjudicated:\n        return \"UNRESOLVED\"", "if False:\n        return \"UNRESOLVED\""),
 ("M22 replacement ignores FAIL bar", "batch_assess70.py", 'and o.get("owner_floor_state") != "FAIL"', ''),
 ("M23 cap off", "batch_assess70.py", "if count[case]>2:", "if count[case]>99:"),
 ("M24 error-status results seen", "package_ledger.py", 'payload.get("result_seen_by_model") is True', 'payload.get("result_seen_by_model") is not False'),
 ("M25 request stamp missing not loss", "package_ledger.py", "if cut_ns is not None and not requests:", "if False:"),
 ("M26 bracket lower uses after", "package_ledger.py", 'lower = previous["before_ns"] - tolerance', 'lower = previous["after_ns"] - tolerance'),
 ("M27 tolerance not applied to upper", "package_ledger.py", 'upper = beat["after_ns"] + tolerance', 'upper = beat["after_ns"]'),
 ("M28 premise verify_report ignores state", "package_premise.py", 'report.get("state") != "PASS"', 'False'),
 ("M29 premise qualification digest unchecked", "package_premise.py", ' or digest(witness) != accepted_witness_sha256):\n        return ["development', '):\n        return ["development'),
 ("M30 premise hardlink unchecked", "package_premise.py", "path.stat().st_nlink != 1", "False"),
 ("M31 premise unlisted mount tolerated", "package_premise.py", 'if mounted_sources - set(sources) - {"package"}:', 'if False:'),
 ("M32 premise owner-line collision unchecked in sources", "package_premise.py", "if pattern and pattern.search(data):", "if False:"),
("M33 watcher overflow detection removed", "package_ledger.py", '"overflow": "overflow" in self._flags_seen,', '"overflow": False,'),
 ("M34 watcher final heartbeat removed", "package_ledger.py", "            self._heartbeat()\n            os.write(self._stop_w", "            os.write(self._stop_w"),
 ("M35 check digest of accepted witness unchecked in check()", "package_premise.py", 'or digest(witness) != accepted_witness_sha256:\n                unresolved', ':\n                unresolved'),
 ("M36 aggregate ignores byte slots", "batch_assess70.py", '"_byte_slots": ledger_bookkeeping["byte_slots"]', '"_byte_slots": {}'),
 ("M37 aggregate ignores owner-slot override", "batch_assess70.py", 'if selected != slots.get(slot) and selected in result["runs"] and slot in owner_scored:', 'if False:'),
 ("M38 disparity bound ignored", "batch_assess70.py", 'if ledger_bookkeeping["byte_disparity_exceeded"]:', 'if False:'),
 ("M39 per-case cap counts only scored", "batch_assess70.py", "count[case] = count.get(case,0)+1", "count[case] = count.get(case,0)"),
 ("M40 observation_adjudicated ignores owner adjudication", "batch_assess70.py", 'and (row.get("owner_floor_adjudication") or {}).get("adjudicated") is True\n', '\n'),
 ("M41 unknown requires exact False only (None treated known)", "batch_assess70.py", "unknown = (part in ('fixed_cost','active_material') and route=='T7'", "unknown = (False and route=='T7'"),
 ("M42 owner_floor_state ignores owner_open_windows", "core70.py", 'or any(r["window"]["start"] <= boundary for r in accounting.get("owner_open_windows", []))):', '):'),
 ("M43 owner_floor_state ignores exact", "core70.py", 'if (accounting.get("owner_floor_exact") is not True or', 'if (False or'),
 ("M44 recompute doesnt compare", "core70.py", 'errors = [] if actual == derived[0] else ["package_access differs from deterministic recomputation"]', 'errors = []'),
 ("M45 supply requires status result only for owner (errors skipped via status)", "package_ledger.py", 'if event.get("status") not in (("result", "error") if errors else ("result",)) or payload.get("result_status") not in (("result", "error") if errors else ("result",)):', 'if event.get("status") not in ("result",) or payload.get("result_status") not in ("result",):'),
 ("M46 native owner read not positive", "package_ledger.py", 'positive.append({"sequence": int(event["sequence"]), "event_id": event.get("event_id"), "source": "native-read"})', 'pass'),
 ("M47 route (ii) mount-less prefix boundary", "package_ledger.py", 'prefix = re.escape(mount.rstrip("/") + "/") if mount else r"(?<![\w.\-])"', 'prefix = ""'),
]
only = sys.argv[2:] 
res = []
for name, fname, old, new in MUTS:
    if only and not any(name.startswith(o) for o in only): continue
    dst = S/"mutwork"
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(S/"mut", dst)
    f = dst/"qualification"/"ssdp70"/"eval"/fname
    text = f.read_text()
    if old not in text:
        res.append((name, "PATTERN-NOT-FOUND")); print(name, "PATTERN-NOT-FOUND", flush=True); continue
    f.write_text(text.replace(old, new, 1))
    p = subprocess.run([sys.executable, "-m", "unittest", "test_package_ledger", "test_batch_cli", "test_package_premise"], cwd=dst/"qualification"/"ssdp70"/"eval", capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE":"1"})
    tail = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""
    failed = [l for l in p.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    status = "KILLED" if p.returncode else "SURVIVED"
    res.append((name, status, failed[:4]))
    print(name, status, [x.split(" (")[0] for x in failed[:4]], flush=True)
