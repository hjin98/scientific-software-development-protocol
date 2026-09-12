from pathlib import Path
import re

candidate = "3bbbdfa8120646d76336c7b916e6a891c9ed38f2"
baseline = "b59adc77efe6951912cfd705cc43830c58ca27d0"
baseline_candidate = "ebbc4591bdfed039512026b8acb3a6749475c1c5"
baseline_bootstrap = "5a062ebc472755607b9dc66d33a5ebbc4b7429aa"
bootstrap = "e12572c021087308570abfa41657a910c6896457"
mapping = "e6a8c12f065c3d25a41da804c129d6bc0a4f7b50"
f2_commit = "6fc26ce374b5346495782871d5d7241de5b90071"
f2_report = "qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F2.md"

# Workplan: retain the NO-PASS review as history, close the implementation repairs,
# and leave only the independent Review / Stage-G lifecycle gate open.
p = Path("workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md")
text = p.read_text(encoding="utf-8")
text = text.replace("implementation_review_state: reopened-no-pass", "implementation_review_state: repaired-qualified-independent-review-pending", 1)
text = text.replace("reopened_stages: D,E,F", "reopened_stages: none", 1)
text = text.replace(
    "stage_g_recovery_gate: blocked-pending-repair-requalification-independent-review",
    "stage_g_recovery_gate: blocked-pending-independent-review",
    1,
)
anchor = "reviewed_candidate_no_pass: 100cbde296de6c1a8db14151f34cfacfebc90eb3\n"
addition = (
    f"qualified_semantic_candidate: {candidate}\n"
    f"f2_qualification_commit: {f2_commit}\n"
    f"f2_qualification: {f2_report}\n"
)
if addition not in text:
    if anchor not in text:
        raise SystemExit("workplan frontmatter anchor missing")
    text = text.replace(anchor, anchor + addition, 1)

h17 = "### 17.1 Current Protocol 6.3 implementation-review repair contract"
d4 = "#### Repair D4R2 - acceptance evidence must establish acceptance of the same repair"
if h17 not in text or d4 not in text:
    raise SystemExit("workplan repair-contract anchors missing")
repair_preamble = f'''### 17.1 Completed Protocol 6.3 implementation-review repair contract

The Protocol 6.2-governed assembled-candidate Review of branch state `100cbde296de6c1a8db14151f34cfacfebc90eb3` was **NO-PASS** with **no Serious Challenge** to accepted Protocol 6.2 authority or the Protocol 6.3 D3 design contract. That Review opened D4R2, D5R2, E2, and F2 while preserving the repaired D1 binding-health, D2 logical-publication, D3 observation-identity, D6 typed-notice, and D7 HAS/template behavior.

Those implementation-context repairs are now closed by immutable semantic candidate `{candidate}` and fresh F2 evidence `{f2_commit}` / `{f2_report}`. D4R2 binds accepted-repair evidence to the exact repair subject, explicit accepted state, and accepting owner; D5R2 derives replication and independent-replication obligations for every schema-1 `PROVEN SUCCESS_PATTERN` rather than trusting claimant omission. E2 publishes self-reference-safe bootstrap `{bootstrap}` only through later mapping descendant `{mapping}`. F2 freshly accounts for all 260 required inherited/Q63/F63/Challenge cases and reruns the assembled source/package/profile/Core/frozen-resource gates.

Earlier 6.3 candidates, bootstraps, mappings, and Stage-F result sets remain immutable historical evidence only. They remain useful falsification fixtures but are not current acceptance anchors. The repair specifications below are retained as the auditable contract that the current candidate was required to satisfy; they are no longer open implementation blockers. Stage G remains blocked on the fresh independent assembled-candidate Review and the separate recovery lifecycle.

'''
text = text[:text.index(h17)] + repair_preamble + text[text.index(d4):]

h18 = "## 18. Current design closure state"
h19 = "## 19. Intended end state"
if h18 not in text or h19 not in text:
    raise SystemExit("workplan current-state anchors missing")
sec18 = f'''## 18. Current design closure state

This is the current-state workplan contract. Detailed NO-PASS chronology and the completed D4R2/D5R2/E2/F2 repair specification remain in §17.1 and qualification records as non-authoritative historical/audit evidence.

No Serious Challenge is active. The final immutable implementation semantic candidate is `{candidate}`. D1/D2/D3/D6/D7 remain preserved and reverified; D4R2 and D5R2 are implementation-context closed; E2 is closed through exact public bootstrap `{bootstrap}` and later mapping `{mapping}`; F2 is closed by candidate-bound 260/260 evidence `{f2_commit}` / `{f2_report}` plus the assembled source/package/profile/Core/frozen-resource gates.

The only remaining Stage-F lifecycle gate is a **fresh independent assembled-candidate Protocol/D3 Review**. Implementation-context qualification is evidence to challenge, not authority. Protocol 6.3 remains proposed; Stage G, recovery, accepted-current status, workplan archive, and `main` cutover remain blocked until that independent Review passes and the separate recovery lifecycle is completed.

The intended design remains evidence-backed project-local memory with non-authoritative evidence, exact durable warrants, immutable observations, stable semantic identity, provenance-aware application episodes, claim-relative maturity, actual accepted-repair recurrence rather than chronology inference, one HAS/overlay interface, basis-bound notices, atomic publication, and lossless progressive disclosure.
'''
text = text[:text.index(h18)] + sec18 + "\n\n" + text[text.index(h19):]
p.write_text(text, encoding="utf-8")

# Implementation state: exact final chain, with recovery/acceptance explicitly unavailable.
p = Path("qualification/ssdp6/IMPLEMENTATION-STATE-PROTOCOL-6.3.md")
p.write_text(f'''---
kind: ssdp63-implementation-state
protocol_version: 6.3.0
branch: ssdp-6.3-engineering-memory
authority: implementation-progress-evidence
status: f2-implementation-qualification-complete-independent-review-pending
accepted_current_protocol: 6.2.0
accepted_rollback_commit: {baseline}
semantic_candidate: {candidate}
protocol_63_public_bootstrap: {bootstrap}
protocol_63_public_bootstrap_mapping: {mapping}
stage_f_static_sensor_commit: {f2_commit}
stage_f_qualification_commit: {f2_commit}
stage_f_qualification: {f2_report}
independent_review: pending_fresh_context
protocol_63_recovery: unavailable_pending_independent_review
---

# Protocol 6.3 Implementation State

## Current disposition

Protocol 6.3 implementation-context repair and F2 qualification are complete for immutable semantic candidate `{candidate}`. Protocol 6.2 remains accepted-current at recovery `{baseline}`. This record does **not** claim independent Review PASS, Protocol 6.3 recovery, lifecycle acceptance, workplan closure, or `main` cutover.

The earlier 6.3 chains ending at `8d0ad239...` and `7f677415...`, their bootstraps/mappings, and their Stage-F reports remain immutable historical evidence only. Branch state `100cbde...` is the reviewed NO-PASS state that opened D4R2/D5R2/E2/F2. None is a current acceptance anchor.

## Owner-layer repair closure

- **D1/D2/D3/D6/D7:** preserved from the reviewed repaired baseline and reverified by the final assembled regression.
- **D4R2 accepted-repair recurrence:** acceptance evidence is typed content bound to the exact repair identity, explicit `ACCEPTED` state, and accepting owner. An unrelated descendant route, wrong repair subject, missing state/owner, reversed chronology, or copied/rebased alias cannot manufacture recurrence.
- **D5R2 maturity/independence:** every schema-1 `PROVEN SUCCESS_PATTERN` derives replication and independent-replication obligations. Claimant omission or false `requires_*` flags cannot waive those obligations, and common provenance cannot count as independent confirmation.

## Replacement bootstrap lifecycle

The current repaired public-source chain is:

```text
self-reference-safe immutable source snapshot: {bootstrap}
later public mapping descendant:               {mapping}
final implementation semantic candidate:       {candidate}
```

The bootstrap snapshot existed and passed readiness before its SHA was published. The later mapping descendant published that exact immutable SHA, exact-ref public realization passed, and subsequent semantic reconciliation preserved the inherited self-reference-safe source-resolution capability. The public bootstrap is version-bound fallback only; it is not recovery or accepted-current state.

## F2 qualification

Fresh implementation-context evidence is `{f2_report}` at commit `{f2_commit}`. It records **260/260** exact case dispositions: 115 inherited Protocol 6.2 scenarios, 79 Q63 scenarios, 62 F63 adversarial cases, and four inherited Challenge passes. High-risk mechanical rows bind executable discriminators; semantic rows bind the exact paired counterfactual, governing owner, and fresh assembled-candidate falsification assessment.

The same pass reran self-hosted PEM validation; D1-D7 focused tests; Protocol 6.3 engineering-memory tests; exact public-bootstrap tests; inherited Protocol 5.16 orchestration; full repository regression; canonical build/package/dist validation; Protocol 6.3 snapshot/profile parity; Orchestrator Core acceptance; whitespace; exact fallback realization; and frozen 5.16/6.0/6.1/6.2 resource comparisons.

Static activation evidence was rebound at `{f2_commit}` to exact candidate `{candidate}` with active-set topology preserved and byte totals recomputed. It remains structural evidence only, not a live token/latency/attention/productivity claim.

## Independent Review boundary

The next required gate is a **fresh independent assembled-candidate Protocol/D3 Review** of `{candidate}` against accepted Protocol 6.2 recovery `{baseline}` and the active workplan. The reviewer must reconstruct the candidate and attempt falsification rather than inheriting this file, green CI, or the 260/260 result as authority.

Until that Review passes:

```text
Stages A-F implementation context: COMPLETE
Independent assembled-candidate Review: PENDING
Protocol 6.3 recovery: UNAVAILABLE
Stage G: BLOCKED
Accepted-current protocol: 6.2.0
Workplan: ACTIVE
Main cutover: NOT AUTHORIZED
```
''', encoding="utf-8")

# Independent handoff: current immutable identities only, with explicit falsification attacks.
p = Path("qualification/ssdp6/INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.3.md")
p.write_text(f'''---
kind: ssdp63-independent-review-handoff
protocol_version: 6.3.0
authority: non-normative-review-handoff
semantic_candidate: {candidate}
qualification_result_commit: {f2_commit}
qualification_result: {f2_report}
static_sensor_evidence_commit: {f2_commit}
public_source_bootstrap: {bootstrap}
public_source_mapping_commit: {mapping}
accepted_protocol_62_recovery: {baseline}
accepted_protocol_62_public_bootstrap: {baseline_bootstrap}
accepted_protocol_62_semantic_candidate: {baseline_candidate}
independent_review: required_fresh_context
protocol_63_recovery: unavailable_pending_review
accepted_current_protocol: 6.2.0
---

# Independent Protocol/D3 Review Handoff — Protocol 6.3 Final Implementation Candidate

## Reviewer mandate

Perform a **fresh independent assembled-candidate Protocol/D3 Review** of immutable semantic candidate `{candidate}` against accepted Protocol 6.2 recovery `{baseline}` and the active Protocol 6.3 workplan. Do not inherit implementation conclusions, this handoff, green CI, preservation labels, or any 260/260 report as authority. Reconstruct the governing semantics and inspect the assembled candidate at the exact commit.

If a genuine blocker exists, identify the earliest owning layer and precise repair obligation and keep Stage G blocked. If none exists, record independent Review PASS as descendant evidence only. Review PASS itself does not establish recovery, accepted-current status, workplan archive, or `main` cutover.

## Immutable identity set

```text
accepted Protocol 6.2 recovery:            {baseline}
accepted Protocol 6.2 semantic candidate:  {baseline_candidate}
accepted Protocol 6.2 public bootstrap:    {baseline_bootstrap}

current 6.3 public bootstrap:               {bootstrap}
later 6.3 public mapping descendant:        {mapping}
final 6.3 semantic candidate:               {candidate}
fresh F2/static-sensor evidence commit:     {f2_commit}
Protocol 6.3 recovery:                       UNAVAILABLE
```

Earlier 6.3 chains (`1484c1d...`/`8d0ad239...` and `5ee4b3ac...`/`1bfb789...`/`7f677415...`) plus reviewed branch state `100cbde...` are historical evidence only. They are useful negative fixtures but are not current acceptance identities.

## Governing surfaces

Review at minimum the active workplan; preservation census; implementation state; `{f2_report}`; static activation sensors; PEM/evidence/convergence/workflow/testing/versioning/Git/trust owners; `source/project_engineering_memory.py`; `PROJECT-ENGINEERING-MEMORY.md`; Protocol 6.3 focused tests; generated `dist/`; Protocol 6.3 profile/prompts/snapshot; and frozen prior-version resources.

## Highest-risk falsification obligations

### D4R2 — accepted-repair subject binding

Independently attempt all of the following: a real repair followed by an unrelated descendant file presented as acceptance; a typed acceptance artifact naming a different repair; missing/ambiguous acceptance state; missing accepting owner; reversed chronology; and copied/rebased/cherry-picked aliases. None may increment recurrence. A valid recurrence must establish a prior occurrence, exact accepted repair subject, durable accepted state/owner evidence, and materially later independent event.

### D5R2 — derived `PROVEN` independence

Construct a `PROVEN SUCCESS_PATTERN` with multiple supporting episodes sharing one provenance cluster while omitting every claimant `requires_replication`/`requires_independence` flag. It must fail. The claimant cannot decide that a required obligation does not exist by omission. Also challenge arbitrary CLOSED obligation names and works-to-preferred/default/best laundering without comparative warrant or accepted owner priority.

### Public bootstrap/lifecycle

Verify `{bootstrap}` is an already-existing self-reference-safe immutable source snapshot and does not self-name; `{mapping}` later publishes that exact snapshot; candidate `{candidate}` realizes the mapped fallback without conflating fallback with recovery or accepted-current state. Recheck the inherited Protocol 5.16 self-reference-safe source-resolution capability and frozen 5.16/6.0/6.1/6.2 resource bytes.

### D1/D2/D3/D6/D7 preservation

Re-falsify durable binding/path resolution, atomic root/partition publication, immutable observation/correction lineage across family move/re-ID, typed notice trigger evaluation, and exact accepted-base/HAS/overlay composition. A regression in these preserved repairs is a blocker even though D4R2/D5R2 were the surviving review defects.

### Four mandatory Challenge dimensions

Run Loss, Scope/materiality laundering, Priority inversion, and False compaction independently against the assembled candidate. In particular, ensure positive/Hot memory cannot hide unresolved higher-impact or mandatory lower-salience state and that compaction never becomes duplicate authority, stale-index authority, eager history loading, or collapsed provenance/lineage.

## F2 evidence to challenge

`{f2_report}` at `{f2_commit}` is implementation-context evidence only. It freshly accounts for exactly 260 cases: 115 inherited scenarios, Q63-01..79, F63-A..BJ, and four Challenge passes. Sample the D4R2/D5R2 rows first, then verify complete accounting and that semantic-paired rows actually discriminate the stated counterfactual rather than merely restating doctrine.

## Review output contract

A valid independent result states the exact candidate/baseline reviewed; preservation reconstruction; D1-D7 and bootstrap disposition; all four Challenge dispositions; sampled generated/package/frozen integrity; any blocker with earliest owner repair; applicability of F2 evidence; PASS/NO-PASS; and Serious Challenge status.

Until independent Review PASS and separate Stage G recovery lifecycle complete:

```text
independent Review: PENDING
Protocol 6.3 recovery: UNAVAILABLE
Stage G: BLOCKED
accepted current: Protocol 6.2
workplan: ACTIVE
main cutover: NOT AUTHORIZED
```
''', encoding="utf-8")

# Preservation census: preserve full T01-T39 and durable-surface census while
# replacing only stale current identity/closure/lifecycle sections.
p = Path("qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md")
text = p.read_text(encoding="utf-8")
front = {
    r"^semantic_candidate: .*?$": f"semantic_candidate: {candidate}",
    r"^public_source_bootstrap: .*?$": f"public_source_bootstrap: {bootstrap}",
    r"^public_source_mapping_commit: .*?$": f"public_source_mapping_commit: {mapping}",
    r"^stage_f_static_sensor_commit: .*?$": f"stage_f_static_sensor_commit: {f2_commit}",
    r"^stage_f_qualification_commit: .*?$": f"stage_f_qualification_commit: {f2_commit}",
    r"^status: .*?$": "status: f2-qualified-independent-review-pending",
}
for pattern, replacement in front.items():
    text, n = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if n != 1:
        raise SystemExit(f"census frontmatter rewrite failed: {pattern}")

h = "## Baseline, repaired candidate, and frozen identities"
h2 = "## Finite durable and generative surface"
if h not in text or h2 not in text:
    raise SystemExit("census identity anchors missing")
identity = f'''## Baseline, repaired candidate, and frozen identities

```text
accepted Protocol 6.2 recovery:            {baseline}
accepted Protocol 6.2 semantic candidate:  {baseline_candidate}
accepted Protocol 6.2 public bootstrap:    {baseline_bootstrap}
6.3 implementation branch start:           5508911f3227c7bcb7e38b0c74a7a37f13fd6b7c
accepted-main branch point:                bf856f742d1744a8ff50f300ee6493fb93e5c9d0

historical invalidated chain 1:             1484c1d3... -> 8d0ad239...
historical invalidated chain 2:             5ee4b3ac... -> 1bfb7894... -> 7f677415... -> 5f52fbdf...
reviewed NO-PASS repair state:              100cbde296de6c1a8db14151f34cfacfebc90eb3

current repaired public bootstrap:          {bootstrap}
later public mapping descendant:            {mapping}
final implementation semantic candidate:    {candidate}
fresh F2/static-sensor evidence:             {f2_commit}
independent Review:                          PENDING
Protocol 6.3 recovery:                       UNAVAILABLE
```

Frozen orchestrator resource trees retained across 6.3 implementation:

```text
sdp-protocol-5.16: 10a5f6707697e55d9e762db7f3b25b19640fccb4
ssdp-protocol-6.0:  16e5b378a87e32ec648305ba865377bfdf5bdf62
ssdp-protocol-6.1:  437f95bf15fb8f9ec430fa5e6de221c9a99af299
ssdp-protocol-6.2:  b111f80e39ace08e3888530277ce89743461329d
```

Accepted 6.2 packaged blobs remain:

```text
prompts.md:   159c58cbac0a8cf66311ddf7e11ad8eb03644e8c
profile.json: 6f21ad0592da343db951ffd56d25aa74a881bd8c
```

Earlier 6.3 chains are preserved as historical evidence and negative fixtures only; no current PASS disposition relies on them as acceptance identities.
'''
text = text[:text.index(h)] + identity + "\n\n" + text[text.index(h2):]

h3 = "## Protocol 6.3 T40-T120 closure map"
h4 = "## Source-generation and lifecycle boundary"
if h3 not in text or h4 not in text:
    raise SystemExit("census closure anchors missing")
closure = f'''## Protocol 6.3 T40-T120 closure map

`QUALIFICATION_CLOSED` means candidate semantics plus discriminating implementation-context evidence are closed. It does not mean independent Review, recovery, accepted-current state, or Stage G is closed.

| IDs | Target semantic group | Current disposition | Current evidence / remaining gate |
| --- | --- | --- | --- |
| T40-T61 | authority separation through logical canonical memory, evidence/statistics/temperature/HAS/capability/coverage/progressive disclosure/package separation | QUALIFICATION_CLOSED | final candidate `{candidate[:12]}...`; focused Protocol 6.3 counterfactuals; F2 result `{f2_commit[:12]}...`; rebound static sensors at the same evidence commit |
| T62 | 6.3 bootstrap/profile/recovery/version staging | PARTIAL_STAGE_G | bootstrap `{bootstrap[:12]}...`, later mapping `{mapping[:12]}...`, candidate `{candidate[:12]}...` qualified; immutable recovery selection/mapping remains Stage G after independent Review |
| T63-T65 | frozen prior resources; source/generated/package parity; static-vs-live claim discipline | QUALIFICATION_CLOSED | fresh F2 assembled gates at `{f2_commit[:12]}...`; static evidence explicitly makes no live-telemetry claim |
| T66 | Protocol 7 inheritance/current-lifecycle reconciliation | OPEN_STAGE_G | no silent Protocol-7 D3 change; accepted-current/history/authority-index reconciliation remains post-Review/recovery |
| T67 | human-facing background/terminology/abbreviation completeness | QUALIFICATION_CLOSED | inherited documentation/orchestration regression plus full source/package pass |
| T68 | independent assembled-candidate qualification/Review | OPEN_INDEPENDENT_REVIEW | handoff targets `{candidate[:12]}...`; implementation-context 260/260 cannot satisfy independent Review |
| T69 | anti-scope-laundering/lower-salience mandatory preservation | QUALIFICATION_CLOSED | fresh Scope/materiality laundering + Priority inversion Challenge dispositions in F2 evidence |
| T70-T120 | recursive-warrant prevention through watermark/coverage separation, including authority binding, atomic publication, base/overlay, trust, provenance, immutable observation/correction, recurrence lineage, semantic identity, maturity/comparative guidance, salience and HAS-basis rules | QUALIFICATION_CLOSED | current owners + focused executable PEM tests + final assembled regression + exact Q63/F63 accounting in `{f2_commit[:12]}...` |

The surviving review defects are closed in implementation context: D4R2 binds accepted-repair evidence to the exact repair subject/state/owner rather than chronology; D5R2 derives replication/independence obligations for `PROVEN SUCCESS_PATTERN` rather than trusting claimant flags. D1/D2/D3/D6/D7 remain reverified preserved repairs.
'''
text = text[:text.index(h3)] + closure + "\n\n" + text[text.index(h4):]

h5 = "## Source-generation and lifecycle boundary"
h6 = "## Current gate disposition"
if h5 not in text or h6 not in text:
    raise SystemExit("census lifecycle anchors missing")
lifecycle = f'''## Source-generation and lifecycle boundary

Completed implementation-side sequence:

```text
canonical 6.3 doctrine/routes/template + PEM validator/tests
 -> reviewed D1-D7 repair state and NO-PASS at 100cbde...
 -> D4R2/D5R2 owner-level false-pass repair
 -> self-reference-safe immutable public bootstrap {bootstrap[:12]}...
 -> later exact public mapping {mapping[:12]}...
 -> final semantic candidate {candidate[:12]}...
 -> full source/package/profile/Core/frozen-resource acceptance
 -> final static-sensor recomputation
 -> exact 260-case F2 qualification {f2_commit[:12]}...
 -> current independent assembled-candidate Review handoff
```

Still-open lifecycle:

```text
fresh independent assembled-candidate Review of {candidate[:12]}...
 -> immutable recovery descendant only after Review PASS
 -> later recovery mapping + mapping-bearing regeneration
 -> targeted recovery/profile/package/Core acceptance
 -> lifecycle/history/authority-index/self-hosted accepted-PEM/Protocol-7 reconciliation
 -> workplan archive / separately authorized cutover
```

`PROJECT-ENGINEERING-MEMORY.md` remains project-local PARTIAL candidate-overlay state and is never copied into generic `dist/` packages or protocol profile snapshots.
'''
text = text[:text.index(h5)] + lifecycle + "\n\n" + text[text.index(h6):]

gate = f'''## Current gate disposition

```text
SERIOUS CHALLENGE: NONE IDENTIFIED IN IMPLEMENTATION-CONTEXT QUALIFICATION
INHERITED T01-T39: RECONSTRUCTED, PRESERVED, AND REQUALIFIED
T40-T61: QUALIFICATION_CLOSED
T62: PARTIAL_STAGE_G — public bootstrap/profile leg closed; recovery leg intentionally open
T63-T65: QUALIFICATION_CLOSED
T66: OPEN_STAGE_G — final Protocol-7/current-lifecycle reconciliation
T67: QUALIFICATION_CLOSED
T68: OPEN_INDEPENDENT_REVIEW
T69-T120: QUALIFICATION_CLOSED
SEMANTIC CANDIDATE: {candidate}
PUBLIC BOOTSTRAP: {bootstrap}
PUBLIC MAPPING DESCENDANT: {mapping}
F2 260-CASE RESULT COMMIT: {f2_commit}
INDEPENDENT REVIEW: PENDING
PROTOCOL 6.3 RECOVERY: UNAVAILABLE
ACCEPTED CURRENT PROTOCOL: 6.2.0
WORKPLAN: ACTIVE
MAIN CUTOVER: NOT AUTHORIZED
```
'''
text = text[:text.index(h6)] + gate
p.write_text(text, encoding="utf-8")

# Cross-artifact identity and state sanity.
paths = [
    "workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md",
    "qualification/ssdp6/IMPLEMENTATION-STATE-PROTOCOL-6.3.md",
    "qualification/ssdp6/INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.3.md",
    "qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md",
]
for path in paths:
    t = Path(path).read_text(encoding="utf-8")
    for required in (candidate, bootstrap, mapping, f2_commit):
        if required not in t:
            raise SystemExit(f"{path} missing current identity {required}")

workplan = Path(paths[0]).read_text(encoding="utf-8")
for required in (
    "implementation_review_state: repaired-qualified-independent-review-pending",
    "reopened_stages: none",
    "stage_g_recovery_gate: blocked-pending-independent-review",
    "### 17.1 Completed Protocol 6.3 implementation-review repair contract",
    "The only remaining Stage-F lifecycle gate is a **fresh independent assembled-candidate Protocol/D3 Review**",
):
    if required not in workplan:
        raise SystemExit(f"workplan missing reconciled state: {required}")

state = Path(paths[1]).read_text(encoding="utf-8")
if "Protocol 6.3 recovery: UNAVAILABLE" not in state or "Stage G: BLOCKED" not in state:
    raise SystemExit("implementation state overclaims lifecycle closure")

handoff = Path(paths[2]).read_text(encoding="utf-8")
if "independent_review: required_fresh_context" not in handoff:
    raise SystemExit("independent review handoff is not pending fresh context")

census = Path(paths[3]).read_text(encoding="utf-8")
if "T68: OPEN_INDEPENDENT_REVIEW" not in census or "PROTOCOL 6.3 RECOVERY: UNAVAILABLE" not in census:
    raise SystemExit("preservation census overclaims lifecycle closure")
