---
kind: protocol-stage-evidence
authority: non-normative-evidence
governing_workplan: SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION
governing_protocol_version: 6.5.0
target_protocol_version: 6.6.0
stage: A
---

# Protocol 6.6 Stage A — Baseline, Memory Basis, Preservation Map, Evaluation Freeze

Evidence coordination for the Stage A gate. It is not D1-D4 authority, a semantic registry, or a release-state owner; current release identities resolve only from [`PROTOCOL-RELEASE-STATE.yaml`](../../PROTOCOL-RELEASE-STATE.yaml).

## 1. Gate disposition

```text
STAGE A GATE: CLOSED (reviewable)
SERIOUS CHALLENGE: NONE
memory basis: reconciled (accepted 6.5 integrated state); canonical HAS recorded below
preservation map: recorded (section 4); maintained through Stage G
baselines: bound at both layers (section 3); static + live probes recorded (section 5)
evaluation basis: frozen before semantic-source mutation (section 6)
```

## 2. Frozen identities

| Role | Identity |
| --- | --- |
| accepted 6.5 canonical semantic source | `7f7b5e24858e813e45ace867a7f8ea5180f43bf0` |
| accepted 6.5 recovery | `c4d5da1e0acb0e9f27376bf69561e8762747cd2d` |
| accepted-current cutover / generated package baseline | `2b8ce17b1f086dc85e6fa8014c4a7bcc45ef60cb` |
| branch base (accepted integrated state on `main`) | `23e46543c174a8451bbadc402df63538105eab10` |
| reviewed workplan head entering implementation | `5a93d12bb702d25235f15c401f32b7192c45145f` |

Canonical `source/` is byte-identical between `7f7b5e2` and `23e4654` (`git diff 7f7b5e2 23e4654 -- source/` is empty), so the branch base carries exactly the accepted 6.5 semantic source.

Inherited acceptance at the branch head before any Stage B edit: `release_state.py` coherent; PEM valid; 352 repository tests OK (3 skipped: remote/CI-only); package build + independent validation + committed-dist parity OK; Orchestrator snapshot check OK; 382 Core tests OK. The container clone was initially shallow; historical refs were made resolvable by unshallowing before those checks (a shallow clone fails release-state/PEM ancestry closed, as designed).

## 3. Two-layer behavioral baseline binding

- **Semantic/source comparisons** read canonical source at `7f7b5e2` (`harness.py static --ref 7f7b5e2…`).
- **Discovery/selection/runtime-package comparisons** install `dist/skills` exported from cutover `2b8ce17` (`git archive 2b8ce17 dist/skills`); its bundles declare `PROTOCOL_VERSION` `6.5.0`. No locally installed approximation or mutable default branch is used.

## 4. Project Engineering Memory basis and HAS

### Reconciliation

The workplan entered with `accepted_pem: REVIEW_REQUIRED` because the root PEM front matter still named Protocol 6.4 P0 (`55c0852`) as accepted base plus a 6.5 candidate overlay although 6.5 is accepted-current.

Resolution under accepted 6.5 governance (not by guessing from `main`/latest):

1. The PEM bytes at `23e4654` are identical to those in reviewed (P21 PASS) and ratified semantic candidate `7f7b5e2`; the 6.5 overlay therefore passed that candidate's Review/ratification and was integrated unchanged through accepted cutover `2b8ce17`.
2. This repository's project-local policy (`AGENTS.md`) designates `main` as the integrated publication line for accepted/base memory; `23e4654` is on `main` and descends from the cutover.
3. Advancing `accepted_base.project_state` to `23e4654` correctly broke `PC-001`'s `AUTHORITY_BOUND` binding (owner route cited `55c0852`, whose `protocol-versioning-and-compatibility.md` changed in 6.5). The accepted 6.5 owner still requires the capability ("When a new profile becomes current, every older supported profile remains frozen and independently testable"), so the binding was remapped to the unchanged accepted owner at `7f7b5e2` rather than silently kept.

The branch overlay is limited to that front-matter reconciliation and PC-001 remap; it self-ratifies nothing. `project_engineering_memory.py` validates it (5 families, 0 notices).

### Canonical HAS

```yaml
pem_basis:
  accepted_project_state: 23e46543c174a8451bbadc402df63538105eab10
  accepted_pem: 23e46543c174a8451bbadc402df63538105eab10
  candidate_overlay_semantic_candidate: ssdp-6.6-cognitive-operational-optimization
has:
  - id: FF-001
    disposition: APPLICABLE
    reason: 6.6 will need a successor public-source fallback; publication must wait until the frozen candidate contains every repaired route. Out of implementation scope (Stage H) but constrains closeout.
  - id: PC-001
    disposition: APPLICABLE
    reason: 6.6 adds a current profile/snapshot; the 6.5 prompts/profile bytes must be frozen with blob-hash oracles and every older frozen tree kept byte-identical.
  - id: SP-001
    disposition: APPLICABLE
    reason: every routing/representation change is made at canonical source owners and descendants (dist, Orchestrator snapshot) are regenerated, never hand-patched.
  - id: SP-002
    disposition: APPLICABLE
    reason: retain candidate -> descendant publication -> distinct recovery; ordinary implementation freezes nothing and publishes no identity.
  - id: DS-001
    disposition: APPLICABLE
    reason: structural/static fixtures and harness counts may claim only the property their oracle discriminates; semantic preservation needs independent Review, behavioral claims need live evidence.
```

## 5. Baseline measurements

Tool: [`eval/harness.py`](eval/harness.py) (removable evidence tooling). Raw output: [`eval/results/static-baseline-6.5.json`](eval/results/static-baseline-6.5.json).

### Layer 0 — catalog metadata (static)

Seven frontmatter blocks: 2,230 bytes (~385 token-proxy); seven `agents/openai.yaml` adapters: 913 bytes. Static inspection cannot establish live selection.

### Layer 1 — declared mandatory-read closure after root selection

| Route | Root | Mandatory (bytes) | Route closure incl. fired concerns (bytes) |
| --- | --- | ---: | ---: |
| R1 local D4 repair | software-implementation | 38,187 | 38,187 |
| R2 D4 with workplan + tests | software-implementation | 38,187 | 72,996 |
| R3 D3 mature replacement (PEM) | software-design | 42,030 | 102,594 |
| R4 D2 specialized import | numerical-algorithm-design | 36,100 | 36,100 (definition detail already inside the 22.6 KB kernel) |
| R5 D1 parameter/default binding (holdout) | scientific-formulation | 35,569 | 52,397 |
| R6 memory-governance update (holdout) | software-maintenance-audit | 33,456 | 61,189 |

The universal kernel (`abstraction-and-concretization.md`, 22,622 bytes) is ~59% of every local-route mandatory closure; about 6.5 KB of it is specialized semantic-definition detail and ~5.5 KB detailed representation/routing rules.

### Layers 2-3 — live probes (Claude Code 2.1.283 headless, `claude-sonnet-5`, project-installed skills)

- Selection probe (S04 local bug, no explicit skill): no SSDP skill invoked within 3 turns; the ambient catalog also exposes ~30 non-SSDP skills (identical across variants; recorded confounder).
- Trajectory probe T1 without explicit skill: fixed correctly (hidden oracle OK), no SSDP activation.
- Trajectory probe T1 with "Use the software-implementation skill.": skill invoked; **zero reference files read** although the 6.5 entrypoint says to read the kernel and D4 owner "before substantive D4 implementation"; oracle OK; 7 turns, 212,861 input tokens incl. cache, $0.094.

Reduced traces/summaries: [`eval/results/stageA/`](eval/results/stageA/). Runs strip the invoking session's session/ingress environment so each evaluation run is an isolated session.

Interpretation (bounded to this harness/model/install mode): for trivial local work the observed protocol context is essentially the injected `SKILL.md`; the 38 KB declared mandatory closure is not honored. Two consequences for design: `SKILL.md` size is the dominant *observed* context term on ordinary routes, and a declared mandatory read that is too large to be honored is a hidden-constraint-loss risk rather than a protection. Stage F therefore measures mandatory-read compliance as well as bytes.

## 6. Frozen evaluation basis

Corpus: [`eval/scenarios.yaml`](eval/scenarios.yaml) with fixtures in [`eval/fixtures/`](eval/fixtures/) and hidden oracles in [`eval/oracles/`](eval/oracles/), frozen by the commit that introduces this file (before any `source/` mutation).

- selection: 11 development (clear D1-D4, three specialists, one mixed admissible set, two negatives, one explicit request) + 5 holdout (mixed D2/D4/D3 admissible set, D1, D4, negative, hygiene/implementation admissible set);
- routes: 4 development + 2 holdout post-selection activation expectations (`fires`/`forbid`);
- trajectories: T1 first-clean local repair, T2 tolerance within documented envelope (development); T3 D2-owned parameter default, T4 Protocol-6.4-bound workplan (holdout).

Claim boundaries: layer 0/2/3 claims bind to Claude Code headless / `claude-sonnet-5` / project-skill install mode as exercised; other harnesses are unqualified. Trajectory correctness uses deterministic hidden oracles plus a separate blinded assessor context; execution-agent completion claims never count. Development cases may be used for repair; a holdout used for tuning is reclassified in the results file.

## 7. Capability-preservation map

Organized by capability family. "6.6 owner/route" is the planned destination; Stage G re-verifies every row against the assembled candidate. `sentinel` names the executable or review check that must still discriminate loss.

| Family (origin) | 6.5 owner | 6.5 activation | 6.6 owner / activation route | Sentinel |
| --- | --- | --- | --- | --- |
| D1-D4 ownership, earliest affected owner, DAG not waterfall (6.0) | kernel + domain refs | always | kernel (kept) | 6.4/6.2 routing tests; R1-R6 |
| abstraction/concretization, fidelity vs adequacy (6.0/6.1) | kernel | always | kernel (kept, compact) | kernel sentinel test |
| authority vs evidence vs delegated machinery; mechanism gains no authority (5.14/6.0) | kernel | always | kernel | stewardship tests |
| materiality definition (6.2) | kernel | always | kernel | kernel sentinel test |
| feasibility > simplicity > economy; minimum justified complexity; local-first repair (5.14) | kernel + convergence | always / recurrence | unchanged split | 5.12/5.14 tests |
| Challenge Pass / Serious Challenge threshold; human adjudication; risk-accepted provisional descendants (6.0) | kernel + workflow + prompts | always | kernel keeps threshold + provisional rule; mutation pipeline/lifecycle states move to workflow (authority mutation predicate) | Serious Challenge tests; 516 orchestration footer test |
| lifecycle state distinctions; authority-mutation acceptance sequence (6.0) | kernel | always | workflow (fires on authority mutation/acceptance) | new 6.6 routing test |
| proportional rigor, importance ≠ priority, escalation/stop (6.5) | kernel + convergence + workflow | always / substantial | kernel principle; convergence detail (unchanged) | 6.5 proportional-rigor tests |
| evidence spec→realization→observation→assessment, staleness, target-vs-execution, common mode (6.1) | evidence ref + testing | evidence predicate | unchanged | 6.1 tests |
| real-owner/proxy-proof acceptance; required unexecuted checks block (5.6) | D4 SKILL + testing | D4 | unchanged (D4 SKILL keeps micro-invariant) | proxy-proof tests |
| Lossless Representation protected property + preference order (6.2) | kernel | always | kernel (compact) | 6.2 kernel phrase sentinel |
| typed activation, routing hop rules, context reuse validity, derived-view subordination (6.2) | kernel | always | kernel (compact rules retained) | 6.2 tests + new activation-boundary tests |
| progressive disclosure; package membership ≠ activation; transport closure (6.1/6.2) | kernel + build/validate | always / build | unchanged + new 6.6 discovery/transport/activation separation tests | package closure tests |
| semantic-definition: source vs context availability, formal well-definedness, parameter family/instance/default, import/hypothesis propagation, definition ≠ warrant, `USES_DEFINITION` direction (6.4) | kernel (always hot) + workflow + prompts | always | **new conditional owner** `semantic-definition-and-traceability.md` (risk-triggered router); kernel keeps the hard invariant `infer -> context_available -> source_available` and the trigger | R4/R5 sentinels; T3 holdout; 6.4 tests retargeted to the new owner |
| PEM non-D5; classification gives no force (6.3) | kernel + PEM ref | always / PEM predicate | kernel one-liner + PEM agent-facing contract | 6.3 tests |
| PEM activation predicate, retrieval, HAS, applicability regardless of temperature, missing ≠ absence (6.3) | workflow + intake + PEM + prompts + every role | PEM predicate | **one** agent-facing owner `project-engineering-memory.md`; others route | R3 sentinel; HAS validator tests |
| PEM schema-1, occurrences/applications, maturity, assessments, bindings, statistics, summary, notices, overlays, fork/rollback (6.3/6.5) | PEM ref | PEM predicate | **cold** `project-engineering-memory-schema.md`, dispatched only for memory-governance questions | PEM validator + schema-parity tests (retargeted); R6 holdout |
| closeout-learning assessment (6.3) | workflow + PEM | closeout | PEM agent-facing contract (update threshold); workflow routes | 6.3 closeout tests |
| compact working state / resumability (6.2/6.5) | workflow §handoff | long work | workflow (same owner, operationalized: minimum fields, staleness, non-authority) | new negative tests |
| workplan contract vs transient progress (6.5) | workflow | workplan | workflow (explicit "when a workplan changes") | new test |
| convergence/recurrence/family, review saturation, revision economy (5.12) | convergence | recurrence | convergence + strategy switch after related repeated findings | 5.12 tests |
| independent Review, out-of-matrix adequacy pass (6.5) | workflow + prompts | Review | workflow + optional independent-trajectory predicates and common-mode limits | 6.5 tests; new tests |
| version-bound interpretation, exact source resolution, no default/latest (5.16/6.2/6.5) | versioning + prompts | version predicate | versioning owner + cheap entry handshake in kernel + `source/version_preflight.py` helper | new E tests; 6.2/6.5 exact-ref tests |
| release-state ownership outside immutable source (6.5) | release_state.py + versioning | release | unchanged | 6.5 release-state tests |
| frozen historical profiles/resources, Core parity, Protocol 7 isolation (6.4/6.5; PC-001) | versioning + Core | release | 6.5 prompts/profile frozen by blob hash; 6.6 profile reuses the schema-v2 stage table/transitions unchanged | Core frozen-profile tests |
| tool/language routing, relation-first analyzers (5.11/5.13/5.15) | tool/language routers | predicate | unchanged; cognitive-resource escalation lives with the rigor owner (`convergence-and-cycle-economy.md`); the tool owner only routes to it | 5.13/5.15 tests |
| documentation, writing background/abbreviation rules (6.1) | writing/doc owners | doc predicate | unchanged | 6.1 tests |
| security/trust; evidence text inert (5.x/6.4) | security + kernel | always / predicate | kernel one-liner kept | security tests |
| generic Agent-Skills validity vs vendor adapter (5.9/6.1) | validate_packages + adapters | build | unchanged; new test that adapter absence does not invalidate generic core | new test |
| manual/portable operation without Orchestrator (5.16/6.2) | prompts + PORTABILITY | always | prompts kept complete; no hidden state | 516 orchestration tests |

No row is planned for deletion. Any row whose Stage G disposition is not PRESERVED/GENERALIZED blocks Review readiness.
