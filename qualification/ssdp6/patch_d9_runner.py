from pathlib import Path

p = Path("qualification/ssdp6/temporary_d9_repair.py")
s = p.read_text()
old_rm = '''run("git", "diff", "--check")
run("git", "rm", ".github/workflows/temporary-protocol63-d9-repair.yml", "qualification/ssdp6/temporary_d9_repair.py")
run("git", "add", "source/project_engineering_memory.py", "tests/test_protocol_63_independent_review_repairs.py")
'''
new_rm = '''run("git", "diff", "--check")
for temporary_path in (
    ".github/workflows/temporary-protocol63-d9-repair.yml",
    "qualification/ssdp6/temporary_d9_repair.py",
    "qualification/ssdp6/patch_d9_runner.py",
    "qualification/ssdp6/DIAGNOSTIC-PROTOCOL-6.3-D9-EXECUTION.txt",
):
    if (ROOT / temporary_path).exists():
        run("git", "rm", temporary_path)
run("git", "add", "source/project_engineering_memory.py", "tests/test_protocol_63_independent_review_repairs.py")
'''
if old_rm not in s:
    raise SystemExit("temporary removal anchor missing")
s = s.replace(old_rm, new_rm, 1)

old_measure = '''sensor = QDIR / "SSDP-6.3-STATIC-ACTIVATION-SENSORS.md"
sensor_text = sensor.read_text()
tail = sensor_text.split("## 6.3 active sets", 1)[1]
sections = re.split(r"(?m)^### ", tail)[1:]
checked = 0
for block in sections:
    heading = block.splitlines()[0]
    m_expected = re.search(r"- active bytes: ([0-9,]+);", block)
    m_paths = re.search(r"(?m)^- active: (.+)$", block)
    if not m_expected or not m_paths:
        continue
    paths = re.findall(r"`([^`]+)`", m_paths.group(1))
    actual = sum((ROOT / path).stat().st_size for path in paths)
    expected = int(m_expected.group(1).replace(",", ""))
    if actual != expected:
        raise SystemExit(f"{heading}: documented active bytes {expected}, exact-candidate bytes {actual}")
    checked += 1
if checked != 11:
    raise SystemExit(f"expected 11 static active-set traces, checked {checked}")
print(f"verified {checked} exact-candidate static active-set byte totals")
'''
new_measure = '''sensor = QDIR / "SSDP-6.3-STATIC-ACTIVATION-SENSORS.md"
sensor_text = sensor.read_text()
tail = sensor_text.split("## 6.3 active sets", 1)[1]
sections = re.split(r"(?m)^### ", tail)[1:]
measurements: dict[str, int] = {}
for block in sections:
    heading = block.splitlines()[0].strip()
    m_paths = re.search(r"(?m)^- active: (.+)$", block)
    if not m_paths:
        continue
    paths = re.findall(r"`([^`]+)`", m_paths.group(1))
    measurements[heading] = sum((ROOT / path).stat().st_size for path in paths)
if len(measurements) != 11:
    raise SystemExit(f"expected 11 static active-set traces, measured {len(measurements)}")
for heading, actual in measurements.items():
    print(f"measured {heading}: {actual} bytes")
'''
if old_measure not in s:
    raise SystemExit("static measurement anchor missing")
s = s.replace(old_measure, new_measure, 1)

old_publish = '''sensor_text = replace_once(sensor_text, "semantic_candidate: 026eecf6ce382c3445ed218aeca80dcf2fb9a426", f"semantic_candidate: {candidate}", "sensor candidate")
sensor_text = replace_once(sensor_text, "F3 owner-binding refresh: the active-set predicates/topology were rechecked against repaired semantic candidate `026eecf6ce382c3445ed218aeca80dcf2fb9a426` and remain unchanged. Every 6.3 byte total below was recomputed from the exact candidate files named by that fixed active set; no F2 candidate-side byte total is carried forward as current evidence.", f"F5/D9 candidate-binding refresh: the active-set predicates/topology were rechecked against repaired semantic candidate `{candidate}` and remain unchanged. Every 6.3 byte total below was mechanically remeasured from the exact candidate files named by that fixed active set; all eleven totals match the table. No F2/F3/F4 candidate-side identity is carried forward as current evidence.", "sensor refresh paragraph")
sensor.write_text(sensor_text)
'''
new_publish = '''sensor_text = replace_once(sensor_text, "semantic_candidate: 026eecf6ce382c3445ed218aeca80dcf2fb9a426", f"semantic_candidate: {candidate}", "sensor candidate")
sensor_text = replace_once(sensor_text, "F3 owner-binding refresh: the active-set predicates/topology were rechecked against repaired semantic candidate `026eecf6ce382c3445ed218aeca80dcf2fb9a426` and remain unchanged. Every 6.3 byte total below was recomputed from the exact candidate files named by that fixed active set; no F2 candidate-side byte total is carried forward as current evidence.", f"F5/D9 candidate-binding refresh: the active-set predicates/topology were rechecked against repaired semantic candidate `{candidate}` and remain unchanged. Every 6.3 byte total below was mechanically recomputed from the exact candidate files named by that fixed active set; the table and per-trace records below publish those exact measurements. No F2/F3/F4 candidate-side identity is carried forward as current evidence.", "sensor refresh paragraph")
lines = sensor_text.splitlines()
for i, line in enumerate(lines):
    if not line.startswith("| ") or line.startswith("| ---") or "Representative task" in line:
        continue
    cells = [cell.strip() for cell in line.strip("|").split("|")]
    if len(cells) != 6 or cells[0] not in measurements:
        continue
    baseline_bytes = int(cells[1].replace(",", ""))
    actual = measurements[cells[0]]
    cells[2] = f"{actual:,}"
    delta = actual - baseline_bytes
    cells[3] = f"{delta:+,}"
    lines[i] = "| " + " | ".join(cells) + " |"
sensor_text = "\\n".join(lines) + "\\n"
for heading, actual in measurements.items():
    pattern = rf"(?m)(^### {re.escape(heading)}\\n\\n- active bytes: )([0-9,]+)(;)"
    sensor_text, count = re.subn(pattern, lambda m, a=actual: m.group(1) + f"{a:,}" + m.group(3), sensor_text, count=1)
    if count != 1:
        raise SystemExit(f"failed to publish exact active bytes for {heading}")
sensor.write_text(sensor_text)
'''
if old_publish not in s:
    raise SystemExit("sensor publication anchor missing")
s = s.replace(old_publish, new_publish, 1)
p.write_text(s)
