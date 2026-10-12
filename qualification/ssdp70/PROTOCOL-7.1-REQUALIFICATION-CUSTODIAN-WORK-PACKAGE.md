---
kind: role-work-package
role: fixture custodian (capable model, separate context; not the candidate author; not the analyst)
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (candidate; non-governing)
date_utc: 2026-10-06
owner_plan: PROTOCOL-7.1-REQUALIFICATION-PLAN.md (phase P3)
---

Governing SSDP version: 6.6.0.

# Fixture custodian work package: Protocol 7.1 requalification

You author the fresh blind material that the 2026-10-06 matrix lacked. Read these first:
- the requalification plan, §§1–3 and §5;
- contract §1 items 6, 9 and 12, §2, §3, §4 and §11.3 (via the workplan the contract cites);
- Rev 16 A1/A2;
- the old store's `CUSTODY-RULES.md` and `HARNESS-INTERFACE.md`.

You may read the 2026-10-06 development transcripts. You may not see any *qualification* run output before the freeze. You report to the analyst and operator **only** counts, digests and the interface files.

The operator will run `requal71 corpus-check`, `custody-stat` and `custody-compare` on your output. Treat their STOP reasons as defects in your deliverable, not as a negotiation.

## C-1 Fresh custody store (arrangement per SD-2)

- **Location.** A new path, never the 2026-09-28 store. Same layout: `corpus/`, `requirements/`, `oracles/`, `keys/`, `probes/`, `human-trial/`, `authoring/`, `operator/`, plus the interface files.
- **Access log.** `ACCESS-LOG.md` is **append-only and excluded from `FREEZE.sha256`**. Its first entries carry forward the old store's unlogged 2026-10-05/06 key uses from the development record §9. Alternatively, append them to the old store's log and refreeze that store.
- **Freeze gate.** `FREEZE-GATE.json` starts `{"candidate_frozen": false, "frozen_run_output_exists": false}`.
- **Before and after each of your sessions,** the operator snapshots metadata (`custody-stat`), and you write an attestation entry naming the paths you opened (contract §1 item 9(b)).

## C-2 Fresh corpus (`corpus/manifest.yaml`)

Every episode carries the existing fields plus:

| Field | Rule |
|---|---|
| `panel` | `main`, `r2`, `sentinels`, `versioning`, `burden`, `routing` or `ordinary` (the plan's §1 key map) |
| `entry` | `pinned:<root>` on every non-ordinary panel; `ordinary` on the ordinary panel |
| `max_turns` | exactly the panel cap: 60 (`routing` 8, `ordinary` 3) |
| `replicates` | the SD-4 value |
| `admissible_roots` | ordinary episodes only: the catalog roots that count as admissible selection; `[]` for a negative |

**Coverage:**
- **Deterministic (`main` key).** Every §11.3 semantic case (composite detection, O1 authoring and review, tension retrieval, delegate cases including the chained case), freshly authored with new planted properties. It must meet every §2 minimum **on its own**: ≥ 20 non-critical detection units, ≥ 6 unnamed, ≥ 12 critical units, ≥ 6 each of nulls, variants, provenance and delegated findings, ≥ 12 owed delegate parts, ≥ 6 O3 and mutation opportunities, R2 classes, and ≥ 12 predicate-excluded opportunities on deterministic keys.
- **Size tasks to finish well inside 60 turns.** Under a 30-turn cap on 2026-10-06, 28 of 51 runs died on episodes declared at ≥ 40 turns.
- **Preservation panels (not blind; stay matched, per A1).** Import S01–S11/H01–H05 (ordinary, 32 paired episodes per arm), P01–P19 (routing, two runs per case), T1/T7/T8 (burden, three pairs, T7 pair addition per §4), T2/T3 (sentinels, twice each) and T4–T6 (versioning) from their accepted 6.6 sources.
- **New-class ordinary episodes.** At least 3 per arm for each of run, ad hoc analysis, results-review, gate-evidence, copy/transcribe/relay and delegate (report-only).

## C-3 Requirements and keys

- **Requirements.** `requirements/` uses the existing measure vocabulary (`expected_scoring_items.json` measures and criticality) so that the harness, `assess70.py` and `corpus-check` work unchanged.
- **Keys.** `keys/` holds planted properties, contested set, ledger and R2 declarations as before.
- **Applicability rulings.** Record a written ruling for every exemption-bearing case: which delegate parts are owed on a fully specified change-only or no-run task. An "owed" ruling must follow owner §6.3.11 and Rev 16 A2 item 2; the 2026-10-06 EP-077 ambiguity must not recur.

## C-4 Stratum-aware scoring (you own the aggregate oracle and the manifest builder)

Change `oracles/_aggregate/aggregate_acceptance.py` and `operator/make_manifest_from_runs.py` so that:
1. The builder carries each run's `accounting.purpose`, `entry_stratum`, `declared_root`, `profile_key_sha256`, deterministic-activation verdict and assessment identity. It takes the **frozen accounting manifest** as input and emits every declared run, with no subset option.
2. The oracle refuses any run whose purpose is not `qualification`, and any manifest that omits a declared run.
3. A deterministic-activation stage fails the profile on any undelivered deterministic run, with no rerun rescue.
4. Critical, doctrine-floor and comparative stages use only runs on keys that the family `criterion_to_keys` assigns. Q4 floors use the ordinary key. Predicate false-firing counts only delivered or selected runs, with the ≥ 12 minimum on deterministic keys. Owner false activations pool over all keys.
5. The four ordinary report groups are emitted, and no-selection outcomes are labelled undelivered-treatment.
6. `advisory` or `unresolved` dispositions without an evaluator assessment identity are refused.
7. No output list is truncated, and counts are reported separately from samples.

**Integrity probes (contract §6).** These must be refused: a development-purpose run, an undelivered deterministic run, an omitted run, an ordinary run offered to a doctrine floor, and a synthesized assessment.

**Regex reassessment.** Re-assess the advisory patterns against paraphrase, using the development transcripts named in the record (EP-007, EP-042, EP-018 `p71`). Record the measured false-negative behavior; do not tune it to those transcripts' wording.

**Integration.** Give the operator the exact aggregate command line for runbook P10. Its exit codes must be:
- **0** when the outcome is PASS;
- **1** for any reached non-PASS outcome;
- **3** when the input is refused (missing run, wrong purpose, integrity failure);

so that a weaker operator can tell a refusal from a result.

## C-5 Human-trial banks

Fresh matched banks drawn from the fresh fixtures, plus a recorded draw, under the existing `human-trial/PROTOCOL.md`.

## C-6 Hand-over (counts only)

Provide:
- `IDENTITIES.json` and `FREEZE.sha256` with its digest;
- per-panel episode and replicate counts, and §2 exposure counts per measure by stratum;
- the C-4 command line;
- `METADATA-FOR-IMPLEMENTER.md` and `HARNESS-INTERFACE.md`.

No key, answer, planted-property identity or oracle pattern goes to the analyst, the operator or any executor.
