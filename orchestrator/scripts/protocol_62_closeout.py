#!/usr/bin/env python3
"""One-use Protocol 6.2 lifecycle closeout runner.

The runner is deliberately kept under the Orchestrator containment root and is
removed after the durable closeout commit is produced and validated.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

RECOVERY = "b59adc77efe6951912cfd705cc43830c58ca27d0"
BOOTSTRAP = "5a062ebc472755607b9dc66d33a5ebbc4b7429aa"
SEMANTIC_CANDIDATE = "ebbc4591bdfed039512026b8acb3a6749475c1c5"
MAPPING_COMMIT = "bc76b16fda96be09f38a1b40a2ef877e8309534d"
GENERATED_COMMIT = "ca622ea2b1c33e70668060cf0cc2fe9138776f7f"
STAGE_G_RUN = "34566291966"
BASELINE_61 = "cec29671b9db59d20124a6e2ce99725ed60b8f0a"
ROLLBACK_61 = "802e75af261efb4f70d71284d860613a2197b639"

ROOT = Path(__file__).resolve().parents[2]
ACTIVE_62 = ROOT / "workplans/active/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md"
ARCHIVE_62 = ROOT / "workplans/archive/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md"
REV3 = ROOT / "workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md"


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"missing replacement anchor in {path}: {old[:80]!r}")
    if text.count(old) != 1:
        raise RuntimeError(f"non-unique replacement anchor in {path}: {old[:80]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_version_owner() -> None:
    path = ROOT / "source/shared/references/protocol-versioning-and-compatibility.md"
    replace_once(
        path,
        "| `ssdp-protocol-6.1` | 6.1.0 | 2 | accepted current until 6.2 closeout |\n| `ssdp-protocol-6.2` | 6.2.0 | 2 | candidate/current-source successor; accepted only after 6.2 qualification/Review/recovery closeout |",
        "| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |\n| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |",
    )
    replace_once(
        path,
        "Git commits cannot self-name, so this recovery mapping is published only by a later descendant after the recovery target already exists. Until mapping-bearing generated descendants, targeted recovery/parity checks, semantic-evolution/Protocol-7 reconciliation, and lifecycle closeout pass, Protocol 6.1 remains accepted-current/rollback authority.",
        "Git commits cannot self-name, so the recovery mapping was published only by later descendant mapping commit `bc76b16fda96be09f38a1b40a2ef877e8309534d` after the recovery target already existed. Mapping-bearing generated descendants were regenerated at `ca622ea2b1c33e70668060cf0cc2fe9138776f7f`, and Stage G recovery/parity/package/Core acceptance passed in GitHub Actions run `34566291966`.\n\nProtocol 6.2 is accepted-current after qualification, independent Review, immutable recovery mapping, generated-artifact reconciliation, semantic-evolution/Protocol-7 handoff reconciliation, and lifecycle closeout. Protocol 6.1 remains immutable historical rollback authority at `802e75af261efb4f70d71284d860613a2197b639` for version-bound 6.1 work.",
    )


def patch_portability() -> None:
    path = ROOT / "PORTABILITY.md"
    replace_once(
        path,
        "| `ssdp-protocol-6.1` | 6.1.0 | 2 | accepted-current until 6.2 closeout |\n| `ssdp-protocol-6.2` | 6.2.0 | 2 | candidate successor; accepted only after 6.2 qualification/Review/recovery closeout |",
        "| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |\n| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |",
    )
    replace_once(
        path,
        "Protocol 6.1 remains accepted-current/rollback until 6.2 qualification, independent candidate Review, immutable recovery mapping, generated-artifact reconciliation and lifecycle closeout all pass.",
        "Protocol 6.2 is accepted-current. Its public-source fallback remains the exact immutable bootstrap `5a062ebc472755607b9dc66d33a5ebbc4b7429aa`, while accepted rollback/recovery resolves to `b59adc77efe6951912cfd705cc43830c58ca27d0`. Protocol 6.1 remains an immutable historical rollback option for explicitly version-bound 6.1 work at `802e75af261efb4f70d71284d860613a2197b639`. Protocol 7 remains pre-cutover and may not displace this document-controlled baseline until its own D3/D4/qualification/cutover gates close.",
    )


def patch_readmes_and_dependency_view() -> None:
    root_readme = ROOT / "README.md"
    replace_once(
        root_readme,
        "Current source candidate: **Protocol 6.2**. Accepted rollback/current release remains Protocol 6.1 until Protocol 6.2 qualification, independent Review, recovery mapping, generated-artifact reconciliation, and lifecycle closeout complete.",
        "Current accepted document-controlled release: **Protocol 6.2**. Protocol 6.1 remains the immutable historical rollback for explicitly version-bound 6.1 work; Protocol 7 remains a proposed deterministic-control-plane successor and is not cut over.",
    )
    replace_once(
        root_readme,
        "6.1.0  -> 802e75af261efb4f70d71284d860613a2197b639\n```",
        "6.1.0  -> 802e75af261efb4f70d71284d860613a2197b639\n6.2.0  -> b59adc77efe6951912cfd705cc43830c58ca27d0\n```",
    )
    replace_once(
        root_readme,
        "Protocol 6.2 replacement public-source bootstrap is **`5a062ebc472755607b9dc66d33a5ebbc4b7429aa`**. That immutable self-reference-safe source snapshot passed source regression, canonical package build, and independent standalone package/link validation before its SHA was published by a descendant. Current 6.2 public fallback, when no compatible installed source is readable, resolves only to that exact ref. Repository default branch is never a protocol-version oracle.",
        "Protocol 6.2 replacement public-source bootstrap is **`5a062ebc472755607b9dc66d33a5ebbc4b7429aa`**. That immutable self-reference-safe source snapshot passed source regression, canonical package build, and independent standalone package/link validation before its SHA was published by a descendant. Accepted Protocol 6.2 recovery is **`b59adc77efe6951912cfd705cc43830c58ca27d0`**; bootstrap and recovery identities are intentionally distinct. Current 6.2 public fallback, when no compatible installed source is readable, resolves only to the bootstrap exact ref. Repository default branch is never a protocol-version oracle.",
    )

    source_readme = ROOT / "source/README.md"
    replace_once(
        source_readme,
        "`source/` is the canonical Protocol 6.2 source. Generated distributions and orchestrator snapshots are derivatives.",
        "`source/` is the canonical accepted-current Protocol 6.2 source. Generated distributions and orchestrator snapshots are derivatives; Protocol 6.1 remains immutable historical rollback authority for version-bound 6.1 work.",
    )

    deps = ROOT / "source/SEMANTIC_DEPENDENCIES.md"
    replace_once(
        deps,
        "ssdp-protocol-6.1 CONSTRAINED_BY -> immutable accepted Protocol 6.1 semantics\nssdp-protocol-6.2 CONSTRAINED_BY -> Protocol 6.2 candidate/current source",
        "ssdp-protocol-6.1 CONSTRAINED_BY -> immutable historical Protocol 6.1 rollback semantics\nssdp-protocol-6.2 CONSTRAINED_BY -> accepted-current Protocol 6.2 semantics",
    )
    replace_once(
        deps,
        "Frozen 5.16/6.0/6.1 profiles remain independent compatibility resources. Protocol 6.2 is not accepted-current until its qualification/Review/recovery lifecycle closes.",
        "Frozen 5.16/6.0/6.1 profiles remain independent compatibility resources. Protocol 6.2 is accepted-current after qualification, independent Review, recovery mapping, generated-artifact reconciliation, Protocol 7 handoff reconciliation, and lifecycle closeout.",
    )


def write_protocol7_revision3() -> None:
    if REV3.exists():
        raise RuntimeError(f"Protocol 7 Revision 3 already exists: {REV3}")
    REV3.write_text(
        f'''---
kind: protocol-major-revision-workplan-amendment
workplan_id: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION
amends_workplan: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION
extends_amendment: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE
protocol_version: 6.2.0
target_protocol_version: 7.0.0
status: active
created_date: 2026-09-11
reconciliation_scope: representation-version-inheritance-only
d3_architecture_mutation: none
active_serious_challenge: none
---

# Protocol 7 Revision 3 — Protocol 6.2 Inheritance Reconciliation

## Background and authority boundary

This compact companion reconciles the active Protocol 7 handoff after acceptance of Scientific Software Development Protocol (SSDP) 6.2. It changes only the inherited document-controlled baseline, representation contract, and compatibility/recovery identities. It does **not** alter or re-accept the deterministic-control-plane D3 architecture in the parent, Revision 1, or Revision 2, and it does not authorize D4 implementation.

The parent plus Revisions 1 and 2 remain the controlling Protocol 7 design handoff for deterministic lifecycle ownership, reducer purity, storage/transport, recovery, cutover, and machine-control semantics. This revision has latest precedence only where those artifacts describe Protocol 6.1 as the current document-controlled baseline or fallback.

## 1. Accepted inherited baseline

Protocol 7 now inherits accepted-current Protocol 6.2 rather than Protocol 6.1 as its pre-cutover document-controlled parent. The accepted identities are:

```text
Protocol 6.2 semantic candidate -> {SEMANTIC_CANDIDATE}
Protocol 6.2 public bootstrap   -> {BOOTSTRAP}
Protocol 6.2 recovery           -> {RECOVERY}
Protocol 6.1 historical rollback -> {ROLLBACK_61}
```

Every accepted Protocol 6.1 doctrine remains inherited through Protocol 6.2. Protocol 7 additionally inherits Protocol 6.2 Lossless Representation semantics: governed scope cannot be narrowed for convenience; generic doctrine has one canonical detailed owner; root/concern/leaf activation is explicit, bounded and acyclic; ordinary links, semantic-dependency views, package membership and generated routing traces do not become activation authority; cold doctrine remains discoverable/reachable; context reuse is validity-scoped; current truth is separated from history; importance weighting cannot omit lower-salience mandatory closure; and static routing/package evidence must not be represented as live model telemetry.

## 2. What this reconciliation does not change

No Protocol 7 control-plane field, state transition, reducer rule, event schema, persistence contract, ownership boundary, recovery algorithm, cutover invariant, or D3 component identity changes merely because the inherited document representation advanced from 6.1 to 6.2. Do not introduce a wrapper, compatibility registry, duplicate activation graph, or new machine field solely to mirror Protocol 6.2 representation doctrine.

If future Protocol 7 architecture cannot preserve an accepted Protocol 6.2 invariant, reopen the earliest affected D3 authority and resolve the contradiction there. Do not patch D4 around an inadequate D3 abstraction.

## 3. Pre-D4 gate disposition

```text
PROTOCOL 6.2 COMPLETION / QUALIFICATION / RECOVERY: SATISFIED
PROTOCOL 6.2 REPRESENTATION-INHERITANCE RECONCILIATION: SATISFIED BY THIS COMPANION
PROTOCOL 7 DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN / SUPERSESSION: STILL REQUIRED
PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED
```

The remaining D3 reopen is the pre-existing Protocol 7 requirement to deliberately supersede/reconcile the current Orchestrator architecture before D4 implementation. This revision neither performs that reopen nor converts the already-reviewed proposed architecture into executable authority.

## 4. Compatibility, fallback, and cutover

Before qualified Protocol 7 cutover, the governing document-controlled fallback/rollback baseline is Protocol 6.2 recovery `{RECOVERY}`. Protocol 6.1 recovery `{ROLLBACK_61}` remains available only for explicitly version-bound historical 6.1 work.

The Protocol 6.2 public fallback remains its exact bootstrap `{BOOTSTRAP}`; recovery identity is not substituted for public bootstrap. Protocol 7 must preserve this bootstrap/recovery distinction in any later source-resolution or migration machinery.

No `main` merge or Protocol 7 cutover is implied by this reconciliation. Qualified Protocol 7 cutover remains separately governed by the parent/revisions and requires the outstanding D3 architecture reopen plus subsequent D4, Review, verification/qualification, recovery and cutover gates.

## 5. Handoff

Protocol 7 work SHALL read the parent, Revisions 1-2, and this Revision 3 as one composed handoff. Where a prior artifact says Protocol 6.1 is the final/current document-controlled baseline, read that statement as historical context superseded by this revision for current work. All unrelated parent/revision requirements remain unchanged.
''',
        encoding="utf-8",
    )


def patch_authority_index() -> None:
    path = ROOT / "workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("protocol_version: 6.0.0", "protocol_version: 6.2.0", 1)
    text = text.replace("reviewed_date: 2026-09-10", "reviewed_date: 2026-09-11", 1)

    start = text.index("## Protocol 6.2 current implementation handoff")
    end = text.index("## Protocol 7.0 current design handoff")
    section62 = f'''## Protocol 6.2 completed handoff

Protocol 6.2 lossless-representation/progressive-disclosure implementation, qualification, independent Review, recovery, generated reconciliation, and closeout are complete. The governing workplan is preserved byte-identically at:

1. `workplans/archive/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md`

Current disposition:

```text
SERIOUS CHALLENGE: NONE
SEMANTIC CANDIDATE: {SEMANTIC_CANDIDATE}
PUBLIC BOOTSTRAP: {BOOTSTRAP}
INVALIDATED BOOTSTRAP ATTEMPT: 1181c2031710c5d343194d87d08543290fded0ab
QUALIFICATION: ORIGINAL 115/115 PASS + COLD-ROUTE REQUALIFICATION PASS + BOOTSTRAP REQUALIFICATION PASS
INDEPENDENT REVIEW: PASS — qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2.md
RECOVERY: {RECOVERY}
RECOVERY MAPPING COMMIT: {MAPPING_COMMIT}
MAPPING-BEARING GENERATED COMMIT: {GENERATED_COMMIT}
STAGE G ACCEPTANCE: PASS — GITHUB ACTIONS RUN {STAGE_G_RUN}
LIFECYCLE STATUS: COMPLETED / ARCHIVED
PARENT ACCEPTED BASELINE: Protocol 6.1 closeout {BASELINE_61}
PARENT HISTORICAL ROLLBACK: {ROLLBACK_61}
CURRENT ACCEPTED DOCUMENT-CONTROLLED BASELINE: Protocol 6.2
```

The public-source bootstrap and accepted recovery remain intentionally distinct. Static activation sensors remain structural evidence only; no live token, latency, cache, or model-performance claim was accepted without corresponding live telemetry.

'''
    text = text[:start] + section62 + text[end:]

    start = text.index("## Protocol 7.0 current design handoff")
    end = text.index("## Version/cutover rule")
    section7 = f'''## Protocol 7.0 current design handoff

Protocol 7.0 design/implementation/review SHALL read and satisfy, as one composed handoff:

1. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION.md`
2. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE.md`
3. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE.md`
4. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md`

Precedence:

- Revision 1 closes ownership, semantic/control binding, storage/transport, cutover, lifecycle-migration, graph-completeness, and compatibility gaps and corrects Scheduler/control-kernel ownership;
- Revision 2 closes reducer-purity, ambient-state, external-effect, deterministic replay, and canonical recovery gaps;
- Revision 3 changes only representation/version inheritance after Protocol 6.2 acceptance: current pre-cutover document-controlled baseline and fallback/rollback become Protocol 6.2, while the parent/Revisions 1-2 D3 architecture semantics remain unchanged;
- every parent requirement not explicitly changed by a later revision remains binding.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
WORKPLAN DESIGN REVIEW: PASS
IMPLEMENTATION STATUS: PROPOSED
PROTOCOL 6.1 HISTORICAL COMPLETION/RECOVERY: SATISFIED
PROTOCOL 6.2 COMPLETION/QUALIFICATION/RECOVERY PREREQUISITE: SATISFIED
PROTOCOL 6.2 REPRESENTATION-INHERITANCE RECONCILIATION: SATISFIED
CURRENT PRE-CUTOVER FALLBACK/ROLLBACK BASELINE: Protocol 6.2 recovery {RECOVERY}
REMAINING PROTOCOL-7-SPECIFIC PRE-D4 REQUIREMENT:
  1. DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN/SUPERSESSION
PROTOCOL 7 D4: NOT AUTHORIZED
```

Protocol 7 D4 remains unauthorized until the existing deliberate D3 Orchestrator architecture reopen/supersession requirement closes. Revision 3 does not perform that reopen and no `main` cutover is implied.

'''
    text = text[:start] + section7 + text[end:]

    start = text.index("## Version/cutover rule")
    end = text.index("## Historical discipline")
    version = f'''## Version/cutover rule

There is exactly one canonical workflow-control authority for any current run.

- Protocol 6.2 is the accepted-current document-controlled baseline; version-bound 6.1 work may still resolve immutable historical recovery `{ROLLBACK_61}`.
- Protocol 7 remains proposed/pre-cutover. Its current fallback/rollback baseline is Protocol 6.2 recovery `{RECOVERY}` until Protocol 7 itself completes the outstanding D3 architecture reopen and subsequent D4/Review/qualification/recovery/cutover gates.
- Under Protocol 7 after qualified cutover, the deterministic orchestrator control plane owns machine lifecycle transitions while workplans/skills/documents remain semantic artifacts.
- Shadow comparison is permitted only while one side remains explicitly non-authoritative.
- No `main` merge/cutover is authorized by Protocol 6.2 closeout.

'''
    text = text[:start] + version + text[end:]
    path.write_text(text, encoding="utf-8")


def patch_history() -> None:
    path = ROOT / "history/SEMANTIC_EVOLUTION.md"
    text = path.read_text(encoding="utf-8")
    marker = "\n## Maintenance\n"
    if marker not in text or "## Protocol 6.1 -> Protocol 6.2" in text:
        raise RuntimeError("unexpected semantic-history closeout precondition")
    entry = f'''
## Protocol 6.1 -> Protocol 6.2

Protocol 6.2 strengthens representation and progressive disclosure without retiring any accepted Protocol 6.1 doctrine or still-valid historical capability.

- **Change:** current protocol communication is normalized around one canonical detailed owner per generic rule, a minimal universal kernel, explicit bounded root/concern/leaf activation, visible cold-path retrieval, validity-scoped context reuse, importance-weighted salience without acceptance loss, and current-vs-history separation. Current semantic descent uses `abstraction-and-concretization.md`; frozen historical profiles/paths retain their original identifiers and bytes.
- **Preservation:** the accepted Protocol 6.1 baseline is `{BASELINE_61}`. The finite preservation census and T01-T39 transformation map were independently falsified against that baseline; no accepted capability was found weakened, orphaned, or retired for compaction convenience.
- **Public-source staging:** first bootstrap attempt `1181c2031710c5d343194d87d08543290fded0ab` was invalidated after an explicit documentation cold-route defect was found. Replacement self-reference-safe public bootstrap `{BOOTSTRAP}` contains the repaired route set and was validated before later publication; current public fallback resolves only to this exact bootstrap, never default/latest.
- **Qualified semantic candidate:** `{SEMANTIC_CANDIDATE}`. Qualification comprises the original 115/115 behavioral pass plus bounded cold-route and bootstrap affected requalifications. Static activation sensors are structural proxies only; the release makes no unsupported live token, latency, cache, or model-performance claim.
- **Independent Review:** PASS with no Serious Challenge and no blockers; record `qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2.md`. Immutable recovery is `{RECOVERY}`, chosen only after the independent PASS so the accepted candidate and required decision evidence are present through ancestry.
- **Recovery publication:** mapping commit `{MAPPING_COMMIT}` publishes `6.2.0 -> {RECOVERY}` only after the recovery target exists. Mapping-bearing distributions were regenerated at `{GENERATED_COMMIT}`. Stage G targeted recovery/parity, source regression, canonical package build/validation, committed distribution parity, snapshot parity and Orchestrator Core acceptance passed in GitHub Actions run `{STAGE_G_RUN}`.
- **Protocol 7 reconciliation:** active Revision 3 changes only the inherited document-controlled baseline/representation contract from Protocol 6.1 to accepted Protocol 6.2. It does not change the proposed deterministic-control-plane D3 architecture and does not authorize D4. Protocol 7 remains blocked on its pre-existing deliberate D3 Orchestrator architecture reopen/supersession requirement.
- **Lifecycle disposition:** COMPLETED / ARCHIVED after current authority/version/portability/dependency/history/index surfaces were reconciled, the Protocol 6.2 workplan was moved byte-identically to `workplans/archive/`, generated descendants were rebuilt from canonical source, and final repository/Core acceptance passed. Protocol 6.2 is accepted-current; Protocol 6.1 recovery `{ROLLBACK_61}` remains immutable historical rollback for explicitly version-bound 6.1 work.

'''
    path.write_text(text.replace(marker, "\n" + entry + "## Maintenance\n", 1), encoding="utf-8")


def archive_workplan() -> None:
    if not ACTIVE_62.exists():
        raise RuntimeError("active Protocol 6.2 workplan missing")
    if ARCHIVE_62.exists():
        raise RuntimeError("Protocol 6.2 archive destination already exists")
    ARCHIVE_62.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(ACTIVE_62), str(ARCHIVE_62))


def write_closeout_test() -> None:
    path = ROOT / "tests/test_protocol_62_closeout.py"
    if path.exists():
        raise RuntimeError("Protocol 6.2 closeout test already exists")
    path.write_text(
        f'''from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Protocol62CloseoutTests(unittest.TestCase):
    def test_current_and_historical_profile_state_is_explicit(self):
        versioning = (ROOT / "source/shared/references/protocol-versioning-and-compatibility.md").read_text()
        portability = (ROOT / "PORTABILITY.md").read_text()
        self.assertIn("| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |", versioning)
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |", versioning)
        self.assertIn("| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |", portability)
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |", portability)

    def test_recovery_bootstrap_and_archive_closeout(self):
        versioning = (ROOT / "source/shared/references/protocol-versioning-and-compatibility.md").read_text()
        self.assertIn("6.2.0  -> {RECOVERY}", versioning)
        self.assertIn("6.2.0 public-source bootstrap -> {BOOTSTRAP}", versioning)
        self.assertNotEqual("{RECOVERY}", "{BOOTSTRAP}")
        self.assertFalse((ROOT / "workplans/active/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md").exists())
        self.assertTrue((ROOT / "workplans/archive/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md").is_file())

    def test_protocol7_is_reconciled_but_d4_stays_blocked(self):
        rev3 = (ROOT / "workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md").read_text()
        index = (ROOT / "workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md").read_text()
        self.assertIn("d3_architecture_mutation: none", rev3)
        self.assertIn("PROTOCOL 7 DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN / SUPERSESSION: STILL REQUIRED", rev3)
        self.assertIn("PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED", rev3)
        self.assertIn("PROTOCOL 6.2 REPRESENTATION-INHERITANCE RECONCILIATION: SATISFIED", index)
        self.assertIn("PROTOCOL 7 D4: NOT AUTHORIZED", index)

    def test_current_dependency_view_names_62_as_current(self):
        dependencies = (ROOT / "source/SEMANTIC_DEPENDENCIES.md").read_text()
        self.assertIn("ssdp-protocol-6.2 CONSTRAINED_BY -> accepted-current Protocol 6.2 semantics", dependencies)
        self.assertIn("ssdp-protocol-6.1 CONSTRAINED_BY -> immutable historical Protocol 6.1 rollback semantics", dependencies)


if __name__ == "__main__":
    unittest.main()
''',
        encoding="utf-8",
    )


def assert_frozen_profiles() -> None:
    expected = {
        "orchestrator/src/sdp_orchestrator/core/resources/protocol/sdp-protocol-5.16": "10a5f6707697e55d9e762db7f3b25b19640fccb4",
        "orchestrator/src/sdp_orchestrator/core/resources/protocol/ssdp-protocol-6.0": "16e5b378a87e32ec648305ba865377bfdf5bdf62",
        "orchestrator/src/sdp_orchestrator/core/resources/protocol/ssdp-protocol-6.1": "437f95bf15fb8f9ec430fa5e6de221c9a99af299",
    }
    for repo_path, tree_sha in expected.items():
        got = subprocess.check_output(["git", "rev-parse", f"HEAD:{repo_path}"], cwd=ROOT, text=True).strip()
        if got != tree_sha:
            raise RuntimeError(f"frozen profile drift: {repo_path}: {got} != {tree_sha}")


def main() -> None:
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")

    patch_version_owner()
    patch_portability()
    patch_readmes_and_dependency_view()
    write_protocol7_revision3()
    patch_authority_index()
    patch_history()
    archive_workplan()
    write_closeout_test()

    run("python", "-m", "pip", "install", "-r", "source/requirements-validation.txt")
    out = Path("/tmp/protocol-dist")
    shutil.rmtree(out, ignore_errors=True)
    run("python", "source/build_skills.py", "--output", str(out))
    run("python", "source/validate_packages.py", "--dist", str(out))
    shutil.rmtree(ROOT / "dist")
    shutil.copytree(out, ROOT / "dist")
    run("python", "source/check_dist.py", "--expected", str(out), "--committed", "dist")

    run("python", "-m", "unittest", "tests.test_protocol_62_representation", "-v")
    run("python", "-m", "unittest", "tests.test_protocol_62_closeout", "-v")
    run("python", "-m", "unittest", "discover", "-s", "tests", "-v")
    run("git", "diff", "--check")

    run("python", "-m", "pip", "install", "./orchestrator", "-r", "orchestrator/requirements-dev.txt")
    run("python", "orchestrator/scripts/generate_protocol_snapshot.py", "--check")
    run("python", "orchestrator/scripts/run_core_tests.py")
    assert_frozen_profiles()

    run("git", "add", "-A")
    run("git", "commit", "-m", "Close Protocol 6.2 lifecycle and reconcile Protocol 7")
    run("git", "push", "origin", "HEAD:ssdp-6.2-lossless-representation")


if __name__ == "__main__":
    main()
