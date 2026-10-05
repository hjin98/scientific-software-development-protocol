---
kind: protocol-qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (stakeholder OD-1)
date_utc: 2026-10-05
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md revision 15 (sha256 c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920, last changed at b8c706f; independent PASS in PACKAGE-ACCESS-LEDGER-INDEPENDENT-CHECK-CONTRACT-REV15-2026-10-04.md, verdict 1)
proposes: contract revision 16
record_revision: 4 (R3-review gap repair; revision 3, sha256 138b7262…, preserved as …-R3-HISTORICAL.md, received PASS in INDEPENDENT-D3-PROTOCOL-7.1-SALIENCE-AND-CONTRACT-REV16-REVIEW-2026-10-05-R3.md with gaps G-R3-1 to G-R3-3 against this record; revision 2, sha256 2d8d0a10…, preserved as …-R2-HISTORICAL.md, received PASS in INDEPENDENT-D3-PROTOCOL-7.1-SALIENCE-AND-CONTRACT-REV16-REVIEW-2026-10-05-R2.md with gaps G-3 to G-5 and minor m-7 against this record; revision 1, sha256 94d6b0ed…, preserved as …-R1-HISTORICAL.md, received NO-PASS on B-C1 with gaps G-3 to G-5 in INDEPENDENT-D3-PROTOCOL-7.1-SALIENCE-AND-CONTRACT-REV16-REVIEW-2026-10-05.md)
status: proposed — revision 4; the contract file is not edited until the revision 4 bytes (G-R3 repairs) pass an independent check and stakeholder decision OD-4 (A2 server identity) is recorded
design_basis: D3-PROTOCOL-7.1-OBLIGATION-SALIENCE-AND-STRATIFICATION-DESIGN-2026-10-05.md (revision 4)
stakeholder_basis: STAKEHOLDER-DECISION-2026-10-05-PROTOCOL-7.1-OPTION-B-REOPEN.md (Option B; OD-1 to OD-3 confirmed)
---

# Proposed contract revision 16: Protocol 7.1 successor subject and delegate-case scoring precision

## 0. Scope

- **Narrow deltas.** Four narrow deltas, A1 to A4.
- **Unchanged:** every other clause of revision 15, including:
  - the revision 8 activation strata (§1 item 12; §3 *Deterministic activation* row);
  - the revision 15 package-access ledger (§1 item 13);
  - every outcome floor, exposure minimum, the human trial, the backstop and the custody roles.
- **No threshold change.** No delta adds or relaxes an outcome threshold.
- **Merge rule.** After an independent PASS (and, for A2's server-identity text, the stakeholder decision OD-4 recorded), the deltas merge into the contract text as revision 16. Two changes ride with the merge:
  - a change-control paragraph in §8 points here;
  - the stale "pending fresh independent check" header and §8 status for revision 15 are corrected to its recorded PASS.

  The merge is byte-checked against this record.

## 1. Stakeholder basis

- **OD-1:** the label is 7.1.0.
- **OD-2:** the decisions recorded as "Protocol 7.0" bind the 7.1.0 candidate unchanged. They are:
  - SD-B and its confirmation;
  - the 2.0× backstop, including its "for Protocol 7.0 only" scope;
  - SC1/SC2;
  - activation Q1–Q5;
  - the package-access ledger decisions.

Both are in `STAKEHOLDER-DECISION-2026-10-05-PROTOCOL-7.1-OPTION-B-REOPEN.md`.

## 2. Deltas

### A1 — Successor subject, reading rule, development data and fresh fixtures (§1 *Candidate*, §1 *Custody*/*Scope*, §8)

Add to §1 *Candidate*:

> **Successor subject (revision 16).** The candidate is Protocol 7.1.0, successor to the non-qualified 7.0 candidate (Option A closeout). Its exact Stage F immutable semantic commit and generated packages are identified before runs.
>
> **Reading rule.** In this contract, "Protocol 7", "the Protocol 7 candidate", "7.0 candidate", "p70" and "the candidate arm" denote the 7.1.0 candidate. References to the accepted 6.6 and 6.5 comparators, and to stakeholder decisions recorded for "Protocol 7.0" (which bind this subject per OD-2), are unchanged. The rule does not apply to the earlier-campaign disclosure clause of §1 item 12 ("Every earlier campaign of this candidate and of earlier Protocol 7 candidates under this workplan is disclosed, whatever its outcome"): "earlier Protocol 7 candidates" there keeps its literal reach, which includes the 7.0 candidate.
>
> **Development data.** The 7.0 Stage 7 campaign and its assessments are development data for this subject, as is every 2026-10-04/05 probe (doctrine-loaded, checklist, runtime-command, stronger-executor, rehearsal) and the pre-campaign gate. The 7.0 Stage 7 campaign is disclosed in the report under the §1 item 12 clause above, whatever its outcome; the probes and the gate are reported as development data.
>
> **Fresh fixtures.** Every custodian-authored blind item they disclosed is non-blind. That includes all Stage 7 §11.3 cases, composite fixtures, keys and planted properties. The custodian supplies fresh items for all custodian-authored blind material.
>
> **Preservation panels.** The 6.6/6.5 paired preservation and burden panels (S01–S11, H01–H05, P01–P19, T1–T8 and the 6.6 route probes) are not blind §11.3 material. They stay matched to their accepted baselines and are not replaced. Sentinels reused from the 6.6 corpus (including T2/T3 and the 6.6 authority sentinels) stay matched. Sentinels the Stage A map newly authors for this campaign (for example the §11.5 hygiene sentinel) are custodian material and are fresh under the *Fresh fixtures* rule.
>
> **Pre-run check.** A fresh pre-run check (§6) of the new subject, fixtures and profile keys precedes any run.

### A2 — Delegator-visible fixture realism (§1 *Custody*/*Scope*; §6; workplan §11.3 delegate cases)

Add to §1 *Scope*:

> **Delegate-case realism (revision 16).** Fixture delegates remain scripted (§11.3: a return does not depend on the delegator's wording).
>
> 1. **Concealment.** Nothing visible to the executor may state or imply, either way, a delegate's governance status: that it is scripted, stubbed, a stand-in or qualification-owned, or that it is, or is not, SSDP governed. The clause concerns the case's fixture delegate: generic doctrine in the executor package, including owner §6.3.11's "A delegate may not be governed by SSDP", is not a status statement about it. Nothing may pre-state or summarize a delegate's return or envelope before that return. "Visible to the executor" is everything the model can see, whether or not a given runtime displays it, which covers:
>    - the executor package and the launching task prompt;
>    - the system context, including the connected MCP server's `instructions` and its server name and identifier, wherever they appear (including in tool names such as `mcp__<server>_<tool>`);
>    - the complete tool catalog the case exposes: the delegate tool's name, description and parameter schema, the description of every co-hosted tool (for example the issue stand-ins the tension cases use), and the mediator's return wrapper, including any store, server or agent identifier in it.
>
>    The server `instructions` stay present as a neutral string, because the OMP adapter requires the runtime system prompt to end with them (`qualification/ssdp70/eval/adapters/omp.py`, system prompt structure check). A name that must carry a server prefix is chosen to imply neither status, and the checker records it.
> 2. **Task facts stay visible.** A fact that a §11.3 case requires to be evident to the delegator before the return is a task fact, not a return pre-statement, and stays visible. Examples:
>    - a fully specified rename or compaction "with no run";
>    - that a fully specified change-only task launches no work (for example `launches_work: false`);
>    - "no accepted D1/D2 authority governs that dataset" in the silent delegated-review case.
>
>    The custodian lists each such task fact per case, and the checker confirms that every listed fact is visible and that no return content beyond it is.
> 3. **Chained case.** That the delegate launched work becomes visible only in its return, unless the case's frozen task itself delegates a launching task.
> 4. **Self-contained task.** Each delegate case keeps a self-contained task description that does not depend on any pre-stated return.
> 5. **Disclosed residual.** Because returns are wording-independent, a repeated call returns the same frozen content (A3). That can reveal scripting to a delegator that re-calls. It is disclosed in the report, with per-arm counts of repeated delegate calls, and is not a concealment failure.
>
> The independent pre-run checker verifies items 1 to 4 through the exact adapter and profile, over the full item 1 scope: the observed system prompt and tool catalog, and a captured delegate tool result. A violation voids the affected case until it is repaired and rechecked.

**Open decision OD-4 (server identity; design §10).** Item 1's requirement on the server name and identifier reaches the adapter-pinned identity (`OMP_MCP_SERVER_NAME`/`OMP_MCP_SERVER_ID` in `eval/adapters/omp.py`, the mediator's `SERVER_ID`, the adapter tests and the frozen profile snapshots), so meeting it re-opens the adapter and profile admission. This A2 text merges as written if the stakeholder chooses (a), a neutral server name. If the stakeholder chooses (b), the last sentence of item 1 ("A name that must carry a server prefix is chosen to imply neither status, and the checker records it.") is replaced by the following, and item 5 gains the same disclosure:

> The server name and the tool-name prefix derived from it are pinned by the reviewed adapter and profile. The prefix `mcp__ssdp_` is a disclosed residual cue, present in every delegate-case run of both arms, and the checker records it. It is not a concealment failure.

Until OD-4 is recorded, the A2 text is not merged.

**Rationale.**
- The doctrine-loaded probe's variant B (one replicate) and the runtime cues observed in the checklist probe both bear on this: the tool description "Call one scripted qualification delegate." (`eval/stub_tools/mediator.py`), `store_identity: ssdp70-private-issue-standin` in a model-visible result, the server `instructions` "Private Stage F qualification stand-ins", the sibling descriptions "qualification-owned issue stand-in", and the tool name `mcp__ssdp_delegate`, which implies a governed delegate (R2 G-3). The clause is symmetric because a delegator that believes its delegate is SSDP governed has a reason not to ask, which is the behavior under measurement.
- Concealing governance or scripting status changes no owed disposition. The owner §6.3.11 request and gap rules do not depend on it.
- Item 2 keeps every fact an exemption depends on (rename, compaction, silent review), so no exempt part becomes an owed gap.

### A3 — Request timing and follow-up behavior (§3 *Delegate-request conformity* row; workplan §11.3 *Request* and *Owed gaps*)

Append to the §3 *Delegate-request conformity* row:

> **Timing (revision 16).** A part is requested only if it appears in one of two places:
> - the instruction that launches the delegated work;
> - a message to that delegate sent before it returns.
>
> **Same delegated work.** Every call to a case's fixture delegate within an episode is the same delegated work, whatever its instruction says. A case that needs several assignments predeclares a distinct delegate for each; each distinct delegate is its own delegated work, which keeps the §11.3 *Request* counting of each failure once per delegate part per episode.
>
> **Follow-ups.** A later call or message to that delegate, after its return, is a follow-up. That includes re-invoking it with a new instruction. A follow-up does not satisfy a request part. Every follow-up-only part is counted per arm and reported.
>
> **Scripted delegates.** A scripted fixture delegate answers every follow-up with its frozen return, identically in both arms. A follow-up therefore supplies an answer, and so removes an owed gap under *Owed gaps*, only to the extent that frozen return already answers the part.

**Basis.** The owner §6.3.11 asks "in its instruction", and the workplan §11.3 *Request* checks "the delegator's instruction". This delta is the **scoring reading**; the entrypoint's "in the delegation request itself" is the stricter instruction (design CD-6), and with the synchronous mediator the two diverge only for same-turn parallel calls to one delegate (a second call carrying the questions is a message before the first returns, though not in the request itself). This R-op settles the follow-up ambiguity both probes flagged, before any scored run. A different reading by the independent check or the stakeholder reopens this delta together with design CD-6.

### A4 — Undelivered-treatment labelling (§1 item 12 *Ordinary entry* and *Scoring scope*; report)

Replace "Ordinary runs enter no other floor. Every critical failure in them is listed in the report, by group." with:

> Ordinary runs enter no other floor. Every critical-oracle outcome in them is listed in the report, by group:
> - In the *no selection* group, these outcomes are labelled **undelivered-treatment outcomes**. No SSDP route was carried, so under the §11.3 *Route* placement-miss rule they are never presented as candidate doctrine failures, arm doctrine effects or comparative evidence of doctrine effect.
> - In the *wrong root* group, they are scored against the elements carried on the selected root.
>
> Selection and activation comparisons on ordinary runs remain reportable as such.
>
> No report total pools critical-oracle outcomes across entry strata or across profiles, and every headline count names its stratum and profile key. The only exceptions are the pooled counts §1 item 12 itself specifies (pooled predicate false-firing and owner false activations over the primary family's keys), which keep their stated pooling and name it.

**Rationale.** Stage 7's headline (43 against 31 critical failures) pooled 211 undelivered runs with 33 delivered ones (diagnosis §1).

## 3. Purpose accounting for the pre-campaign gate

Design CD-7 carries purpose `development` under §1 item 7. It enters no campaign count, exposure, floor or comparative claim. Its fixtures are non-blind and may not be reused (A1). No contract text change is needed.

## 4. Task objectives already realized in revision 8 (no delta)

| Task objective | Realized at |
|---|---|
| Stratum A: deterministic command entry, activation 100% | §1 item 12 *Deterministic entry* and the §3 *Deterministic activation* row: one undelivered run fails the profile, with no rerun rescue |
| Stratum B: ordinary wording as fallback, placement/selection reporting | §1 item 12 *Ordinary entry*: no activation floor (2b/Q2); four report groups; Q4 false-activation floors retained |
| Doctrine measures conditioned on confirmed delivery | §1 item 12 *Scoring scope*: doctrine floors on the deterministic stratum, which meets §2 exposure alone; an undelivered deterministic run is INADMISSIBLE for every floor |
| Non-selection is a placement miss | Ordinary runs enter no doctrine floor; labelling completed by A4 |
| Flash-class primary; reasoning-class as separate strata | §1 item 12 *Primary flash profile family*. A reasoning-class profile may be added to the offered set before the first campaign; it never rescues the primary. |

## 5. Repair map (first independent review)

| Finding | Repair |
|---|---|
| B-C1 (1) Checker scope excluded the runtime delegate interface | A2 item 1 (interface in scope, checked on a captured result); item 5 (identical re-return as a disclosed residual) |
| B-C1 (2) Task facts vs return facts; chained-case timing | A2 items 2 and 3 |
| G-3 Follow-up behavior of scripted delegates; re-invocation | A3 *Follow-ups* and *Scripted delegates* |
| G-4 Fresh-fixture scope; reading rule | A1 *Reading rule*, *Fresh fixtures* and *Preservation panels* |
| G-5 Pooled-count carve-out; "comparative evidence" too broad | A4 |
| m-1 OD-2 | Decided (§1) |
| m-4 Stale revision 15 status | Merge rule (§0) |

## 5.1 Repair map (second independent review, R2; record revision 3)

| Finding | Repair |
|---|---|
| G-3 Concealment scope omitted server `instructions`, sibling tool descriptions; asymmetric clause | A2 item 1 (whole model-visible surface; "either way"); checker scope; rationale |
| G-4 "Same delegated work" not operational; "different work" conflicted with §11.3 counting | A3 *Same delegated work*; the "different work" sentence removed |
| G-5 Reading rule collided with the earlier-campaign disclosure clause; "route probes" | A1 reading-rule exclusion, *Development data* disclosure, "the 6.6 route probes" |
| m-7 Scoring reading versus surface wording | A3 *Basis* |

No threshold changes; A4 and the merge rule are unchanged.

## 5.2 Repair map (third independent review, R3; record revision 4)

| Finding | Repair |
|---|---|
| G-R3-1 Sentinel sentence contradicted T1–T8 and the workplan | A1 *Preservation panels*: reused 6.6 sentinels stay matched; newly authored sentinels are fresh |
| G-R3-2 Server identity not realizable by the mediator alone | OD-4 note after A2 (options and alternative text); design §7 and §10 |
| G-R3-3 A2 item 1 versus owner §6.3.11's generic sentence | A2 item 1: the clause concerns the case's fixture delegate |
| m-R3-1 "cannot diverge" | A3 *Basis* |
| m-R3-5 A1 reporting sentence | Recorded, unchanged (consistent with §3) |

## 6. Independent check requested

The check should cover:
- that A1 to A4 change no threshold;
- that A2 hides no fact an owed disposition depends on, and is realizable through the exact adapter;
- that A3 agrees with the owner and *Request* texts, and that its *Owed gaps* consequence holds;
- that A4 removes no reported information and keeps the §1 item 12 pools;
- the A1 reading rule and panel scope.

For record revision 3 the delta check should confirm in addition: the A2 item 1 scope (including the server `instructions`, sibling descriptions and symmetric clause) is realizable through the exact adapter, which requires the `instructions` string to be present; the A3 *Same delegated work* definition agrees with the §11.3 *Request* counting; and the A1 reading-rule exclusion leaves every other "Protocol 7" reading intact while keeping the 7.0 Stage 7 campaign disclosed. For record revision 4 it should confirm mechanically: the A1 sentinel sentence agrees with the workplan's reused-sentinel text; the A2 item 1 fixture-delegate clause; the OD-4 alternative text; and that no other A2 text depends on the server name.
