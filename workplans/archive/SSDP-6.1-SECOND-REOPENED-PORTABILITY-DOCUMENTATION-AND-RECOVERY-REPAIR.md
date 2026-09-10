---
kind: implementation-workplan
workplan_id: SSDP-6.1-SECOND-REOPENED-PORTABILITY-DOCUMENTATION-AND-RECOVERY-REPAIR
protocol_version: 6.1.0
status: active
created_date: 2026-09-10
reviewed_date: 2026-09-10
active_serious_challenge: none
---

# SSDP 6.1 Second Reopened Portability, Documentation, and Recovery Repair

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** uses four semantic authority domains: D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture, and D4 specification/implementation. A **concretization** is a lower-level expression of accepted authority; an **evidence realization** is a concrete execution of an evidence specification. A **semantic candidate** is the immutable Git commit whose Protocol behavior is under qualification. A **recovery identity** is an immutable Git commit that can restore the accepted Protocol 6.1 document-controlled/semi-automated system.

This workplan reopens only the bounded D4 packaging/portability, documentation, evidence-oracle, and lifecycle/recovery surface after a fresh post-closeout Review found three blockers. It does not change accepted D1/D2/D3 doctrine, create Protocol 7 machinery, or weaken any previously accepted Protocol 6.1 requirement.

## 1. Governing composed authority

Implementation and Review SHALL read this workplan together with the complete accepted Protocol 6.1 handoff:

1. `workplans/archive/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT.md`;
2. `workplans/archive/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT-REVISION-1-HUMAN-FACING-DOCUMENTATION-AND-FINAL-REVIEW-CLOSURE.md`;
3. `workplans/archive/SSDP-6.1-REOPENED-FINAL-REVIEW-REPAIR.md`;
4. this active repair workplan.

Every previously settled requirement remains binding unless this workplan explicitly clarifies the implementation mechanics required to satisfy it. The previously accepted semantic candidate `5f911fecb0de2847f63c0b4859e1dd8c63d3d8ef` and recovery snapshot `0c90fda19bf6ed9cb0c4511beb3da80ace6584ed` remain immutable historical evidence but are superseded for final Protocol 6.1 release/recovery authority by this reopen.

## 2. Reopen findings

### R2-1 — self-contained skill packages have dangling transitive Markdown routes

Current packaging derives bundle membership from direct `SKILL.md` routes. That design remains admissible and SHOULD be preserved because it keeps package membership explicit and bounded. However, packaged references may themselves contain local Markdown links. At least `documentation-and-evidence.md` routes to `scientific-technical-writing.md` while several bundles that include the former omit the latter. Current validation inspects only direct routes from `SKILL.md`, so package acceptance can remain green while an installed bundle contains a broken local reference.

Required end state:

- every local Markdown link contained by a shipped package resolves to a file present in that same package unless it is an external URI or an intentional same-document fragment;
- skills that materially route through `documentation-and-evidence.md` and can require the human-facing writing standard SHALL directly route `scientific-technical-writing.md`, preserving the current direct-membership model rather than adding a recursive build subsystem;
- package validation SHALL inspect local Markdown routes in every packaged `.md` resource, not only `SKILL.md`;
- a synthetic nested-dangling-route counterexample SHALL fail validation;
- current shipped bundles SHALL pass the strengthened closure check.

Expected owning surface includes `source/validate_packages.py`, D3/D4 role entrypoints, affected support-specialist entrypoints, package tests, and regenerated `dist/` artifacts. `source/build_skills.py` SHOULD remain direct-route driven unless implementation evidence proves that impossible.

### R2-2 — current Protocol 6.1 public fallback is not version-correct when repository default is 6.0

Current 6.1 workflow prompts name the canonical public repository but do not identify an immutable compatible 6.1 public-source ref. The repository default branch still exposes Protocol 6.0. Therefore a web agent following the advertised URL cannot both obey the no-version-substitution rule and reach current 6.1 source without out-of-band branch knowledge.

Required end state:

- current Protocol 6.1 public fallback SHALL identify an explicit immutable Git commit containing compatible 6.1 source and SHALL never depend on the repository default branch having already cut over;
- the current workflow prompt SHALL expose that immutable public-source ref explicitly and instruct current 6.1 fallback to read `source/` at that ref;
- current versioning guidance SHALL distinguish the immutable public-source bootstrap snapshot from historical 5.16/6.0 mappings and from later lifecycle/evidence commits;
- current portability guidance SHALL state the same mapping coherently;
- the oracle SHALL reject a current 6.1 prompt that merely names the repository URL while leaving the ref unresolved/default-branch dependent;
- add a behavioral qualification scenario that requires version-correct immutable fallback when the default branch is an incompatible protocol version.

Git commits cannot contain their own SHA. Therefore implementation SHALL use a two-step identity sequence rather than an impossible self-reference: first create an immutable repaired 6.1 public-source bootstrap snapshot containing all package/documentation fixes; then create the final semantic candidate whose current prompt/versioning/portability guidance explicitly points to that earlier immutable compatible snapshot. The final semantic candidate remains the subject of qualification; the bootstrap snapshot is a version-correct public source, not automatically the final recovery identity.

### R2-3 — the accepted human-facing background standard was not applied consistently to current Protocol-owned documents

Revision 1 already owns the rule; this workplan does not broaden it. The defect is incomplete concretization. Current Protocol-owned guides/entrypoints and the prior fresh qualification/Review records use project-specific terminology before sufficient background orientation.

Required end state:

- current Protocol 6.1 operator-facing entrypoints materially relying on SSDP-specific terms SHALL provide concise early `Background and terminology` context before substantive reasoning depends on those terms;
- at minimum reconcile root `README.md`, `source/README.md`, `PORTABILITY.md`, and current authority-bearing D1-D4 skill entrypoints; reconcile support-skill entrypoints where they introduce SSDP-specific concepts before an explicit supplied background route;
- do not turn skill entrypoints into textbooks or duplicate precise normative definitions; background definitions remain explanatory and point to canonical owners;
- do not rewrite the already committed prior qualification/Review records merely to hide their historical nonconformance. They become historical evidence after this reopen. New qualification and Review records for the repaired candidate SHALL themselves contain an early background/terminology section and obey first-use abbreviation rules;
- preserve release-pinned Protocol 5.x/6.0 bytes unchanged.

## 3. Frozen repair decisions and delegated implementation space

The following cycle-scoped decisions are fixed because they prevent recurrence without adding a new architecture:

1. Keep the existing direct `SKILL.md`-route package-membership model.
2. Strengthen validation across every packaged Markdown resource so local `.md` links must resolve inside the package.
3. Add missing direct writing-standard routes at affected skill entrypoints rather than recursively importing arbitrary reference graphs.
4. Use an immutable repaired 6.1 bootstrap commit for public-source fallback; never rely on `main`/repository-default state for current 6.1 resolution before cutover.
5. Preserve prior qualification/Review records as historical evidence; create fresh compliant evidence records for the new candidate.
6. Do not mutate frozen Protocol 5.16 or Protocol 6.0 profile/resource bytes.

Exact helper functions, test layout, wording compression, and temporary transport mechanics remain delegated D4 space. Temporary CI transport is permitted only when required by the web environment, must be tightly trigger-scoped, and must be removed from the final candidate tree.

## 4. Implementation sequence

### Stage A — reopen lifecycle and repair source/package/documentation ownership

1. Mark Protocol 6.1 lifecycle active/no-pass in the authority index and semantic-history current entry while retaining prior closeouts as historical evidence.
2. Add concise early background/terminology sections to the affected current 6.1 human-facing entrypoints/guides.
3. Add direct `scientific-technical-writing.md` routes to every current skill that directly packages `documentation-and-evidence.md` but otherwise leaves that local dependency unresolved.
4. Strengthen `source/validate_packages.py` to validate local Markdown-link closure for every packaged Markdown file.
5. Add focused regression tests proving both positive package closure and a known-broken nested dangling route.
6. Regenerate all affected skill directories/ZIPs from canonical `source/` and run repository/package/orchestrator acceptance.
7. Commit this accepted stage as the immutable 6.1 public-source bootstrap snapshot.

### Stage B — bind current public fallback to the immutable repaired bootstrap snapshot

1. Update current `development-workflow-prompts.md` so Protocol 6.1 public fallback explicitly uses the Stage-A immutable commit and never repository-default source implicitly.
2. Update canonical `protocol-versioning-and-compatibility.md`, `PORTABILITY.md`, and current README/routing prose coherently.
3. Strengthen the static oracle so a repository URL without the immutable current-6.1 fallback ref is insufficient.
4. Add scenario 95 covering an incompatible default branch with correct immutable 6.1 public fallback.
5. Regenerate affected skill packages and the current `ssdp-protocol-6.1` Orchestrator snapshot/profile from canonical source.
6. Run complete repository regression, canonical package build, package validation, committed-dist parity, whitespace, Protocol snapshot parity, and Orchestrator Core acceptance.
7. Remove any temporary CI/transport workflow before freezing the semantic candidate.

### Stage C — fresh qualification and independent Review

1. Execute/reassess all 95 Protocol 6.1 behavioral scenarios against the final semantic candidate; old 94/94 evidence is historical only for this closeout.
2. Record a new human-facing qualification report with concise Background/terminology context and explicit candidate/evidence provenance.
3. Perform a fresh independent D3 Review using Protocol 6.1 itself. Review SHALL directly falsify nested package-reference closure, immutable public fallback, current documentation-standard conformance, frozen 6.0 compatibility, and generated-source parity.
4. No final recovery closeout is authorized with an active Serious Challenge or open blocker.

### Stage D — replacement recovery and closeout

After Stage C PASS:

1. establish an immutable replacement Protocol 6.1 recovery commit containing the accepted semantic candidate and admissible qualification/Review evidence needed for rollback interpretation;
2. publish that exact recovery SHA in current `protocol-versioning-and-compatibility.md` and `PORTABILITY.md` using a later mapping-only current-source commit; because an immutable commit cannot self-name, the recovery target itself need not contain its own SHA;
3. regenerate packages affected by the mapping-only canonical-source update and rerun package/parity plus targeted version/recovery tests;
4. update semantic history and the 6.1/7.0 authority index, archive this workplan, and mark the Protocol 7 recovery prerequisite satisfied only after the mapping-only closeout is verified;
5. preserve every earlier recovery candidate as immutable historical evidence, never as the final accepted rollback baseline.

## 5. Acceptance boundaries and counterfactuals

Protocol 6.1 remains NO-PASS until all of the following are true:

- **Package closure:** deleting `scientific-technical-writing.md` from a bundle that contains a local link to it makes package validation fail.
- **Nested-link oracle:** a synthetic packaged reference containing `[x](missing.md)` fails even when `SKILL.md` itself has no dangling direct route.
- **Direct-membership discipline:** current shipped resources remain intentionally routed from skill entrypoints; validation does not silently turn every shared reference into package payload.
- **Public fallback:** if the repository default branch exposes Protocol 6.0, current 6.1 fallback still resolves the explicit immutable 6.1 public-source commit and never silently substitutes 6.0.
- **Versioning guidance:** current protocol versioning and portability guidance coherently identify the accepted immutable public-source/recovery identities at the appropriate lifecycle stage.
- **Human-facing conformance:** newly current/revised Protocol-owned guides, role entrypoints, qualification report, and final Review define necessary SSDP-specific terminology before relying on it; non-obvious abbreviations follow first-use expansion.
- **Historical preservation:** frozen 5.16 and 6.0 profile/resource bytes remain unchanged.
- **Generated-source integrity:** `dist/` and current Orchestrator profile/snapshot are regenerated from canonical source and pass parity; no hand-edited generated descendant remains.
- **Executable acceptance:** full repository regression, package build/validation/parity, whitespace, Protocol snapshot parity, and Orchestrator Core acceptance all execute successfully on the final candidate or remain explicitly blocking.
- **Behavioral qualification:** 95/95 fresh PASS with no Serious Challenge.
- **Independent Review:** fresh PASS with zero open blocking findings.
- **Lifecycle:** this workplan is archived only after the replacement recovery mapping is verified.

## 6. Non-goals

- No Protocol 7 TaskEnvelope/ResultEnvelope/control-plane machinery.
- No mandatory recursive package builder, graph database, universal documentation glossary, or package manifest expansion solely for symmetry.
- No merge to `main` unless separately authorized or performed through the repository's normal release process.
- No rewriting of historical 5.x/6.0 artifacts or prior qualification/Review reports merely to make history look clean.
- No broad semantic rename of retained opaque compatibility paths.

## 7. Reopened disposition

```text
SERIOUS CHALLENGE: NONE
REOPEN FINDINGS: 3 BLOCKING
D1/D2/D3 SEMANTIC AUTHORITY CHANGE: NONE
IMPLEMENTATION AUTHORIZED: YES — BOUNDED D4/DOCUMENTATION/PORTABILITY REPAIR
PROTOCOL 6.1 LIFECYCLE: ACTIVE / NO-PASS
PROTOCOL 7 RECOVERY PREREQUISITE: REOPENED / UNSATISFIED
```
