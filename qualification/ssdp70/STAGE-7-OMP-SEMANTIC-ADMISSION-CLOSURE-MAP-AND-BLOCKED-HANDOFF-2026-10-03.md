# Stage 7 OMP semantic-admission closure map and blocked handoff

**Terminal state: `BLOCKED / READY FOR` the *fixture custodian* role (cells 1–10, 13), with a separate evaluator-admission build gated on host prerequisites (§1 B1).** No semantic evidence was produced, no role other than the implementer ran, no provider execution occurred, and no cell of the 13 changed status. This is a design/blocker record, not admission evidence. Role instructions and the executor invocation are in `STAGE-7-OMP-SEMANTIC-ADMISSION-ROLE-HANDOFFS-2026-10-03.md` (the **handoffs**).

Governing SSDP: `6.6.0`. Starting HEAD `f3c5ad10c7c91a88503705e81660c1ba4bc906fa`; the tree is byte-identical to `ec580a340b415c4cfe88d2a76f2b93744c202b79` (tree `60b107f2…`, verified). Ending HEAD: unchanged; this report is the only working-tree change and is uncommitted.

## 1. Blockers, earliest first

**B0 — environment: RESOLVED for writes; two live prerequisites remain.** The stakeholder added `$HOME/ssdp70-omp-stagef` as a working directory, after which the residue quarantine was done (§4). Still absent in the implementer's sandbox: the `omp` executable (`/opt/omp/omp` does not exist; only the retained runtime-closure tarball is present) and provider egress (`api.deepinfra.com:443` denied by the egress proxy). Without them no exact-profile execution and no evaluator probe can run from this session. I did not try to work around either.

**B1 — evaluator admission has no governed producer and no existing ADMITTED record.**
- `core70.EVALUATOR_ADMISSION_CHECKS` (6 checks) and `validate_profile_admission(role="evaluator")` *consume* an ADMITTED record. `omp_stage7_admission.py` is executor-only and states it has "no code path that writes status=ADMITTED".
- No file anywhere under the repository or `$HOME/ssdp70-omp-stagef` is an evaluator `profile-admission*.json`. The only evaluator artifacts are residue from the reverted `a94288b9` work.
- The only prior evaluator realization is the Claude profile that failed its admission premises (`STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-ACTUAL-PROFILE-RECHECK-STOP-BLOCKED-2026-09-28.md`, A3/A7).
- Consequence: `assess70.py` cannot lawfully run (it raises unless `validate_profile_admission(mode="qualification")` passes for the evaluator). This is upstream of cells 2–13 evaluator-judged evidence, 11 and 12.
- Runtime options, checked: **Claude** — the only credential on this host is `SSDP70_DEEPINFRA_API`, there is no Anthropic route, and the v4 Claude adapter was never live-verified. **OMP via the existing adapter** — impossible without editing `adapters/omp.py`: `OMP_BUILTIN_TOOLS` (`omp.py:136`) is the fixed six-tool surface, `omp.py:946` requires every profile's `native_tools` to start with it, and `omp_argv` (`omp.py:1058`) passes it to `--tools`. An evaluator must be read-only, and `omp.py`'s hash is bound into the executor profile key, so editing it would stale all 34 exact-profile runs. **OMP via a new evaluator adapter file** — expressible without touching any frozen file; chosen (§3 R1). It is a sizeable D4 build and its claims (read-only enforcement, credential/network denial) can only be proven live, which needs the B0 prerequisites.
- `assess70.result_text()` parses Claude-style `{"type":"result"}` events, which OMP's stream does not emit, so the new adapter must translate (adapter-owned) or `assess70` must change. I did not read `adapters/claude.py` or `harness70.py` in full.

**B2 — `perturb_evaluator_identity` has no reuse boundary to perturb.** `assess70.py` never reuses an assessment; it always launches the evaluator. The only cache is the executor-run cache (`core70.cache_valid`, `core70.py:1668`). `assessment_identity` (`assess70.py:312-333`) already binds evaluator profile key/document, capabilities, adapter, wrapper, core, admission, runtime observation, key-tree digest, rubric digest, schema version and scoring manifest. Contract §1.11 states a binding rule for assessment reuse *if it exists*; §6 asks for an evaluator-identity perturbation. Whether "no reuse mechanism" makes the cell vacuous or requires a reuse validator to exist is a contract reading I should not make. Inventing a fixture cache would be the forbidden self-fulfilling test.

**B3 — no executable cross-run comparative-scoring owner found** (grep over `core70`, `assess70`, `harness70`, `evidence70`, then `eval/*.py`; only cell-name bookkeeping matched). `known_broken_both_arms_miss` ("critical failure not averaged away despite aggregate improvement") is a cross-run property, while `outcome_from_dispositions` (`core70.py:795`) is per-run. Either the evaluator judges it from custodian-held paired data and a key, or the real owner does not yet exist. Needs a ruling; limited search, so treat as "not found", not "absent".

Earlier than all of these, and not a blocker: **no Serious Challenge.** The contract does not forbid a supplemental subcampaign (see §2).

## 2. Contract findings that shape the design

- **Custody/pre-run timing is "before any candidate run" / "before an execution profile may run qualification subjects"** (contract §1, §6) — i.e. before blinded Protocol 7 subjects, not before the retained Stage 7 transport realizations. The workplan (lines 769, 771) directs missing cells to be produced "through the existing real owner" under the campaign. So a **new** custodian→checker→execution chain for a targeted semantic subcampaign is permitted. The historical synthetic campaign (`non_custody=true`) cannot gain retroactive custody and is not asked to. The final checker, not me, decides if that is sufficient.
- **The 13 cells are `independent-inspection` evidence class** (`allowed_evidence_classes`). `record_proof` checks only campaign containment and source hashing for them; the admission tool does not verify semantics. Adjudication is the independent checker's job by design.
- **Chained case (workplan line 815):** "no known-broken probe can exercise that condition; the independent pre-run checker confirms it with a first-look probe (I66-4)." The contract's mechanism is a *checker first-look probe over what is at hand*, over a custodian-frozen scenario whose anomaly lives only in launched-work records. Delegation in this profile is a **data-only stand-in** (`stub_tools/mediator.py:delegate` returns a fixture string; retained events label it `scripted-qualification-standin`). A custodian-authored chained stub is corpus data and needs no frozen-code change. If the final checker instead demands a real nested launched agent, the mediator (a bound support file) must change and **the exact profile key goes stale** (§5). Flagged as an open reading, not assumed.
- A false lead I checked and dropped: the mediator reads `delegates/<agent>.json` while the corpus writes `reviewer.yaml`. The retained run shows `known_agent: true` and a delivered return, so the delegate path works.

## 3. Rulings taken under the stakeholder's delegation

The stakeholder said to handle these as I see fit. They are **implementer proposals**, recorded so the final checker can accept or reject them; none is authority, and each states what rejection would cost.

- **R1 — evaluator runtime (B1).** A new read-only OMP evaluator adapter in a new file (`adapters/omp_eval.py`), DeepInfra route, no edits to any frozen file, admitted through the existing six evaluator checks by a *separate* evaluator-admission checker. Rejected alternatives: Claude (no credentials, never live-verified), editing `omp.py` (stales the executor profile and all 34 runs). Cost if rejected: a different evaluator runtime and a new profile, so nothing built on R1 survives.
- **R2 — reuse (B2).** Contract §1.11 states a binding rule for assessment reuse and says an assessment cache "may be" separate; no reuse is required to exist, and none does. I build no reuse validator. Evidence offered for cell 11 is therefore the real `assessment_identity` binding from two real evaluator assessments plus static proof that no consumer reads a prior `assessment*.json`, labeled **vacuous-by-absence**, not as a behavioral rejection. Cost if rejected: a new reuse validator module with its own real-boundary tests, then actual reuse attempts under one-at-a-time perturbation.
- **R3 — both-arms-miss (B3).** Realized as an episode whose evidence carries both arms' per-subgroup results and an aggregate improvement, judged by the evaluator against a custodian key (per-run `outcome_from_dispositions` is the owner reached). No cross-run comparative scorer is built or claimed. Cost if rejected: such an owner does not exist and must be specified (D3) before the cell can be evidenced.
- **R4 — chained delegate.** Custodian-authored data-only stand-in plus the pre-run checker's own first-look probe, which is the contract's stated mechanism (workplan line 815). No mediator change. Cost if rejected (real nested launch required): `stub_tools/mediator.py` changes, the profile key changes, and all exact-profile evidence is stale.
- **R5 — planted defects.** Known-broken subject output may be produced by an exact-profile run whose custodian-authored task instructs the defective output; the discrimination tested is the evaluator's/oracle's, the expected disposition is the custodian's frozen label, and no retained report is hand-edited. Cost if rejected: cells 2–5, 7–9 need naturally occurring defects, which a single model cannot guarantee.

## 4. Campaign state verified (read-only)

**Cleanup done.** `semantic-evidence-20261003/` (126 files, created after the review sealed at 20:58 local) was inventoried (aggregate `0459f0e7b1f4065070087c7c14ea78ca5d3752109ab7e08296f372a436d36f28`, identical to the earlier read-only pass) and moved, not deleted, to `$HOME/ssdp70-omp-stagef/quarantine-a94288b9-reverted-semantic-evidence/` with `inventory.sha256`. It is forensic only and is no input to any role. After the move, against `original-file-inventory.json` (2,280 files): **2,279 byte-identical; `campaign.json` differs, as expected** — it is the mutable index that `record_proof` advanced; the original is preserved as `original-campaign.json`. The 26-file `review-artifact-manifest.json` matches. 35 proof files = 22 PASS + 13 UNRESOLVED. The active campaign is the intended post-review state. I did not run the CLI `verify`.

## 5. Frozen identity and freshness

No executable, profile, capability, support, runtime-closure, campaign, or admission-tool byte was changed. Frozen identities unchanged: candidate `d50dcb53…`, semantic subject `db94a2df…`, profile `3ce07101…`. The 34-run transport evidence therefore remains applicable **for transport/provenance/containment/scheduling only**; it cannot discriminate any semantic cell (synthetic single-item presence oracles).

Routes that would stale the profile if chosen: any edit to `core70.py`, `harness70.py`, `adapters/omp.py`, OMP support files (incl. `stub_tools/mediator.py`), `omp_stage7_*.py`. The design below deliberately adds no such edits. A new evaluator admission producer must live in a **new file** and not edit `core70.py`; an assessment-reuse validator (if B2 requires one) would be new code too, and the checker must decide whether `core70` binds it.

## 6. Closure map (every cell is `BLOCKED`)

Categories per the task: A retained evidence + independent inspection; B new exact-profile OMP run; C real evaluator on frozen key/rubric; D real cache/reuse; E custodian/pre-run checker, pre-execution; F chained delegation. "Frozen disposition" is authored by the custodian and is **not** authored here.

| # | Cell | Cat. | Real owner / path | Behavioral event needed | Independent role(s) | Timing | Existing campaign evidence? | Provider? |
|---|---|---|---|---|---|---|---|---|
| 1 | withheld_oracle_branches | E | custody records; pre-run checker | custodian freezes classification rationale, branch inventory, exposure plan, key digests; checker inspects the frozen bytes | custodian + pre-run checker | checker access log must precede first semantic run; process-generated timestamps | No (`non_custody=true`) | No |
| 2 | known_broken_both_arms_miss | B+C (+B3) | per-run dispositions via `assess70`; comparative owner unresolved | paired arms where decisive subgroup missed in both while aggregate improves | custodian, evaluator | key frozen pre-run | No | Yes |
| 3 | known_broken_wrong_binding_o3 | B+C | evaluator vs custodian key; matched O2-only/O3-bound | report that expands scope/binding vs correct scope | custodian, evaluator | key pre-run | No | Yes |
| 4 | known_broken_wrong_null_variant_delegate | B+C | evaluator; separate null/variant/delegate-gap branches | one bad run per branch + compliant control | custodian, evaluator | same | No | Yes |
| 5 | known_broken_false_tension_closure_asserter | B+C | evaluator; native vs claimed asserter in retained events | closure with spoofed/shared account, multi-bound applicability | custodian, evaluator | same | No | Yes |
| 6 | known_broken_loss_before_destructive_boundary | B (deterministic oracle viable) | real exact-profile trajectory in a disposable workspace; order-sensitive oracle on native+normalized events | positive: inquiry/retention before destructive action; negative: destructive first | custodian (oracle), checker | oracle frozen pre-run | No | Yes |
| 7 | known_broken_unauthorized_write | B+C | containment (`mutation`/`sandboxed`) is §1.8 evidence; *semantic rejection* is evaluator | judgment that treats a sandboxed write as authorized | custodian, evaluator | same | Containment part only | Yes |
| 8 | known_broken_version_self_adoption | B+C | evaluator; 6.6-bound task, p66/p70 arms | Protocol-7-only duty vs 6.x-required duty, attribution | custodian, evaluator | same | Arm packages only | Yes |
| 9 | known_good_legitimate_withholding | B+C | evaluator; frozen cheap-first-look envelope | specific legitimate limitation vs generic hedge vs skipped view | custodian, evaluator | same | No | Yes |
| 10 | known_good_designed_termination | B | real runner episode ending through designed termination; `termination`/terminal-result/artifact state through `core70` evidence states | designed vs normal vs incomplete vs error | custodian, checker | pre-run | No (positives completed normally) | Yes |
| 11 | perturb_evaluator_identity | D (blocked by B1, B2) | cache/reuse boundary — **does not exist** | reuse under identical identity; one-at-a-time perturbation of model/runtime/reasoning/wrapper/key-rubric/schema; actual reuse attempt | evaluator, checker | after evaluator admission | No | Evaluator runs |
| 12 | final_report_changed_files_tool_trace_assessment | C (blocked by B1) | `assess70.py` end to end | real launch; manifest, runtime observation, trace, identity, verdict, containment; missing-evidence negative | evaluator, checker | after evaluator admission | Only `prepare_bundle` delivery, offline | Evaluator runs |
| 13 | chained_delegate_first_look | F+E | custodian-authored stub; checker's first-look probe over what is at hand | executor's real delegate call/return; anomaly only in custodian-held launched-work records | custodian, OMP executor, separate checker | stub frozen + checker probe pre-judgment | No (single canned reviewer) | Yes |

**Counterexample discipline (per planned discriminator).** For every deterministic oracle (cells 6, 10), the smallest wrong implementation that would still pass is one keyed to the strings the custodian wrote rather than to event order/terminal state. Required control: the same oracle run on the *negative* realization must fail, and the oracle must be authored by the custodian before the run, not by the implementer. For evaluator cells, a wrong evaluator that always answers `pass` must fail the known-broken branch, and one that always answers `fail` must fail the known-good branch; each branch therefore needs a paired control inside the same frozen suite.

## 7. Role packages (inputs frozen at the boundary; no role may be simulated by me)

1. **Fixture custodian** — context separate from the implementer. *Produces* synthetic Stage 7 semantic fixtures, expected dispositions, classification rationale, branch inventory, exposure plan, destructive-boundary/termination oracles, chained stub data, evaluator keys/rubric; writes a content-addressed freeze manifest with timestamps produced by the freezing process. *Receives*: contract §§1–2, §6, this map's rows. *Must not* write candidate source or see executor outputs. *Withholds from implementer/executor*: keys, expected dispositions, rationale.
2. **Pre-run checker** — separate from custodian and implementer. *Inspects frozen bytes before any semantic run*; records access log, counts, pass/fail; confirms the chained first-look condition (I66-4). Its record must be generated by its own process; I cannot supply it.
3. **OMP executor** — runs targeted exact-profile episodes under profile `3ce07101…` only after #2's record exists and its digest matches the frozen manifest. Receives blinded task artifacts only. Ordinary driver flow, retained under the campaign root.
4. **Evaluator** — runs only after evaluator admission (B1) exists, receives retained run evidence plus keys after run output is frozen.
5. **Final independent Stage 7 checker** — fresh context; adjudicates all 13 cells and owns lifecycle finalization. Nothing here substitutes for it.

Deliberately **not built now**: a custody-freeze tool, destructive/termination oracles, evaluator admission producer, a cache validator. Each depends on an open ruling (§3) and on being exercised at the real boundary, and unexercised machinery written ahead of those rulings would be the scaffolding this task forbids. The freeze tool's minimal interface when it is built: append-only manifest of path/size/sha256 and process-generated UTC stamps, recorded before, and checked by, role #2.

## 8. Per-cell disposition and required reporting

All 13: **BLOCKED**.

1–10, 13: reason — fixture custody (role #1) and pre-run check (role #2) have not occurred; executor runs additionally need the B0 host prerequisites. For 2–5, 7–9 also B1 (no admitted evaluator), for 13 also R4 acceptance.
11: reason — B1; R2 acceptance.
12: reason — B1.

| Item | Value |
|---|---|
| Changed files | this report and `STAGE-7-OMP-SEMANTIC-ADMISSION-ROLE-HANDOFFS-2026-10-03.md`; non-git: residue moved to the quarantine directory |
| Frozen profile/candidate identities changed | No |
| Retained campaign applicability | Transport/provenance/containment/scheduling only |
| Targeted provider executions | None |
| Evaluator admission identity | None exists; none created |
| Assessment identity | None produced |
| Cache/reuse tests | None; no reuse mechanism exists (B2) |
| Custodian identity / frozen digests | None; role has not run |
| Pre-run checker identity/result | None; role has not run |
| Chained-delegate realization | None |
| Blinded subjects touched | No |
| Independent Stage 7 proof status changed | No; 22 PASS (structural) + 13 UNRESOLVED stand |

Checks executed: repository state and tree-identity verification; residue inventory, quarantine move and campaign file-hash comparison (2,280 files, run before and after the move); nested `bwrap` smoke test (works), `omp` executable and DeepInfra reachability probes (both unavailable); source reading of the contract, workplan §11, independent review, `core70.py` (check sets, admission, outcome), `assess70.py`, `omp_stage7_admission.py` (class map, `record_proof`, exact-profile claim checks), `stub_tools/mediator.py`. **Not read in full:** `harness70.py`, `adapters/omp.py`, `adapters/claude.py`, `omp_stage7_campaign.py`. No test suite was run, because no code changed.

**BLOCKED / READY FOR: the fixture custodian** (handoffs §1), with the evaluator adapter build and executor launch waiting on the host's `omp` executable and DeepInfra egress.
