#!/usr/bin/env python3
"""Temporary branch-local helper to finish deterministic Protocol 6.1 migration."""
from __future__ import annotations

import base64
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = os.environ.get("GITHUB_REPOSITORY", "hjin98/scientific-software-development-protocol")
TOKEN = os.environ["GITHUB_TOKEN"]


def fetch_blob(sha: str) -> bytes:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/git/blobs/{sha}",
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req) as response:  # noqa: S310 - fixed GitHub API host
        payload = json.load(response)
    return base64.b64decode(payload["content"])


def install_blob(path: str, sha: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(fetch_blob(sha))


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"expected migration anchor missing: {label}")
    return text.replace(old, new)


# Prepared current-authority source edits. These blobs were reviewed before this
# helper was introduced; this helper only materializes them into the branch.
PREPARED = {
    "source/shared/references/scientific-formulation.md": "8cc196115450887cf5ff736be7056ff2c9a715d0",
    "source/shared/references/numerical-algorithm-design.md": "79e6588e74ab4e80415eb1213a3c651e73d789a7",
    "source/shared/references/specification-and-implementation.md": "04353ed936cf3c76ec5b106b9e53a9f4d7ce65a8",
    "source/shared/templates/abstraction_realization_change_plan_template.md": "31440519fab151fdee75ad9da70f57fd05a8b121",
    "source/shared/templates/implementation_workplan_template.md": "b1db4fbc13b1caa646c59fe36e2bdec04d786869",
    "source/build_skills.py": "ea4c8dd5fbfa2ebd50a6e151d7f38555d2e6b92c",
    "source/shared/references/language-profiles.md": "732d226cbc71c8eebe96d0f175fbb3b49f11967d",
    "source/shared/references/long-horizon-code-health.md": "c27b57e3638bebf36b6cacb7638066accbb545e5",
    "source/shared/references/convergence-and-cycle-economy.md": "a20d6ca33b5e59cfde8e79d7763aa11a8ce6629d",
    "source/shared/references/scientific-software.md": "9b66e109b97279d8ec471aff0f13d563ad92291f",
    "source/shared/references/concurrency-and-orchestration.md": "c6b6bf9adc431c03e59fb301128e50b2d42c400f",
    "source/shared/references/repository-intake.md": "45eeafe550fa14ced67dec6747fbb77154bcefb5",
    "source/shared/references/python-engineering.md": "397e996037b0dea5ad92fe6d7a2002adfe849c3b",
    "source/shared/references/cpp-engineering.md": "bad15429b24c7a116c84768d016af304c6b9a029",
    "source/shared/references/development-workflow-prompts.md": "43685fff64fcbfcb67717fe97f6df441ae3719f5",
    "orchestrator/src/sdp_orchestrator/core/canonical.py": "90600b4f075b44f55de872c9172a392a9f8903ed",
}
for rel, sha in PREPARED.items():
    install_blob(rel, sha)

# D3 current authority uses the new concretization vocabulary. The compatibility
# filename remains unchanged; evidence-realization terminology is not present in
# this D3 reference, so these bounded replacements are unambiguous.
arch_path = ROOT / "source/shared/references/architecture-and-design.md"
arch = arch_path.read_text(encoding="utf-8")
for old, new in (
    ("realizes", "concretizes"),
    ("realization", "concretization"),
    ("Realization", "Concretization"),
    ("unrealizable", "impossible to concretize"),
):
    arch = arch.replace(old, new)
arch = arch.replace("[Abstraction, concretization, authority, and challenge](abstraction-and-concretization.md)", "[Abstraction, concretization, authority, and challenge](abstraction-and-realization.md)")
arch_path.write_text(arch, encoding="utf-8")

# Add independent Protocol 6.1 profile identity while preserving 5.16 and 6.0.
profile_path = ROOT / "orchestrator/src/sdp_orchestrator/core/profile.py"
p = profile_path.read_text(encoding="utf-8")
p = replace_required(
    p,
    "frozen compatibility definition while Protocol 6.0 uses an independent\nschema-v2 profile selected by declared protocol/profile identity.",
    "frozen compatibility definition while Protocol 6.0 and 6.1 use independent\nschema-v2 profiles selected by declared protocol/profile identity.",
    "profile docstring",
)
p = replace_required(p, "    SSDP6_PROFILE_ID,\n", "    SSDP6_PROFILE_ID,\n    SSDP61_PROFILE_ID,\n", "6.1 canonical import")
p = replace_required(
    p,
    'DEFAULT_PROFILE_ID = SSDP6_PROFILE_ID\nSSDP6_PROFILE_SCHEMA_VERSION = 2\nSSDP6_PROTOCOL_VERSION = "6.0.0"\nSSDP6_COMPATIBLE_PROTOCOL_VERSIONS: tuple[str, ...] = ("6.0.0", "6.0")\n',
    'SSDP6_PROFILE_SCHEMA_VERSION = 2\nSSDP6_PROTOCOL_VERSION = "6.0.0"\nSSDP6_COMPATIBLE_PROTOCOL_VERSIONS: tuple[str, ...] = ("6.0.0", "6.0")\n\nSSDP61_PROFILE_SCHEMA_VERSION = 2\nSSDP61_PROTOCOL_VERSION = "6.1.0"\nSSDP61_COMPATIBLE_PROTOCOL_VERSIONS: tuple[str, ...] = ("6.1.0", "6.1")\nDEFAULT_PROFILE_ID = SSDP61_PROFILE_ID\n',
    "current profile constants",
)
anchor = "\n\n@dataclass(frozen=True)\nclass ProfileDefinition:"
if "_SSDP61_TRANSITIONS" not in p:
    insert = '''\n\ndef _protocol61_term(text: str) -> str:\n    return text.replace("realization", "concretization").replace("realize", "concretize")\n\n\n_SSDP61_STAGE_TABLE: dict[str, StageRow] = dict(_SSDP6_STAGE_TABLE)\n_SSDP61_TRANSITIONS: tuple[TransitionRow, ...] = tuple(\n    (source, trigger, target, _protocol61_term(explanation))\n    for source, trigger, target, explanation in _SSDP6_TRANSITIONS\n)\n'''
    p = replace_required(p, anchor, insert + anchor, "6.1 profile tables")
p = replace_required(
    p,
    "    SSDP6_PROFILE_ID: ProfileDefinition(SSDP6_PROFILE_ID, 2, SSDP6_PROTOCOL_VERSION, SSDP6_COMPATIBLE_PROTOCOL_VERSIONS, _SSDP6_STAGE_TABLE, _SSDP6_TRANSITIONS),\n}",
    "    SSDP6_PROFILE_ID: ProfileDefinition(SSDP6_PROFILE_ID, SSDP6_PROFILE_SCHEMA_VERSION, SSDP6_PROTOCOL_VERSION, SSDP6_COMPATIBLE_PROTOCOL_VERSIONS, _SSDP6_STAGE_TABLE, _SSDP6_TRANSITIONS),\n    SSDP61_PROFILE_ID: ProfileDefinition(SSDP61_PROFILE_ID, SSDP61_PROFILE_SCHEMA_VERSION, SSDP61_PROTOCOL_VERSION, SSDP61_COMPATIBLE_PROTOCOL_VERSIONS, _SSDP61_STAGE_TABLE, _SSDP61_TRANSITIONS),\n}",
    "profile registry",
)
profile_path.write_text(p, encoding="utf-8")

# Protocol source resolution is generic; only its human-facing compatibility
# description needs to acknowledge all three independently versioned profiles.
ps_path = ROOT / "orchestrator/src/sdp_orchestrator/core/protocol_source.py"
ps = ps_path.read_text(encoding="utf-8")
ps = ps.replace("Protocol 5.16 and Protocol 6.0 are separate profile/source contracts.", "Protocol 5.16, Protocol 6.0, and Protocol 6.1 are separate profile/source contracts.")
ps_path.write_text(ps, encoding="utf-8")

# Snapshot generation now protects both historical compatibility profiles and
# generates only the current 6.1 snapshot.
snapshot = r'''#!/usr/bin/env python3
"""Generate/check current Protocol 6.1 snapshot and prove frozen profile parity."""
from __future__ import annotations
import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_SRC = REPO_ROOT / "orchestrator" / "src"
sys.path.insert(0, str(PACKAGE_SRC))
from sdp_orchestrator.core import profile as P  # noqa: E402
from sdp_orchestrator.core.canonical import parse_document  # noqa: E402
from sdp_orchestrator.core.protocol_source import CANONICAL_PROMPTS_RELPATH, CANONICAL_VERSION_RELPATH, PACKAGED_PROFILE, PACKAGED_PROMPTS  # noqa: E402

RESOURCE_ROOT = PACKAGE_SRC / "sdp_orchestrator" / "core" / "resources" / "protocol"
CURRENT_TARGET_DIR = RESOURCE_ROOT / P.DEFAULT_PROFILE_ID
FROZEN = {
    P.PROFILE_ID: {PACKAGED_PROMPTS: "3730b06393843e9c24406a324f981ab4481858da", PACKAGED_PROFILE: "b3d4257fcd18af7bdb1799b2db742659bb2403fc"},
    P.SSDP6_PROFILE_ID: {PACKAGED_PROMPTS: "d127b9eb8da165afd905d4c35cc8b7572b201d56", PACKAGED_PROFILE: "76c53539a985bc8408f8432932e91e5477696db9"},
}

def _git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324

def validate_frozen() -> list[str]:
    drift: list[str] = []
    for profile_id, expected in FROZEN.items():
        root = RESOURCE_ROOT / profile_id
        texts: dict[str, str] = {}
        for name, expected_sha in expected.items():
            path = root / name
            if not path.is_file():
                drift.append(f"{profile_id}:{name}:missing")
                continue
            data = path.read_bytes()
            if _git_blob_sha(data) != expected_sha:
                drift.append(f"{profile_id}:{name}:immutable-bytes-changed")
            try:
                texts[name] = data.decode("utf-8")
            except UnicodeDecodeError:
                drift.append(f"{profile_id}:{name}:not-utf8")
        if set(texts) == {PACKAGED_PROMPTS, PACKAGED_PROFILE}:
            document = parse_document(texts[PACKAGED_PROMPTS], profile_id=profile_id)
            derived = P.profile_to_json(P.build_profile(document, profile_id).descriptor)
            if derived != texts[PACKAGED_PROFILE]:
                drift.append(f"{profile_id}:profile-not-derived-from-prompts")
    return drift

def render_current() -> dict[str, str]:
    defn = P.definition(P.DEFAULT_PROFILE_ID)
    declared_version = (REPO_ROOT / CANONICAL_VERSION_RELPATH).read_text(encoding="utf-8").strip()
    if declared_version != defn.protocol_version:
        raise ValueError(f"canonical source Protocol version does not match current profile: {declared_version!r} != {defn.protocol_version!r}")
    prompts = (REPO_ROOT / CANONICAL_PROMPTS_RELPATH).read_text(encoding="utf-8")
    document = parse_document(prompts, profile_id=P.DEFAULT_PROFILE_ID)
    snapshot = P.build_profile(document, P.DEFAULT_PROFILE_ID)
    return {PACKAGED_PROMPTS: prompts, PACKAGED_PROFILE: P.profile_to_json(snapshot.descriptor)}

render = render_current

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift = validate_frozen()
    if drift:
        print("frozen Protocol profile drift: " + ", ".join(drift), file=sys.stderr)
        return 1
    try:
        expected = render_current()
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"snapshot generation failed: {exc}", file=sys.stderr)
        return 1
    if args.check:
        stale = [name for name, text in expected.items() if not (CURRENT_TARGET_DIR / name).is_file() or (CURRENT_TARGET_DIR / name).read_text(encoding="utf-8") != text]
        if stale:
            print(f"current packaged snapshot is stale: {', '.join(stale)}", file=sys.stderr)
            return 1
        print("current Protocol 6.1 snapshot matches canonical source; Protocol 5.16 and 6.0 snapshots are immutable and coherent")
        return 0
    CURRENT_TARGET_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in expected.items():
        (CURRENT_TARGET_DIR / name).write_text(text, encoding="utf-8")
    print(f"wrote {len(expected)} current snapshot files to {CURRENT_TARGET_DIR.relative_to(REPO_ROOT)}")
    print("validated frozen Protocol 5.16 and 6.0 snapshots without rewriting them")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
'''
(ROOT / "orchestrator/scripts/generate_protocol_snapshot.py").write_text(snapshot, encoding="utf-8")

# Update existing profile tests while preserving their inherited behavioral
# coverage, then add explicit frozen-6.0 coverage.
test_path = ROOT / "orchestrator/tests/test_ssdp6_profiles.py"
t = test_path.read_text(encoding="utf-8")
head, tail = t.split("\nclass FrozenLegacyProfileTests", 1)
head = head.replace('self.assertEqual(P.DEFAULT_PROFILE_ID, "ssdp-protocol-6.0")', 'self.assertEqual(P.DEFAULT_PROFILE_ID, "ssdp-protocol-6.1")')
head = head.replace('self.assertEqual(self.descriptor.profile.protocol_version, "6.0.0")', 'self.assertEqual(self.descriptor.profile.protocol_version, "6.1.0")')
head = head.replace('governing_protocol_version="6.0.0"', 'governing_protocol_version="6.1.0"')
head = head.replace('protocol_version="6.0.0"', 'protocol_version="6.1.0"')
old_mapping = '''        self.assertEqual(P.profile_id_for_version("6.0.0"), P.DEFAULT_PROFILE_ID)\n        self.assertEqual(P.profile_id_for_version("6.0"), P.DEFAULT_PROFILE_ID)'''
new_mapping = '''        self.assertEqual(P.profile_id_for_version("6.0.0"), P.SSDP6_PROFILE_ID)\n        self.assertEqual(P.profile_id_for_version("6.0"), P.SSDP6_PROFILE_ID)\n        self.assertEqual(P.profile_id_for_version("6.1.0"), P.DEFAULT_PROFILE_ID)\n        self.assertEqual(P.profile_id_for_version("6.1"), P.DEFAULT_PROFILE_ID)'''
head = replace_required(head, old_mapping, new_mapping, "profile version test")
head = head.replace('self.assertIn("authorized reduced d2->d4 or d1->d4 route", d4_body)', 'self.assertIn("direct d1/d2->d4", d4_body)')
head = head.replace('self.assertIn("do not manufacture a d3 authority mutation", d4_body)', 'self.assertIn("do not manufacture d3 mutation", d4_body)')
frozen60 = r'''

class FrozenProtocol60ProfileTests(unittest.TestCase):
    def test_protocol60_profile_stays_schema_v2_and_version_bound(self) -> None:
        frozen = PS.resolve_packaged(P.SSDP6_PROFILE_ID).snapshot.descriptor
        self.assertEqual(frozen.profile.profile_id, "ssdp-protocol-6.0")
        self.assertEqual(frozen.profile.protocol_version, "6.0.0")
        self.assertEqual(frozen.profile.profile_schema_version, 2)
        self.assertEqual(frozen.schema_version, 2)
        self.assertEqual([s.stage.stage_key for s in frozen.stages], [key for _, key, _ in SSDP6_STAGES])

    def test_protocol60_packaged_bytes_are_frozen(self) -> None:
        import hashlib
        root = REPO_ROOT / "orchestrator/src/sdp_orchestrator/core/resources/protocol/ssdp-protocol-6.0"
        expected = {"prompts.md": "d127b9eb8da165afd905d4c35cc8b7572b201d56", "profile.json": "76c53539a985bc8408f8432932e91e5477696db9"}
        for name, sha in expected.items():
            data = (root / name).read_bytes()
            actual = hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324
            self.assertEqual(actual, sha, name)

    def test_protocol60_profile_is_still_derived_from_protocol60_prompts(self) -> None:
        root = REPO_ROOT / "orchestrator/src/sdp_orchestrator/core/resources/protocol/ssdp-protocol-6.0"
        text = (root / "prompts.md").read_text(encoding="utf-8")
        document = parse_document(text, profile_id=P.SSDP6_PROFILE_ID)
        expected = P.profile_to_json(P.build_profile(document, P.SSDP6_PROFILE_ID).descriptor)
        self.assertEqual((root / "profile.json").read_text(encoding="utf-8"), expected)
'''
test_path.write_text(head + frozen60 + "\n\nclass FrozenLegacyProfileTests" + tail, encoding="utf-8")

# Static Protocol 6.1 behavioral contracts supplement inherited Protocol tests.
(ROOT / "tests/test_protocol_61_evidence_evolution.py").write_text(r'''from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Protocol61EvidenceEvolutionTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_current_version_and_concretization_vocabulary(self) -> None:
        self.assertEqual(self.read("source/PROTOCOL_VERSION").strip(), "6.1.0")
        authority = self.read("source/shared/references/abstraction-and-realization.md")
        self.assertIn("ABSTRACTION  --design / constrain-->  CONCRETIZATION", authority)
        self.assertIn("evidence realization", authority)

    def test_evidence_model_and_stale_evidence_are_explicit(self) -> None:
        evidence = self.read("source/shared/references/evidence-evolution-and-dependencies.md")
        testing = self.read("source/shared/references/testing-and-validation.md")
        for phrase in ("evidence specification", "evidence realization", "observation", "evidence assessment", "EXECUTION_DEPENDS_ON"):
            self.assertIn(phrase, evidence)
        self.assertIn("stale passing", testing.lower())
        self.assertIn("stale failing", testing.lower())

    def test_bounded_dependency_and_history_surfaces_exist(self) -> None:
        dep = self.read("source/SEMANTIC_DEPENDENCIES.md")
        hist = self.read("history/SEMANTIC_EVOLUTION.md")
        self.assertIn("Absence", dep)
        self.assertIn("independence", dep)
        self.assertIn("Semantic Evolution", hist)

    def test_human_facing_background_and_abbreviation_contract(self) -> None:
        writing = self.read("source/shared/references/scientific-technical-writing.md")
        self.assertIn("intended competent reader", writing)
        self.assertIn("full term (ABC)", writing)
        d1 = self.read("source/shared/templates/scientific_method_paper_template.md")
        d2 = self.read("source/shared/templates/numerical_algorithmic_method_paper_template.md")
        self.assertLess(d1.index("## Background and terminology"), d1.index("## Normative scientific / mathematical formulation"))
        self.assertLess(d2.index("## Background and terminology"), d2.index("## Governing numerical / algorithmic formulation"))

    def test_current_prompt_uses_canonical_public_repository(self) -> None:
        prompts = self.read("source/shared/references/development-workflow-prompts.md")
        self.assertIn("https://github.com/hjin98/scientific-software-development-protocol", prompts)
        self.assertNotIn("https://github.com/hjin98/software-development-protocol", prompts)

if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8")

# Current human-facing entry docs: compact version/profile/evidence migration.
readme_path = ROOT / "README.md"
r = readme_path.read_text(encoding="utf-8")
r = r.replace("Current protocol version: **6.0**.", "Current protocol version: **6.1**.")
r = r.replace("Protocol 6 generalizes", "Protocol 6.1 preserves and refines")
r = r.replace("REALIZATION", "CONCRETIZATION").replace("realization", "concretization").replace("Realization", "Concretization")
r = r.replace("alongside current `ssdp-protocol-6.0` schema v2.", "alongside frozen `ssdp-protocol-6.0` schema v2 and current `ssdp-protocol-6.1` schema v2.")
marker = "## Verification and challenge\n"
if "## Evidence and evolution\n" not in r:
    r = r.replace(marker, "## Evidence and evolution\n\nProtocol 6.1 distinguishes downstream **concretization** from **evidence realization**. Evidence follows `evidence specification -> evidence realization -> observation -> evidence assessment`; applicability, target-vs-execution dependencies, stale evidence, bounded semantic dependency views, and semantic-evolution history are first-class maintenance concerns. Evidence is not a fifth semantic authority.\n\n" + marker)
readme_path.write_text(r, encoding="utf-8")

src_readme = ROOT / "source/README.md"
s = src_readme.read_text(encoding="utf-8")
s = s.replace("# Scientific Software Development Protocol 6.0", "# Scientific Software Development Protocol 6.1")
s = s.replace("recursively constrained realization", "recursively constrained concretization")
s = s.replace("realizations", "concretizations").replace("realization", "concretization")
s = s.replace("accepted Specification + code/executable concretization", "accepted Specification + code/executable concretization")
s = s.replace("ships both `sdp-protocol-5.16` profile schema v1 and `ssdp-protocol-6.0` profile schema v2.", "ships frozen `sdp-protocol-5.16` schema v1 and `ssdp-protocol-6.0` schema v2 profiles plus current `ssdp-protocol-6.1` schema v2.")
s = s.replace("- evidence -> `shared/references/testing-and-validation.md`", "- evidence/evolution/dependencies -> `shared/references/evidence-evolution-and-dependencies.md`\n- testing/validation -> `shared/references/testing-and-validation.md`")
src_readme.write_text(s, encoding="utf-8")

port_path = ROOT / "PORTABILITY.md"
port = port_path.read_text(encoding="utf-8")
port = port.replace("Protocol 6 preserves", "Protocol 6.1 preserves")
port = port.replace("https://github.com/hjin98/software-development-protocol", "https://github.com/hjin98/scientific-software-development-protocol")
port = port.replace("| `ssdp-protocol-6.0` | 6.0.0 | 2 | current domain-aware workflow |", "| `ssdp-protocol-6.0` | 6.0.0 | 2 | frozen pre-6.1 compatibility |\n| `ssdp-protocol-6.1` | 6.1.0 | 2 | current evidence/evolution-aware document-controlled workflow |")
port = port.replace("Historical 5.16 prompt/profile bytes remain immutable.", "Historical 5.16 and 6.0 prompt/profile bytes remain immutable.")
port = port.replace("full realization paths", "full concretization paths")
port_path.write_text(port, encoding="utf-8")

# Existing qualification remains the inherited behavioral set; update current
# terminology/version cases and append explicit 6.1 cases.
q_path = ROOT / "qualification/ssdp6/SCENARIOS.md"
q = q_path.read_text(encoding="utf-8")
q = q.replace("# Protocol 6 Behavioral Qualification Scenarios", "# Protocol 6.1 Behavioral Qualification Scenarios")
q = q.replace("Abstraction / realization", "Abstraction / concretization")
q = q.replace("realizations", "concretizations").replace("realization", "concretization").replace("Realization", "Concretization")
q = q.replace("Current installed protocol is 6.0", "Current installed protocol is 6.1")
q = q.replace("Current 6.0 workplan", "Version-bound 6.0 workplan")
q = q.replace("Selected workplan declares 6.0.0 while project default profile is 5.16. Workplan declaration wins and selects `ssdp-protocol-6.0` schema v2.", "Selected workplan declares 6.0.0 while current default is 6.1. Workplan declaration wins and selects frozen `ssdp-protocol-6.0` schema v2.")
if "### 70. Evidence specification survives owner replacement" not in q:
    q += r'''

## G. Protocol 6.1 evidence, evolution, and human-facing context

### 70. Evidence specification survives owner replacement
A property test targets an unchanged D2 invariant but executes through a replaced D4 owner. Keep the evidence specification if its oracle remains valid, remap/rerun it against the new owner, and treat the old execution result as candidate-specific evidence rather than preserving the obsolete owner.

### 71. Stale pass is not confirmation
A historical test passed on an old candidate whose governing proposition or oracle changed. The pass cannot close the current claim until applicability is re-established.

### 72. Stale fail is not refutation
A historical test fails because it encodes superseded D4 behavior while the target invariant remains unchanged. Review/retire or remap the test; do not patch current production code to satisfy stale evidence.

### 73. Common-mode evidence
Three tests share the same erroneous expected-value generator. They are not three independent confirmations of the claim.

### 74. Partial dependency map
A bounded semantic-dependency file contains no edge from changed D2 authority to one consumer, but the mapped scope was never certified complete. Missing edge is not evidence of independence; perform independent affected-surface reasoning.

### 75. Semantic evolution prevents dead-end recurrence
A previously rejected algorithm is proposed again. Git shows chronology and the semantic-evolution record preserves the material reason for rejection. Use that reasoning as history/context while current D2 authority remains controlling.

### 76. Human-facing specialized term
A new D1 paper introduces a project-specific scientific term unknown to its intended competent reader and immediately uses it normatively. Documentation is incomplete until a concise background definition/explanation precedes reliance on the term.

### 77. First-use abbreviation
A new method paper uses `MLFF` before explaining it. Introduce `machine-learning force field (MLFF)` at first explanatory use; independently consumable summary material must remain interpretable on its own.

### 78. Background is not normative substitution
A friendly background paragraph paraphrases a D2 concept imprecisely. The documentation specialist may repair the explanation but cannot replace the precise D2 normative definition editorially.

### 79. Frozen Protocol 6.0 profile
Current default is 6.1, but a workplan declares 6.0.0. Core resolves frozen `ssdp-protocol-6.0`; its prompt/profile bytes and 6.0 terminology remain unchanged.

### 80. Current Protocol 6.1 profile
A 6.1.0 workplan selects `ssdp-protocol-6.1` schema v2. Current prompts use concretization terminology, evidence applicability/impact closure, and the canonical public repository fallback without requiring a Protocol 7 control plane.
'''
q_path.write_text(q, encoding="utf-8")

print("Protocol 6.1 source migration materialized")
