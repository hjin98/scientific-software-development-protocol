from pathlib import Path


def replace(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"missing expected text in {path}: {old!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


replace(
    "PORTABILITY.md",
    "Live claims require fresh-session evidence for the named harness/model/install mode; unavailable telemetry remains unavailable rather than inferred.",
    "Live claims require fresh-session evidence for the named harness/model/install mode; unavailable telemetry remains unavailable rather than inferred. Do not infer another environment from one run.",
)
replace(
    "PORTABILITY.md",
    "| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current / frozen when 6.3 profile is added |",
    "| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |",
)
replace(
    "PORTABILITY.md",
    "Historical profile/prompt bytes remain immutable.",
    "During Protocol 6.3 candidate qualification, the 6.2 resource is an immutable predecessor snapshot while Protocol 6.2 remains accepted-current operational authority until cutover. Historical profile/prompt bytes remain immutable.",
)
replace(
    "source/shared/references/development-workflow-prompts.md",
    "If neither compatible source can be read, report truthful non-closure rather than executing from memory or a similarly named incompatible skill.",
    "If neither compatible source can be read, report truthful non-closure rather than executing from memory or a similarly named incompatible skill. Repository-default bytes are never a substitute for a version-mapped immutable source.",
)
replace(
    "source/shared/references/abstraction-and-concretization.md",
    "Workplans, tests, gates, metrics, reviews, reports, implementation machinery, historical frequency, and project memory are constraints, evidence, coordination, or concretizations—not objectives or self-authorizing rules.",
    "Workplans, tests, gates, metrics, reviews, reports, and implementation machinery are constraints, evidence, or concretizations—not objectives. Historical frequency and project memory are likewise decision inputs or coordination state, not self-authorizing rules.",
)
replace(
    "source/shared/references/convergence-and-cycle-economy.md",
    "**No recurrence count, review count, cycle budget, memory temperature, or convergence target can force acceptance**; escalation changes the engineering method, **not the pass threshold**.",
    "**No recurrence count, review count, cycle budget, or convergence target can force acceptance**; memory temperature cannot force acceptance either; escalation changes the engineering method, **not the pass threshold**.",
)
replace(
    "source/shared/references/protocol-versioning-and-compatibility.md",
    "| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current while 6.3 candidate is being qualified |",
    "| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |",
)
replace(
    "source/shared/references/protocol-versioning-and-compatibility.md",
    "Schema v2 remains unless an actual machine profile contract changes.",
    "During 6.3 qualification, the 6.2 profile bytes are frozen as the immutable predecessor resource while 6.2 remains accepted-current until 6.3 cutover. Schema v2 remains unless an actual machine profile contract changes.",
)
replace(
    "source/SEMANTIC_DEPENDENCIES.md",
    "ssdp-protocol-6.2 CONSTRAINED_BY -> accepted Protocol 6.2 semantics/recovery",
    "ssdp-protocol-6.2 CONSTRAINED_BY -> accepted-current Protocol 6.2 semantics",
)

for path in (
    "tests/test_protocol_516_long_horizon_quality.py",
    "tests/test_protocol_61_evidence_evolution.py",
    "tests/test_protocol_62_representation.py",
    "tests/test_protocol_contracts.py",
):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    candidates = (
        ('self.assertEqual("6.2.0", read("source/PROTOCOL_VERSION").strip())', 'read("source/PROTOCOL_VERSION").strip()'),
        ('self.assertEqual(self.read("source/PROTOCOL_VERSION").strip(), "6.2.0")', 'self.read("source/PROTOCOL_VERSION").strip()'),
        ('self.assertEqual((SOURCE / "PROTOCOL_VERSION").read_text().strip(), "6.2.0")', '(SOURCE / "PROTOCOL_VERSION").read_text().strip()'),
    )
    changed = False
    for old, expr in candidates:
        if old in text:
            new = (
                f'version = tuple(int(part) for part in {expr}.split("."))\n'
                '        self.assertEqual(version[0], 6)\n'
                '        self.assertGreaterEqual(version, (6, 2, 0))'
            )
            text = text.replace(old, new, 1)
            changed = True
            break
    if not changed:
        raise SystemExit(f"no 6.2 current-version assertion found in {path}")
    p.write_text(text, encoding="utf-8")

p = Path("tests/test_protocol_62_representation.py")
text = p.read_text(encoding="utf-8")
old = '''for name in sorted(path.name for path in REFERENCES.glob("*.md")):
            self.assertIn(f"`{name}`", text, name)
        for name in sorted(path.name for path in TEMPLATES.glob("*.md")):
            self.assertIn(f"`{name}`", text, name)'''
new = '''baseline_references = {path.name for path in REFERENCES.glob("*.md")} - {"project-engineering-memory.md"}
        baseline_templates = {path.name for path in TEMPLATES.glob("*.md")} - {"project_engineering_memory_template.md"}
        for name in sorted(baseline_references):
            self.assertIn(f"`{name}`", text, name)
        for name in sorted(baseline_templates):
            self.assertIn(f"`{name}`", text, name)'''
if old not in text:
    raise SystemExit("missing Protocol 6.2 preservation census enumeration")
text = text.replace(old, new, 1)
old = '''self.assertIn(f"public_ref = {bootstrap}", prompt)
            self.assertNotIn("automatic current-6.2 public fallback is unavailable", prompt)'''
new = '''current_version = (SOURCE / "PROTOCOL_VERSION").read_text().strip()
            if current_version == "6.2.0":
                self.assertIn(f"public_ref = {bootstrap}", prompt)
                self.assertNotIn("automatic current-6.2 public fallback is unavailable", prompt)
            else:
                self.assertIn(f"accepted_6_2_public_ref = {bootstrap}", prompt)
                self.assertIn("current_public_ref = unavailable_pending_6.3_bootstrap_qualification", prompt)'''
if old not in text:
    raise SystemExit("missing Protocol 6.2 fallback assertion block")
p.write_text(text.replace(old, new, 1), encoding="utf-8")

p = Path("tests/test_protocol_61_evidence_evolution.py")
text = p.read_text(encoding="utf-8")
old = '''self.assertIn(f"PUBLIC_REF = {bootstrap}", prompts)
            self.assertIn("current 6.2 may fall back", lower)
            self.assertNotIn("automatic current-6.2 public fallback is unavailable", lower)'''
new = '''current_version = self.read("source/PROTOCOL_VERSION").strip()
            if current_version == "6.2.0":
                self.assertIn(f"PUBLIC_REF = {bootstrap}", prompts)
                self.assertIn("current 6.2 may fall back", lower)
                self.assertNotIn("automatic current-6.2 public fallback is unavailable", lower)
            else:
                self.assertIn(f"ACCEPTED_6_2_PUBLIC_REF = {bootstrap}", prompts)
                self.assertIn("CURRENT_PUBLIC_REF = UNAVAILABLE_PENDING_6.3_BOOTSTRAP_QUALIFICATION", prompts)
                self.assertIn("version-bound 6.2 work continues to use exactly", lower)'''
if old not in text:
    raise SystemExit("missing inherited 6.2 prompt fallback block")
p.write_text(text.replace(old, new, 1), encoding="utf-8")

p = Path("tests/test_protocol_516_orchestration.py")
text = p.read_text(encoding="utf-8")
old = '''published = re.search(r"public_ref = ([0-9a-f]{40})", self.lower)
        if published is None:
            self.assertIn("bootstrap self-reference rule", self.lower)
            self.assertIn("automatic current-6.2 public fallback is unavailable", self.lower)
            self.assertNotIn("current 6.2 may fall back", self.lower)
        else:
            self.assertNotEqual(published.group(1), "1181c2031710c5d343194d87d08543290fded0ab")
            self.assertNotIn("automatic current-6.2 public fallback is unavailable", self.lower)'''
new = '''current_version = (ROOT / "source/PROTOCOL_VERSION").read_text(encoding="utf-8").strip()
        if current_version == "6.2.0":
            published = re.search(r"public_ref = ([0-9a-f]{40})", self.lower)
            if published is None:
                self.assertIn("bootstrap self-reference rule", self.lower)
                self.assertIn("automatic current-6.2 public fallback is unavailable", self.lower)
                self.assertNotIn("current 6.2 may fall back", self.lower)
            else:
                self.assertNotEqual(published.group(1), "1181c2031710c5d343194d87d08543290fded0ab")
                self.assertNotIn("automatic current-6.2 public fallback is unavailable", self.lower)
        else:
            self.assertIn("current_protocol = 6.3.0", self.lower)
            self.assertIn("current_public_ref = unavailable_pending_6.3_bootstrap_qualification", self.lower)
            self.assertIn("accepted_6_2_public_ref = 5a062ebc472755607b9dc66d33a5ebbc4b7429aa", self.lower)
            self.assertIn("self-reference-safe source snapshot", self.lower)'''
if old not in text:
    raise SystemExit("missing orchestration fallback branch")
p.write_text(text.replace(old, new, 1), encoding="utf-8")
