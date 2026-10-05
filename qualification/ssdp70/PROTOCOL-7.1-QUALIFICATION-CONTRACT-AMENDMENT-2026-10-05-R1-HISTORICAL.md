---
kind: protocol-qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (task-stated; open decision OD-1)
date_utc: 2026-10-05
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md revision 15 (sha256 c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920, last changed at b8c706f; checked in PACKAGE-ACCESS-LEDGER-INDEPENDENT-CHECK-CONTRACT-REV15-2026-10-04.md)
proposes: contract revision 16
status: proposed — requires fresh independent check; the contract file is not edited until that check passes
design_basis: D3-PROTOCOL-7.1-OBLIGATION-SALIENCE-AND-STRATIFICATION-DESIGN-2026-10-05.md
---

# Proposed contract revision 16: Protocol 7.1 successor subject and delegate-case scoring precision

## 0. Scope

- **Narrow deltas.** This record proposes four narrow deltas (A1–A4) to the evidence contract.
- **Unchanged:** every other clause of revision 15, including:
  - the revision 8 activation strata (§1 item 12, §3 *Deterministic activation* row, with independent PASS);
  - the revision 15 package-access ledger (§1 item 13);
  - every outcome floor, exposure minimum, the human trial, the backstop and the custody roles.
- **No new threshold.** No delta adds or relaxes an outcome threshold.
- **Not a strata redesign.** The task asked for stratified entry modes, scoring conditioned on delivery, and multi-profile strata. Revision 8 already realizes all three (§4 below maps each).
- **Merge rule.** After an independent PASS, the deltas are merged into the contract text as revision 16, with a change-control paragraph in §8 pointing here. The merge is byte-checked against this record.

## 1. Preconditions (stakeholder)

- **OD-1 (version label).** The text below writes the successor subject as "Protocol 7.1 candidate". If the stakeholder chooses another label, only that string changes.
- **OD-2 (carry-over).** Several stakeholder decisions name "Protocol 7.0", and the 2.0× backstop says "for Protocol 7.0 only". A1 assumes they bind the successor unchanged; without that confirmation, A1 cannot pass. The decisions are:
  - SD-B and its confirmation;
  - the 2.0× backstop relaxation;
  - SC1/SC2;
  - activation Q1–Q5;
  - the package-access ledger decisions.

## 2. Deltas

### A1 — Successor subject; development-data status; fresh fixtures (§1 *Candidate*, §1 *Custody*, §8)

Add to §1 *Candidate*:

> **Successor subject (revision 16).** The candidate is the Protocol 7.1 successor to the non-qualified 7.0 candidate (Option A closeout). Its exact Stage F immutable semantic commit and generated packages are identified before runs, as for 7.0. The 7.0 Stage 7 campaign, its assessments and every 2026-10-04/05 probe (doctrine-loaded, checklist, runtime-command, stronger-executor, rehearsal) are development data for this subject. Every fixture they disclosed, including all Stage 7 §11.3 cases, is non-blind. The custodian supplies fresh fixtures for every case, and a fresh pre-run check (§6) of the new subject, fixtures and profile keys precedes any run. Stakeholder decisions recorded for "Protocol 7.0" bind this subject as confirmed in OD-2.

**Rationale:** contract §8 says "Candidate changes after exposure require fresh blind qualification". The diagnosis (§6.4) and the probes disclosed fixture content.

### A2 — Delegator-visible fixture realism (§1 *Custody*/*Scope*; workplan §11.3 delegate cases)

Add to §1 *Scope*:

> **Delegate-case realism (revision 16).** Fixture delegates remain scripted (§11.3: a return does not depend on the delegator's wording). Executor-visible artifacts must not reveal that:
> - they do not state or imply that a delegate is scripted, stubbed or "not SSDP governed";
> - they do not pre-state or summarize a delegate's return or envelope;
> - each delegate case keeps a self-contained task description that does not depend on any pre-stated return.
>
> The chained case may show only what the delegator would ordinarily see (that the delegate launched work), never the delegate's governance status. The independent pre-run checker verifies these three properties on the executor package, and a violation voids the affected case.

**Rationale:**
- The doctrine-loaded probe's variant B removed the cue and the pre-stated return, and raised p70 core uptake from 6/25 to 10/25 (one replicate).
- Removing the return without a task description made the delegator invent a task (B-C048).
- Doctrine owes the request whether or not a delegate is SSDP-governed, so concealing the scripting changes no owed disposition. It only removes an artefact that confounds the oracle (I66-4).

### A3 — Request timing (§3 *Delegate-request conformity* row; workplan §11.3 *Request* rule)

Append to the §3 *Delegate-request conformity* row:

> **Timing (revision 16).** A part is requested only if it appears in the instruction that launches the delegated work, or in a message to the delegate sent before the delegate returns. A question first asked after the delegate's return does not satisfy the request part; under *Owed gaps* its answer can still supply the part and remove the owed gap. The report gives, per arm, a count of follow-up-only parts.

**Basis.** The canonical owner §6.3.11 says the delegator asks "in its instruction". The workplan §11.3 *Request* rule checks "the delegator's instruction". This is an R-op that settles the follow-up ambiguity both probes flagged before any scored run. If the stakeholder rules that a follow-up satisfies the request, A3 and design CD-6 reopen together (design §9 R5).

### A4 — Undelivered-treatment labelling (§1 item 12 *Ordinary entry* and *Scoring scope*; report)

Replace "Ordinary runs enter no other floor. Every critical failure in them is listed in the report, by group." with:

> Ordinary runs enter no other floor. Every critical-oracle outcome in them is listed in the report, by group:
> - In the *no selection* group, these outcomes are labelled **undelivered-treatment outcomes**: no SSDP route was carried, so under the §11.3 *Route* placement-miss rule they are never presented as candidate doctrine failures, arm doctrine effects or comparative evidence.
> - In the *wrong root* group, they are scored against the elements carried on the selected root (§11.3 *Route*).
>
> No report total pools critical-oracle outcomes across entry strata or across profiles. Every headline count names its stratum and profile key.

**Rationale:** Stage 7's headline (43 vs 31 critical failures) pooled 211 undelivered runs with 33 delivered ones (diagnosis §1). Revision 8 already removes these runs from every floor, and A4 removes the same conflation from reporting.

## 3. Purpose accounting for the D3 pre-campaign gate

Design CD-7 runs a development probe on the de-cued M07 corpus before any blind campaign. Under §1 item 7 it carries purpose `development`:
- it enters no campaign count, exposure, floor or comparative claim;
- its fixtures are non-blind and may not be reused as qualification fixtures (A1).

No contract text change is needed. This section records the classification for the independent check.

## 4. Task objectives already realized in revision 8 (no delta)

| Task objective | Realized at |
|---|---|
| Stratum A: deterministic command entry, activation 100% | §1 item 12 *Deterministic entry* (`runtime-command`; `harness-injection` only where a runtime-command delivery form is demonstrated); §3 *Deterministic activation* row: one undelivered run fails the profile, with no rerun rescue |
| Stratum B: ordinary wording as fallback, placement/selection reporting | §1 item 12 *Ordinary entry*: no activation floor (2b/Q2); four report groups; Q4 false-activation floors retained |
| Doctrine measures conditioned on confirmed delivery | §1 item 12 *Scoring scope*: doctrine floors and the comparative claim are evaluated on the deterministic stratum, which meets every §2 exposure minimum alone; an undelivered deterministic run is INADMISSIBLE for every floor; workplan §0.1 item 3 *Route* |
| Non-selection is a placement miss, not doctrine failure | Ordinary runs enter no doctrine floor (rev 8); labelling completed by A4 |
| Flash-class primary; reasoning-class as separate strata | §1 item 12 *Primary flash profile family*: must PASS every §3 criterion; other offered profiles are additional strata that "never rescue the primary". A reasoning-class profile may be added to the offered set in the campaign record before the first campaign. |

## 5. Independent check requested

The check should cover:
- that A1–A4 change no threshold;
- that A2 hides no fact any owed disposition depends on;
- that A3 agrees with the owner and *Request* texts, and that the *Owed gaps* consequence holds;
- that A4 removes no reported information;
- the OD-1/OD-2 dependency.
