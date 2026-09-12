#!/usr/bin/env python3
"""One-use Protocol 6.3 lifecycle closeout runner.

This runner mutates only current lifecycle/version/routing/evidence surfaces after
R2 Review PASS and Stage-G recovery-mapped acceptance. Historical evidence and
the reviewed workplan are preserved rather than rewritten retrospectively.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEMANTIC = "190c8b4d352c203ef74c94d57c4f18d30eb7186d"
BOOTSTRAP = "86c13cab6bdd1991dffa94e277db8eacf87e2e11"
BOOTSTRAP_MAPPING = "a8dac814cc2813b3bb336e5b6abde5fbcf44949e"
REVIEW_RECOVERY = "9f353097fab36e325a325f1c2f9d9cec32e86177"
RECOVERY_MAPPING = "0c76c0461b7376f17182d29ba145a198a092463c"
GENERATED = "e75282ae850b774a9466902f4c74ba6a179116bd"
STAGE_G_RUN = "34699052516"
BASE_62 = "b59adc77efe6951912cfd705cc43830c58ca27d0"
SEMANTIC_62 = "ebbc4591bdfed039512026b8acb3a6749475c1c5"
BOOTSTRAP_62 = "5a062ebc472755607b9dc66d33a5ebbc4b7429aa"
ACTIVE_WP = ROOT / "workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md"
ARCHIVE_WP = ROOT / "workplans/archive/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md"
REV4 = ROOT / "workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one replacement anchor, found {count}: {old[:100]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        raise RuntimeError(f"{path}: marker already present: {marker}")
    path.write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8")


def patch_versioning() -> None:
    p = ROOT / "source/shared/references/protocol-versioning-and-compatibility.md"
    replace_once(
        p,
        "Protocol 6.3 recovery is separately mapped to `9f353097fab36e325a325f1c2f9d9cec32e86177` after independent Review R2 PASS. Bootstrap and recovery identities are distinct. Protocol 6.2 remains accepted-current until mapping-bearing generated descendants and Stage G lifecycle closeout pass.",
        f"Protocol 6.3 recovery is separately mapped to `{REVIEW_RECOVERY}` after independent Review R2 PASS. Bootstrap and recovery identities are distinct. Mapping-bearing generated descendants were regenerated at `{GENERATED}`, and Stage G recovery/parity/package/profile/Core acceptance passed in GitHub Actions run `{STAGE_G_RUN}`. Protocol 6.3 is accepted-current after lifecycle closeout; Protocol 6.2 remains immutable historical rollback authority for version-bound 6.2 work.",
    )
    replace_once(
        p,
        "| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |\n| `ssdp-protocol-6.3` | 6.3.0 | 2 | candidate; generated and independently parity-checked |",
        "| `ssdp-protocol-6.2` | 6.2.0 | 2 | frozen historical rollback |\n| `ssdp-protocol-6.3` | 6.3.0 | 2 | accepted current |",
    )
    replace_once(
        p,
        "During 6.3 qualification, the 6.2 profile bytes are frozen as the immutable predecessor resource while 6.2 remains accepted-current until 6.3 cutover. Schema v2 remains unless an actual machine profile contract changes. Core selects by declared protocol/profile identity, not one global latest constant. Frozen profile bytes/behavior remain independently testable. A generic profile/package may include 6.3 PEM doctrine/template but never a live project's `PROJECT-ENGINEERING-MEMORY.md` or derived local project summary.",
        "Protocol 6.3 is accepted-current. The 6.2 profile bytes remain frozen as an immutable predecessor/rollback resource. Schema v2 remains because no machine profile contract changed. Core selects by declared protocol/profile identity, not one global latest constant. Frozen profile bytes/behavior remain independently testable. A generic profile/package may include 6.3 PEM doctrine/template but never a live project's `PROJECT-ENGINEERING-MEMORY.md` or derived local project summary.",
    )
    replace_once(p, "## Protocol 6.3 candidate/bootstrap/recovery staging", "## Protocol 6.3 accepted bootstrap/recovery lifecycle")
    replace_once(
        p,
        f"The pre-repair Protocol 6.3 bootstrap `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, second bootstrap `5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb`, owner-binding bootstrap `e12572c021087308570abfa41657a910c6896457`, and D4R3 bootstrap `dc22f09fd38dbbfeaeb0160152da9b284654f66e` are immutable historical evidence only. D9 changed canonical validator semantics, so Replacement self-reference-safe source snapshot `{BOOTSTRAP}` passed source regression, package/profile integrity, Orchestrator Core, and bootstrap readiness before this later descendant published its exact SHA as the sole current 6.3 public-source fallback. Protocol 6.3 recovery is separately pinned to `{REVIEW_RECOVERY}` after R2 Review PASS; the accepted 6.2 mappings remain operative while Protocol 6.2 is accepted-current until mapping-bearing generated descendants and Stage G lifecycle closeout pass. The Protocol 6.3 public bootstrap remains `{BOOTSTRAP}` and is not recovery.",
        f"The pre-repair Protocol 6.3 bootstrap `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, second bootstrap `5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb`, owner-binding bootstrap `e12572c021087308570abfa41657a910c6896457`, and D4R3 bootstrap `dc22f09fd38dbbfeaeb0160152da9b284654f66e` remain immutable historical evidence only. D9 changed canonical validator semantics, so replacement self-reference-safe source snapshot `{BOOTSTRAP}` passed source regression, package/profile integrity, Orchestrator Core, and bootstrap readiness before descendant `{BOOTSTRAP_MAPPING}` published its exact SHA as the sole 6.3 public-source fallback. Independent Review R2/recovery target `{REVIEW_RECOVERY}` is intentionally distinct; descendant `{RECOVERY_MAPPING}` published the recovery mapping, mapping-bearing descendants were regenerated at `{GENERATED}`, and Stage G acceptance passed in run `{STAGE_G_RUN}`. Protocol 6.3 is accepted-current; version-bound 6.2 recovery `{BASE_62}` remains immutable historical rollback. The public bootstrap is not recovery.",
    )


def patch_portability() -> None:
    p = ROOT / "PORTABILITY.md"
    replace_once(p, "## Protocol 6.3 candidate routing contract", "## Protocol 6.3 routing contract")
    replace_once(
        p,
        f"For Protocol 6.3, pre-repair bootstrap `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, second bootstrap `5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb`, owner-binding bootstrap `e12572c021087308570abfa41657a910c6896457`, and D4R3 bootstrap `dc22f09fd38dbbfeaeb0160152da9b284654f66e` are historical evidence only. D9 changed canonical validator semantics. Replacement self-reference-safe source snapshot `{BOOTSTRAP}` passed bootstrap readiness before a later descendant published its exact SHA as the sole authorized version-bound 6.3 public fallback. Recovery is separately mapped to `{REVIEW_RECOVERY}` after R2 Review PASS; Protocol 6.2 remains accepted-current until Stage G generated reconciliation and lifecycle closeout pass. If neither compatible local source nor mapped compatible immutable public source can be read, report truthful non-closure.",
        f"For Protocol 6.3, pre-repair bootstrap `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, second bootstrap `5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb`, owner-binding bootstrap `e12572c021087308570abfa41657a910c6896457`, and D4R3 bootstrap `dc22f09fd38dbbfeaeb0160152da9b284654f66e` are historical evidence only. D9 changed canonical validator semantics. Replacement self-reference-safe source snapshot `{BOOTSTRAP}` passed bootstrap readiness before descendant `{BOOTSTRAP_MAPPING}` published its exact SHA as the sole authorized version-bound 6.3 public fallback. Recovery is separately mapped to `{REVIEW_RECOVERY}` after R2 Review PASS; descendant `{RECOVERY_MAPPING}` published that mapping and mapping-bearing generated state `{GENERATED}` passed Stage G acceptance in run `{STAGE_G_RUN}`. Protocol 6.3 is accepted-current; Protocol 6.2 recovery `{BASE_62}` remains immutable historical rollback. If neither compatible local source nor mapped compatible immutable public source can be read, report truthful non-closure.",
    )
    replace_once(
        p,
        "| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |\n| `ssdp-protocol-6.3` | 6.3.0 | 2 | candidate after distinct generation/qualification |",
        "| `ssdp-protocol-6.2` | 6.2.0 | 2 | frozen historical rollback |\n| `ssdp-protocol-6.3` | 6.3.0 | 2 | accepted current |",
    )
    replace_once(
        p,
        "During Protocol 6.3 candidate qualification, the 6.2 resource is an immutable predecessor snapshot while Protocol 6.2 remains accepted-current operational authority until cutover. Historical profile/prompt bytes remain immutable. Workplan `protocol_version` selects compatible semantics before stage interpretation. Serious Challenge/human-pending state stops ordinary automatic closure; orchestration represents/routes state but never decides scientific truth. PEM schema versioning is independent of orchestration profile schema; Protocol 6.3 supports PEM schema 1 and fails safe for unsupported memory-dependent decisions.",
        "Protocol 6.3 is accepted-current and the 6.2 resource remains an immutable predecessor/rollback snapshot. Historical profile/prompt bytes remain immutable. Workplan `protocol_version` selects compatible semantics before stage interpretation. Serious Challenge/human-pending state stops ordinary automatic closure; orchestration represents/routes state but never decides scientific truth. PEM schema versioning is independent of orchestration profile schema; Protocol 6.3 supports PEM schema 1 and fails safe for unsupported memory-dependent decisions.",
    )
    replace_once(
        p,
        f"Protocol 6.2 remains accepted-current while 6.3 is a candidate. Version-bound 6.2 public fallback remains exact bootstrap `{BOOTSTRAP_62}` and accepted recovery remains `{BASE_62}`. Version-bound 6.3 public fallback is usable only when the `6.3.0 public bootstrap` mapping above contains an immutable Git SHA; an unavailable sentinel means no 6.3 fallback is currently authorized. This does not make 6.3 accepted-current. Protocol 6.3 recovery is now mapped to `{REVIEW_RECOVERY}`, distinct from public bootstrap `{BOOTSTRAP}`, but Protocol 6.3 cannot displace the 6.2 baseline until regenerated parity and the remaining Stage G lifecycle gates close.",
        f"Protocol 6.3 is accepted-current after independent Review R2, exact recovery mapping, regenerated package/profile parity, and Stage G lifecycle closeout. Version-bound 6.3 public fallback is exact bootstrap `{BOOTSTRAP}` and accepted recovery is separately `{REVIEW_RECOVERY}`. Protocol 6.2 public bootstrap `{BOOTSTRAP_62}` and recovery `{BASE_62}` remain immutable historical resources for explicitly version-bound 6.2 work. Repository default/latest remains forbidden as a version oracle.",
    )


def patch_navigation() -> None:
    p = ROOT / "README.md"
    replace_once(
        p,
        "Current accepted document-controlled release: **Protocol 6.2**. This branch contains the **Protocol 6.3 candidate implementation** and does not make 6.3 accepted-current by repository presence. Protocol 6.2 remains the immutable rollback/current authority for version-bound 6.2 work until the 6.3 qualification, bootstrap/profile/package, independent Review, recovery, and lifecycle gates close. Protocol 7 remains a proposed deterministic-control-plane successor and is not cut over.",
        f"Current accepted document-controlled release: **Protocol 6.3**. Accepted recovery is `{REVIEW_RECOVERY}` and the distinct immutable public-source bootstrap is `{BOOTSTRAP}`. Protocol 6.2 recovery `{BASE_62}` remains immutable historical rollback for explicitly version-bound 6.2 work. Protocol 7 remains a proposed deterministic-control-plane successor and is not cut over.",
    )
    replace_once(p, "The universal current-candidate kernel is", "The universal current kernel is")
    replace_once(
        p,
        f"6.2.0  -> {BASE_62}\n```",
        f"6.2.0  -> {BASE_62}\n6.3.0  -> {REVIEW_RECOVERY}\n```",
    )
    old = f"**Earlier Protocol 6.3 bootstrap attempts `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, `5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb`, owner-binding-invalidated `e12572c021087308570abfa41657a910c6896457`, and D4R3 snapshot `dc22f09fd38dbbfeaeb0160152da9b284654f66e` are historical only; current public-source bootstrap is `{BOOTSTRAP}`; Protocol 6.3 recovery is mapped to `{REVIEW_RECOVERY}` after R2 Review PASS; Protocol 6.2 remains accepted-current until the remaining Stage G generated-reconciliation and lifecycle gates close.** Replacement self-reference-safe source snapshot `{BOOTSTRAP}` was qualified before this later descendant published the exact mapping as the sole authorized version-bound 6.3 public fallback."
    new = f"**Earlier Protocol 6.3 bootstrap attempts `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, `5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb`, owner-binding-invalidated `e12572c021087308570abfa41657a910c6896457`, and D4R3 snapshot `dc22f09fd38dbbfeaeb0160152da9b284654f66e` are historical only. Current 6.3 public-source bootstrap is `{BOOTSTRAP}`; accepted recovery is `{REVIEW_RECOVERY}`; bootstrap and recovery are intentionally distinct.** Bootstrap mapping descendant `{BOOTSTRAP_MAPPING}`, recovery mapping descendant `{RECOVERY_MAPPING}`, and generated reconciliation `{GENERATED}` preserve self-reference-safe publication. Stage G acceptance passed in run `{STAGE_G_RUN}`."
    replace_once(p, old, new)

    p = ROOT / "source/README.md"
    replace_once(p, "# Scientific Software Development Protocol 6.3 Candidate Source", "# Scientific Software Development Protocol 6.3 Source")
    replace_once(
        p,
        "`source/` is the canonical Protocol 6.3 candidate source on the 6.3 implementation branch. Protocol 6.2 remains accepted-current until the 6.3 qualification, bootstrap/profile/package, independent Review, recovery, and lifecycle gates close. Generated distributions and orchestrator snapshots are derivatives; frozen historical/version-bound resources remain immutable.",
        f"`source/` is the canonical accepted-current Protocol 6.3 source. Accepted recovery is `{REVIEW_RECOVERY}` and public-source bootstrap is separately `{BOOTSTRAP}`. Protocol 6.2 recovery `{BASE_62}` remains immutable historical rollback for version-bound 6.2 work. Generated distributions and orchestrator snapshots are derivatives; frozen historical/version-bound resources remain immutable.",
    )
    replace_once(
        p,
        f"Current path uses `abstraction-and-concretization.md`. Frozen 5.16/6.0/6.1/6.2 files/profiles retain their version-faithful identifiers/bytes. Protocol 6.2 accepted recovery remains `{BASE_62}` and public bootstrap remains `{BOOTSTRAP_62}` for version-bound 6.2 work. Current Protocol 6.3 public fallback is exact bootstrap `{BOOTSTRAP}`. Stage-G recovery is separately mapped to `{REVIEW_RECOVERY}` after R2 Review PASS; Protocol 6.2 remains accepted-current until mapping-bearing generated artifacts and lifecycle closeout pass.",
        f"Current path uses `abstraction-and-concretization.md`. Frozen 5.16/6.0/6.1/6.2 files/profiles retain their version-faithful identifiers/bytes. Protocol 6.2 recovery `{BASE_62}` and public bootstrap `{BOOTSTRAP_62}` remain historical resources for version-bound 6.2 work. Accepted-current Protocol 6.3 public fallback is exact bootstrap `{BOOTSTRAP}` and accepted recovery is separately `{REVIEW_RECOVERY}`; mapping-bearing generated reconciliation `{GENERATED}` passed Stage G acceptance in run `{STAGE_G_RUN}`.",
    )

    p = ROOT / "AGENTS.md"
    replace_once(
        p,
        "For Protocol 6.3 candidate work run the repository acceptance workflow documented in `README.md`/CI, including PEM validation/counterfactual tests, inherited and 6.3 qualification, package build/independent validation, committed-distribution parity, whitespace checks, frozen-resource integrity, and Orchestrator Core snapshot/tests when affected. Protocol 6.2 remains accepted-current until 6.3 completes its self-reference-safe bootstrap/profile/package, independent Review, recovery mapping, generated/Core parity, and lifecycle closeout. Never guess or self-declare a 6.3 public bootstrap/recovery SHA.",
        f"For Protocol 6.3 work run the repository acceptance workflow documented in `README.md`/CI, including PEM validation/counterfactual tests, inherited and 6.3 qualification, package build/independent validation, committed-distribution parity, whitespace checks, frozen-resource integrity, and Orchestrator Core snapshot/tests when affected. Protocol 6.3 is accepted-current with public bootstrap `{BOOTSTRAP}` and distinct recovery `{REVIEW_RECOVERY}`. Protocol 6.2 recovery `{BASE_62}` remains immutable historical rollback for version-bound 6.2 work. Never guess or self-declare a protocol bootstrap/recovery SHA.",
    )

    p = ROOT / "source/shared/references/development-workflow-prompts.md"
    replace_once(
        p,
        f"Recovery is separately mapped to `{REVIEW_RECOVERY}` after R2 Review PASS, but Protocol 6.2 remains accepted-current until Stage G generated reconciliation and lifecycle closeout pass.",
        f"Recovery is separately mapped to `{REVIEW_RECOVERY}` after R2 Review PASS. Mapping-bearing generated reconciliation `{GENERATED}` passed Stage G acceptance in run `{STAGE_G_RUN}`; Protocol 6.3 is accepted-current and Protocol 6.2 remains immutable historical rollback for version-bound 6.2 work.",
    )


def patch_semantic_dependencies() -> None:
    p = ROOT / "source/SEMANTIC_DEPENDENCIES.md"
    replace_once(p, "current Protocol 6.3 candidate", "current accepted Protocol 6.3")
    replace_once(
        p,
        "ssdp-protocol-6.2 CONSTRAINED_BY -> accepted-current Protocol 6.2 semantics\nssdp-protocol-6.3 CONSTRAINED_BY -> Protocol 6.3 candidate semantics until qualification/Review/recovery cutover",
        "ssdp-protocol-6.2 CONSTRAINED_BY -> immutable historical Protocol 6.2 rollback semantics\nssdp-protocol-6.3 CONSTRAINED_BY -> accepted-current Protocol 6.3 semantics",
    )
    replace_once(
        p,
        "Frozen 5.16/6.0/6.1/6.2 profiles remain independent compatibility/rollback resources during 6.3 implementation. Protocol 6.2 remains accepted-current until Protocol 6.3 completes qualification, immutable bootstrap/profile generation, independent Review, recovery mapping, generated-artifact/Core parity, and lifecycle closeout. Unsupported PEM schemas fail safe for memory-dependent decisions without breaking unrelated protocol routes.",
        "Frozen 5.16/6.0/6.1/6.2 profiles remain independent compatibility/rollback resources. Protocol 6.3 is accepted-current after qualification, immutable bootstrap/profile generation, independent Review R2, recovery mapping, generated-artifact/Core parity, Protocol 7 inheritance reconciliation, and lifecycle closeout. Unsupported PEM schemas fail safe for memory-dependent decisions without breaking unrelated protocol routes.",
    )


def write_revision4() -> None:
    if REV4.exists():
        raise RuntimeError(f"Revision 4 already exists: {REV4}")
    REV4.write_text(f'''---
kind: protocol-major-revision-workplan-amendment
workplan_id: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION
amends_workplan: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION
extends_amendment: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION
protocol_version: 6.3.0
target_protocol_version: 7.0.0
status: active
created_date: 2026-09-12
reconciliation_scope: project-learning-version-inheritance-only
d3_architecture_mutation: none
active_serious_challenge: none
---

# Protocol 7 Revision 4 — Protocol 6.3 Inheritance Reconciliation

## Background and authority boundary

This compact companion reconciles the active Protocol 7 handoff after acceptance of Scientific Software Development Protocol (SSDP) 6.3. It changes only the inherited document-controlled baseline, Protocol 6.3 project-learning contract, and compatibility/bootstrap/recovery identities. It does **not** alter or re-accept the deterministic-control-plane D3 architecture in the parent or Revisions 1-3 and does not authorize Protocol 7 D4 implementation.

Revision 4 has latest precedence only where earlier Protocol 7 artifacts describe Protocol 6.2 or an earlier release as the current document-controlled baseline/fallback. Every unrelated parent/Revision 1-3 requirement remains binding.

## 1. Accepted inherited baseline

```text
Protocol 6.3 semantic candidate -> {SEMANTIC}
Protocol 6.3 public bootstrap   -> {BOOTSTRAP}
Protocol 6.3 recovery           -> {REVIEW_RECOVERY}
Protocol 6.2 historical rollback -> {BASE_62}
```

Protocol 7 inherits all accepted Protocol 6.2 doctrine through 6.3 plus the accepted 6.3 project-learning strengthening: Project Engineering Memory (PEM) is evidence-backed project-local decision support, not D5; activation is conditional on material historical relevance; Historical Applicability Set (HAS) closure is task-local; stable family identity cannot launder semantic change; evidence/binding health and current authority remain independently governed; positive guidance requires discriminating evidence; summaries/temperature/maturity do not create authority or applicability.

## 2. What this reconciliation does not change

No Protocol 7 control-plane field, state transition, reducer rule, event schema, persistence contract, ownership boundary, recovery algorithm, cutover invariant, or D3 component identity changes merely because the inherited document-controlled baseline advanced from 6.2 to 6.3. Do not add a PEM registry, shadow control plane, compatibility wrapper, duplicate memory database, or machine field solely to mirror 6.3 project-learning doctrine.

If future Protocol 7 architecture cannot preserve an accepted 6.3 invariant, reopen the earliest affected D3 authority and resolve the contradiction there rather than patching D4 around it.

## 3. Pre-D4 gate disposition

```text
PROTOCOL 6.3 COMPLETION / QUALIFICATION / R2 REVIEW / RECOVERY: SATISFIED
PROTOCOL 6.3 INHERITANCE RECONCILIATION: SATISFIED BY THIS COMPANION
PROTOCOL 7 DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN / SUPERSESSION: STILL REQUIRED
PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED
```

The pre-existing deliberate D3 Orchestrator architecture reopen/supersession remains the next Protocol-7-specific gate. This revision neither performs that reopen nor converts any proposed Protocol 7 architecture into executable authority.

## 4. Compatibility, fallback, and cutover

Before qualified Protocol 7 cutover, the governing document-controlled fallback/rollback baseline is Protocol 6.3 recovery `{REVIEW_RECOVERY}`. Protocol 6.2 recovery `{BASE_62}` remains available only for explicitly version-bound historical 6.2 work.

Protocol 6.3 public fallback is exact bootstrap `{BOOTSTRAP}` and is intentionally distinct from recovery `{REVIEW_RECOVERY}`. Protocol 7 must preserve this distinction in later source-resolution/migration machinery.

No `main` merge or Protocol 7 cutover is implied by this reconciliation. Qualified Protocol 7 cutover remains separately governed by the composed parent/Revisions 1-4 handoff and still requires the outstanding D3 architecture reopen followed by D4, Review, qualification, recovery and cutover gates.

## 5. Handoff

Protocol 7 work SHALL read the parent plus Revisions 1-4 as one composed handoff. Where an earlier artifact names Protocol 6.2 or an earlier release as current pre-cutover document authority, read that statement as historical context superseded by Revision 4 for current work. All unrelated prior requirements remain unchanged.
''', encoding="utf-8")


def patch_authority_index() -> None:
    p = ROOT / "workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md"
    replace_once(p, "protocol_version: 6.2.0", "protocol_version: 6.3.0")
    replace_once(p, "reviewed_date: 2026-09-11", "reviewed_date: 2026-09-12")
    replace_once(p, "# SSDP 6.1 / 6.2 / 7.0 Workplan Authority Index", "# SSDP 6.1 / 6.2 / 6.3 / 7.0 Workplan Authority Index")
    marker = "## Protocol 7.0 current design handoff"
    text = p.read_text(encoding="utf-8")
    if marker not in text or "## Protocol 6.3 completed handoff" in text:
        raise RuntimeError("authority-index insertion anchor invalid")
    section = f'''## Protocol 6.3 completed handoff

Protocol 6.3 evidence-backed project-engineering-memory implementation, qualification, repaired bootstrap publication, independent Review R2, recovery, mapping-bearing regeneration, and Stage G closeout are complete. Its governing workplan is preserved as reviewed historical evidence at:

1. `workplans/archive/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md`

Current disposition:

```text
SERIOUS CHALLENGE: NONE
SEMANTIC CANDIDATE: {SEMANTIC}
PUBLIC BOOTSTRAP: {BOOTSTRAP}
BOOTSTRAP PUBLICATION DESCENDANT: {BOOTSTRAP_MAPPING}
QUALIFICATION: F5 + D9 repair + bootstrap/publication affected requalification PASS
INDEPENDENT REVIEW R2: PASS — qualification/ssdp6/FINAL-REVIEW-R2-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3.md
RECOVERY: {REVIEW_RECOVERY}
RECOVERY MAPPING COMMIT: {RECOVERY_MAPPING}
MAPPING-BEARING GENERATED COMMIT: {GENERATED}
STAGE G ACCEPTANCE: PASS — GITHUB ACTIONS RUN {STAGE_G_RUN}
LIFECYCLE STATUS: COMPLETED / ARCHIVED
PARENT ACCEPTED BASELINE: Protocol 6.2 recovery {BASE_62}
CURRENT ACCEPTED DOCUMENT-CONTROLLED BASELINE: Protocol 6.3
```

The public-source bootstrap and accepted recovery remain intentionally distinct. Historical invalidated 6.3 bootstrap/candidate attempts remain immutable negative evidence rather than current fallback. PEM remains non-authoritative project-local decision support; no D5 or parallel control plane was accepted.

'''
    p.write_text(text.replace(marker, section + marker, 1), encoding="utf-8")
    replace_once(
        p,
        "4. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md`",
        "4. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md`\n5. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md`",
    )
    replace_once(
        p,
        "- Revision 3 changes only representation/version inheritance after Protocol 6.2 acceptance: current pre-cutover document-controlled baseline and fallback/rollback become Protocol 6.2, while the parent/Revisions 1-2 D3 architecture semantics remain unchanged;\n- every parent requirement not explicitly changed by a later revision remains binding.",
        "- Revision 3 changes only representation/version inheritance after Protocol 6.2 acceptance: current pre-cutover document-controlled baseline and fallback/rollback became Protocol 6.2, while the parent/Revisions 1-2 D3 architecture semantics remained unchanged;\n- Revision 4 changes only project-learning/version inheritance after Protocol 6.3 acceptance: current pre-cutover document-controlled baseline and fallback/rollback become Protocol 6.3, while the parent/Revisions 1-3 D3 architecture semantics remain unchanged;\n- every parent requirement not explicitly changed by a later revision remains binding.",
    )
    replace_once(
        p,
        f"PROTOCOL 6.2 REPRESENTATION-INHERITANCE RECONCILIATION: SATISFIED\nCURRENT PRE-CUTOVER FALLBACK/ROLLBACK BASELINE: Protocol 6.2 recovery {BASE_62}",
        f"PROTOCOL 6.2 REPRESENTATION-INHERITANCE RECONCILIATION: SATISFIED\nPROTOCOL 6.3 COMPLETION/QUALIFICATION/R2-REVIEW/RECOVERY PREREQUISITE: SATISFIED\nPROTOCOL 6.3 INHERITANCE RECONCILIATION: SATISFIED\nCURRENT PRE-CUTOVER FALLBACK/ROLLBACK BASELINE: Protocol 6.3 recovery {REVIEW_RECOVERY}",
    )
    replace_once(
        p,
        "Revision 3 does not perform that reopen and no `main` cutover is implied.",
        "Revisions 3-4 do not perform that reopen and no `main` or Protocol 7 cutover is implied.",
    )
    replace_once(
        p,
        f"- Protocol 6.2 is the accepted-current document-controlled baseline; version-bound 6.1 work may still resolve immutable historical recovery `802e75af261efb4f70d71284d860613a2197b639`.\n- Protocol 7 remains proposed/pre-cutover. Its current fallback/rollback baseline is Protocol 6.2 recovery `{BASE_62}` until Protocol 7 itself completes the outstanding D3 architecture reopen and subsequent D4/Review/qualification/recovery/cutover gates.",
        f"- Protocol 6.3 is the accepted-current document-controlled baseline; version-bound 6.2 work may still resolve immutable historical recovery `{BASE_62}` and older declared versions retain their own mappings.\n- Protocol 7 remains proposed/pre-cutover. Its current fallback/rollback baseline is Protocol 6.3 recovery `{REVIEW_RECOVERY}` until Protocol 7 itself completes the outstanding D3 architecture reopen and subsequent D4/Review/qualification/recovery/cutover gates.",
    )
    replace_once(p, "No `main` merge/cutover is authorized by Protocol 6.2 closeout.", "No `main` merge or Protocol 7 cutover is authorized by Protocol 6.3 closeout.")


def patch_evidence_state() -> None:
    p = ROOT / "qualification/ssdp6/IMPLEMENTATION-STATE-PROTOCOL-6.3.md"
    p.write_text(f'''---
kind: ssdp63-implementation-state
protocol_version: 6.3.0
branch: ssdp-6.3-engineering-memory
authority: implementation-progress-evidence
status: stage-g-complete-accepted-current
accepted_current_protocol: 6.3.0
accepted_rollback_commit: {REVIEW_RECOVERY}
semantic_candidate: {SEMANTIC}
protocol_63_public_bootstrap: {BOOTSTRAP}
protocol_63_public_bootstrap_mapping: {BOOTSTRAP_MAPPING}
stage_f_static_sensor_commit: 092c784383868081e9dee2081e3895f3d1263630
stage_f_qualification_commit: 092c784383868081e9dee2081e3895f3d1263630
independent_review: r2_pass
independent_review_recovery_commit: {REVIEW_RECOVERY}
protocol_63_recovery: {REVIEW_RECOVERY}
protocol_63_recovery_mapping: {RECOVERY_MAPPING}
mapping_bearing_generated_commit: {GENERATED}
stage_g_acceptance_run: {STAGE_G_RUN}
---

# Protocol 6.3 Implementation State

## Current disposition

Protocol 6.3 lifecycle closeout is complete on the implementation branch. Semantic candidate `{SEMANTIC}` passed fresh independent Review R2 with zero blockers and zero Serious Challenges. The immutable R2 review commit `{REVIEW_RECOVERY}` is accepted Protocol 6.3 recovery; descendant `{RECOVERY_MAPPING}` publishes the recovery mapping. Public-source bootstrap `{BOOTSTRAP}` remains intentionally distinct and was published earlier by descendant `{BOOTSTRAP_MAPPING}`.

Mapping-bearing packages/profile/snapshot descendants were regenerated at `{GENERATED}`. GitHub Actions run `{STAGE_G_RUN}` passed repository regression, PEM validation, independent package validation and committed-distribution parity, Protocol snapshot parity, Orchestrator Core acceptance, recovery/bootstrap distinction, and whitespace checks before the generated reconciliation was committed.

Protocol 6.3 is accepted-current. Protocol 6.2 recovery `{BASE_62}` remains immutable historical rollback for explicitly version-bound 6.2 work. Protocol 7 inheritance is reconciled separately without modifying its D3 architecture or authorizing D4. No `main` merge is implied by this branch-local lifecycle closeout.

## Historical repair chain

Earlier F2/F3/F4/F5 candidates, qualification records, invalidated bootstrap attempts, and the pre-bootstrap-repair Review-PASS record remain immutable historical evidence. In particular F5 incorrectly conflated semantic candidate `{SEMANTIC}` with a replacement bootstrap even though that immutable candidate embedded historical D4R3 fallback `dc22f09fd38dbbfeaeb0160152da9b284654f66e`. Promotion review exposed the defect; the lifecycle was repaired by constructing and qualifying self-reference-safe bootstrap `{BOOTSTRAP}` before later publication, then performing fresh R2 Review and Stage G. Historical evidence is preserved rather than rewritten as if the earlier conclusion had been correct.
''', encoding="utf-8")

    p = ROOT / "qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md"
    replace_once(p, "status: bootstrap-repaired-evidence-reconciled-independent-review-r2-pending", "status: stage-g-complete-accepted-current")
    replace_once(
        p,
        "independent Review R2:                       PENDING\nProtocol 6.3 recovery:                       UNAVAILABLE",
        f"independent Review R2:                       PASS / recovery commit {REVIEW_RECOVERY}\nProtocol 6.3 recovery:                       {REVIEW_RECOVERY}\nrecovery mapping descendant:                 {RECOVERY_MAPPING}\nmapping-bearing generated descendant:        {GENERATED}\nStage G acceptance run:                       {STAGE_G_RUN}",
    )
    append_once(p, "## Stage G final disposition", f'''## Stage G final disposition

Independent Review R2 passed with zero blockers and zero Serious Challenges and is frozen at recovery commit `{REVIEW_RECOVERY}`. Descendant `{RECOVERY_MAPPING}` publishes the exact recovery mapping while keeping public bootstrap `{BOOTSTRAP}` distinct. Mapping-bearing generated descendant `{GENERATED}` passed the complete Stage G repository/PEM/package/dist/profile/Core/whitespace acceptance surface in GitHub Actions run `{STAGE_G_RUN}`.

The T01-T39 inherited preservation set and T40-T120 Protocol 6.3 extension remain closed without a discovered loss, scope/materiality laundering defect, priority inversion, false compaction, or frozen-resource mutation. Protocol 6.3 is accepted-current after current-authority/history/Protocol-7 reconciliation and workplan archival. Protocol 6.2 recovery `{BASE_62}` remains immutable historical rollback.''')

    close = ROOT / "qualification/ssdp6/STAGE-G-CLOSEOUT-PROTOCOL-6.3.md"
    if close.exists():
        raise RuntimeError("Stage G closeout evidence already exists")
    close.write_text(f'''---
kind: ssdp63-stage-g-closeout-evidence
protocol_version: 6.3.0
date: 2026-09-12
status: pass
semantic_candidate: {SEMANTIC}
public_source_bootstrap: {BOOTSTRAP}
public_source_mapping_commit: {BOOTSTRAP_MAPPING}
independent_review_r2_recovery: {REVIEW_RECOVERY}
recovery_mapping_commit: {RECOVERY_MAPPING}
mapping_bearing_generated_commit: {GENERATED}
stage_g_acceptance_run: {STAGE_G_RUN}
accepted_parent_recovery: {BASE_62}
blockers: 0
serious_challenges: 0
---

# Protocol 6.3 Stage G Closeout

**STAGE G: PASS.** Protocol 6.3 is accepted-current on the reviewed implementation branch after fresh R2 Review PASS, immutable recovery publication, mapping-bearing package/profile regeneration, and full Stage G acceptance.

The lifecycle identities are deliberately distinct:

```text
semantic candidate     -> {SEMANTIC}
public bootstrap       -> {BOOTSTRAP}
bootstrap publication  -> {BOOTSTRAP_MAPPING}
R2 review / recovery   -> {REVIEW_RECOVERY}
recovery mapping       -> {RECOVERY_MAPPING}
generated reconciliation -> {GENERATED}
```

GitHub Actions run `{STAGE_G_RUN}` passed full repository regression, self-hosted PEM validation, independent package validation, committed-distribution parity, Protocol snapshot parity, Orchestrator Core acceptance, recovery/bootstrap-distinction tests, and whitespace checks on the recovery-mapped assembled state before `{GENERATED}` was committed.

Current-authority, semantic-history, Protocol 7 inheritance, and authority-index surfaces are reconciled in the closeout descendant. The Protocol 6.3 workplan is archived byte-identically as historical cycle authority. Protocol 6.2 recovery `{BASE_62}` remains immutable historical rollback. No Protocol 7 D3 reopen, Protocol 7 D4 authorization, or `main` merge is implied.
''', encoding="utf-8")


def append_history() -> None:
    p = ROOT / "history/SEMANTIC_EVOLUTION.md"
    append_once(p, "## Protocol 6.2 -> Protocol 6.3", f'''## Protocol 6.2 -> Protocol 6.3

Protocol 6.3 adds evidence-backed Project Engineering Memory (PEM) as project-local non-authoritative decision support while preserving all accepted Protocol 6.2 doctrine and representation/routing capability.

- **Change:** project learning becomes an explicit evidence-backed representation for demonstrated failures, successes, discoveries, preserved capabilities, and current notices. Conditional Historical Applicability Set (HAS) use makes relevant history available for substantial mature rework, recurrence, scaling/optimization, migration/recovery/revert/restoration, without turning memory into a fifth authority domain.
- **Authority boundary:** D1-D4/current project/external owners remain authoritative. Temperature, maturity, repetition, summaries, tests, documentation, or PEM placement cannot self-promote a claim. Same-ID semantic change cannot be laundered through reconciliation; evidence/binding health and current owner applicability remain independently checked.
- **Semantic candidate:** `{SEMANTIC}`.
- **Bootstrap falsification and repair:** multiple earlier bootstrap attempts remain historical negative evidence. Promotion review additionally discovered that F5 had mislabeled `{SEMANTIC}` as replacement bootstrap although that immutable candidate still embedded D4R3 fallback `dc22f09fd38dbbfeaeb0160152da9b284654f66e`. Self-reference-safe bootstrap `{BOOTSTRAP}` was therefore constructed with 6.3 fallback unavailable, fully qualified, and only later named by publication descendant `{BOOTSTRAP_MAPPING}`.
- **Independent Review R2:** PASS with zero blockers and zero Serious Challenges; review/recovery commit `{REVIEW_RECOVERY}`. The four inherited Challenge dimensions—Loss, scope/materiality laundering, priority inversion, and false compaction—passed.
- **Recovery publication:** descendant `{RECOVERY_MAPPING}` publishes `6.3.0 -> {REVIEW_RECOVERY}` while keeping bootstrap `{BOOTSTRAP}` distinct.
- **Generated reconciliation and Stage G:** mapping-bearing packages/profile/snapshot descendants were regenerated at `{GENERATED}`. GitHub Actions run `{STAGE_G_RUN}` passed repository regression, PEM validation, independent package validation/parity, snapshot parity, Orchestrator Core, recovery/bootstrap distinction, and whitespace checks.
- **Protocol 7 reconciliation:** Revision 4 changes only inherited document-control/project-learning/version identities to accepted Protocol 6.3; it does not mutate the proposed Protocol 7 D3 architecture or authorize D4.
- **Lifecycle disposition:** COMPLETED / ARCHIVED. Protocol 6.3 is accepted-current; Protocol 6.2 recovery `{BASE_62}` remains immutable historical rollback for version-bound 6.2 work. Detailed failed-attempt chronology remains in qualification evidence and Git rather than being rewritten away.''')


def archive_workplan() -> None:
    if not ACTIVE_WP.exists():
        raise RuntimeError(f"active Protocol 6.3 workplan missing: {ACTIVE_WP}")
    if ARCHIVE_WP.exists():
        raise RuntimeError(f"archive Protocol 6.3 workplan already exists: {ARCHIVE_WP}")
    before = ACTIVE_WP.read_bytes()
    ARCHIVE_WP.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(ACTIVE_WP), str(ARCHIVE_WP))
    if ARCHIVE_WP.read_bytes() != before:
        raise RuntimeError("workplan archive move was not byte-identical")


def write_closeout_test() -> None:
    p = ROOT / "tests/test_protocol_63_closeout.py"
    if p.exists():
        raise RuntimeError("Protocol 6.3 closeout test already exists")
    p.write_text(f'''import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECOVERY = "{REVIEW_RECOVERY}"
BOOTSTRAP = "{BOOTSTRAP}"
BASE62 = "{BASE_62}"


class Protocol63CloseoutTests(unittest.TestCase):
    def test_accepted_current_and_identity_distinction(self) -> None:
        versioning = (ROOT / "source/shared/references/protocol-versioning-and-compatibility.md").read_text()
        portability = (ROOT / "PORTABILITY.md").read_text()
        readme = (ROOT / "README.md").read_text()
        self.assertIn("| `ssdp-protocol-6.3` | 6.3.0 | 2 | accepted current |", versioning)
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | frozen historical rollback |", versioning)
        self.assertIn(f"6.3.0  -> {{RECOVERY}}", versioning)
        self.assertIn(f"6.3.0 public bootstrap -> {{BOOTSTRAP}}", portability)
        self.assertIn(f"6.3.0 recovery -> {{RECOVERY}}", portability)
        self.assertNotEqual(RECOVERY, BOOTSTRAP)
        self.assertIn("Current accepted document-controlled release: **Protocol 6.3**", readme)
        self.assertIn(BASE62, readme)

    def test_workplan_archived_and_protocol7_inheritance_reconciled(self) -> None:
        active = ROOT / "workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md"
        archived = ROOT / "workplans/archive/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md"
        rev4 = ROOT / "workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md"
        self.assertFalse(active.exists())
        self.assertTrue(archived.is_file())
        text = rev4.read_text()
        self.assertIn("d3_architecture_mutation: none", text)
        self.assertIn("PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED", text)
        self.assertIn(f"Protocol 6.3 recovery           -> {{RECOVERY}}", text)

    def test_current_dependency_and_closeout_evidence(self) -> None:
        deps = (ROOT / "source/SEMANTIC_DEPENDENCIES.md").read_text()
        state = (ROOT / "qualification/ssdp6/IMPLEMENTATION-STATE-PROTOCOL-6.3.md").read_text()
        closeout = (ROOT / "qualification/ssdp6/STAGE-G-CLOSEOUT-PROTOCOL-6.3.md").read_text()
        self.assertIn("ssdp-protocol-6.3 CONSTRAINED_BY -> accepted-current Protocol 6.3 semantics", deps)
        self.assertIn("accepted_current_protocol: 6.3.0", state)
        self.assertIn(f"protocol_63_recovery: {{RECOVERY}}", state)
        self.assertIn("**STAGE G: PASS.**", closeout)


if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8")


def main() -> None:
    patch_versioning()
    patch_portability()
    patch_navigation()
    patch_semantic_dependencies()
    write_revision4()
    patch_authority_index()
    patch_evidence_state()
    append_history()
    archive_workplan()
    write_closeout_test()


if __name__ == "__main__":
    main()
