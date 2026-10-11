# S2b independent tooling review — 2026-10-11

Governing SSDP version: 6.6.0. Final disposition: **PASS for bounded S2b tooling after the repair recheck below**. Initial disposition was **NO-PASS** on the first reviewed draft. No Serious Challenge to the accepted S2b architecture or decision specification was established. The three initial D4 conformance blockers were repaired by the parent implementation owner and independently rechecked; initial findings and identities remain preserved below. This is a fresh Codex review; no code was changed by the reviewer.

Subject: `/home/samjin/agent-skills/scientific-software-development-protocol/.claude/worktrees/agent-aa5d0c3f4a3d3a7e3`, branch `ssdp-7.2.1-tooling`, uncommitted delta over `24518df5627bea00c1d84708acfd26cf2c4edb41`. Authority reconstructed from `S5-721-REDUCTION-PLAN-2026-10-11.md` revision 4, especially §§6.1, 7, the thirteenth stakeholder ruling including exact-text ratification, and the consolidated workplan's measurement/backstop and review boundaries. Software-design entrypoint, abstraction/concretization, architecture, workflow, testing, evidence and definition owners were applied. Older Stage-F repairs in the consolidated plan do not enlarge this S2b scope. Memory lookup had no relevant hits; no memory assertion supplied authority.

## Blockers

**B1 — item-specific unowed harm can disappear through aggregation.** `compare_721.evaluate` aggregates every `delegate_request.unowed.*` item's fails before testing whether the comparator is at zero. Give new one `unowed.F` failure and aa zero F failures, but give aa one `unowed.T` failure: no harm flag is emitted. §7 lists these as items outside the primary pool and guards unowed parts above zero with aa at zero. Cross-item comparator failures cannot cancel the guarded item. Existing `test_unowed_request_parts_failing_in_new_with_aa_at_zero_is_flagged` explicitly expects this suppression. Repair the actual item route and discriminating test.

**B2 — authorized conditional observations silently disappear.** `compare_721.load_rows` builds its command map with `if not c.get("conditional")`. An offline synthetic completed `sentinels-add-c01` run with a binding failed sentinel consequently produces no descriptive row. §7 requires full per-item sentinel tables; conditionality governs authorization/launch, not deletion of realized observations. Include completed authorized add-on observations descriptively without adding them to the main primary population. The same filter also loses burden add-on accounting, though live Q5c remains separately owned by h4.

**B3 — check-plan accepts loss of a required panel arm.** From the real `Mapping721` offline plan fixture, remove p72aa from burden command metadata and argv, reduce run counts accordingly, and remove matching b1 burden declaration slots. Keep arms-spec unchanged (burden still explicitly contains p721/p72aa/p65). `prepare_campaign.py check-plan` returns code 0 with `verdict=PASS`, 81 planned runs and no problems. The single arms specification must govern panel membership; current subset-of-all-arm-name checking does not establish panel conformance. Validate each command against its panel's exact required arms, preserving explicit compatibility/configuration semantics only if reconciled with the specification.

The counterexamples ran only on synthetic/scratch outputs and retained S4 route material. Material findings were promptly sent to the parent repair owner.

## Executed and inspected evidence

Independent command: `env -u SSDP70_OMP_PROVIDER_CREDENTIAL python3 -m pytest -q -p no:anyio qualification/ssdp70/qual-v2` — **126 passed in 34.03 seconds, no skips**. That result predates repairs and does not negate the counterexamples.

The suite's actual-owner integration executes `harness70.run_episode`, then `assess70.main` through campaign_assess run/collect, then build_campaign_record on two distinct run roots with the same logical identity (both harness replicate 0). Adapter doubles sit below these owners; this is offline route evidence, not live provider or production qualification. Synthetic full declarations exercise plan, check-plan, verify, distinct disposition keys and pair_order per command-set replicate; missing/misplaced/extra replicate realizations are rejected by the builder. The command-set route leaves corpus manifest and logical scope unchanged. No derived manifest or episode-mode launch replaces matrix execution.

Retained 72b compatibility tests reproduce baseline plan/declaration/expected-runs (normalizing scratch paths), collected dispositions plus console output, and campaign record/audit plus console output byte-identically against 24518df. Explicit default arms-spec and omitted arms-spec agree. This is byte parity of the tested existing campaign surfaces, not a claim of arbitrary configuration equivalence.

Mapping p721→cand, p72aa→b1, p65→b65 reaches unchanged h4.q5c: routes T1/T7/T8 pass on uniform synthetic modes; mixed T7 modes remain PENDING below seven pairs. Conditional launch remains separately authorized, chunks remain two episodes, and h4's other gates are not used to decide the 7.2.1 comparison.

Decision tests and source reconstruction establish named P1/P2/P3 pools, strict margins, fixed harm thresholds, W/B unresolved filling, one seeded index matrix carrying both arms/replicates by episode, and numpy/pure-Python parity for diagnostic samples. Tests include clear improvement, no improvement, FRAGILE bracket, missing data, external false/pending gates, and component tables explicitly labelled keyword proxies. B1/B2 remain material omissions despite this coverage.

Duplicate original/rerun directories and missing declared runs are independently rejected by build_campaign_record via verify; compare_721 assumes the external activation/admissibility condition has been established and is not itself the identity/realization admission owner. It takes the first rerun when multiple exist, but that cannot support go if the required external verify boundary correctly rejects duplicate reruns. Missing dispositions remain unresolved; unequal realized main opportunities require the declared external admissibility/paired measurement gate rather than an invented substitution for lost realizations. Preserve these assumptions in the closed runbook.

## Remaining gates and scope

Fresh repaired-candidate test/review evidence is required. §7's operating-characteristic re-simulation on clustered synthetic data through the frozen decision function and the design lead's table in WORK/STATUS.md remain prelaunch obligations; small diagnostic simulations in the suite are not that complete table. S2a, S3 independent edit/mapping review, static Q5c, sizes, authorizations, live Q5c, concurrent measurement, result recommendation and stakeholder ratification remain separate. Nothing here changes release state or qualifies 7.2.0/7.2.1.

No custody keys/authoring, fixture item contents, rubric answers or calibration responses were accessed. No real provider credential was held/printed/used. No live provider call, source/dist edit, frozen harness edit or core70 edit was made by this review.

## Reviewed SHA-256 identities

All paths below are relative to `qualification/ssdp70/qual-v2/` in the draft worktree.

| File | SHA-256 |
|---|---|
| arms_spec.py | 22df359a2e7102975725d25a7ef0ba9135ade2da1c0f921d93db264cdf9d6f8f |
| prepare_campaign.py | 91a3713fd7feb7d939e8e34423efb6b807682f62e1f2b0d109b3a960c0088461 |
| campaign_run.py | 4c073aa73f1f56d8dccda3dc7995d271aa773b0fd040b97762703637a1dd08a0 |
| campaign_assess.py | cec14a395cfca2d858bd0787b0e5b2f763fd1a984e821103ca3ed495e0257cf2 |
| build_campaign_record.py | a05a529655bb35b3b9fb77aef2cd0a27b0c136a47a13b53f4b62f8be22dde606 |
| compare_721.py | c6feee6f31ffa6d17412fd8e6fd210ae0ecf45ee306929d45b0bef540eee1dab |
| test_arms_spec.py | d9ad6b4a06b77ee91e21e73b0e221b46d75a51a3a8230328dee168c991d67d66 |
| test_compare_721.py | 80a2de2924d226d93f23cacdeedaf1141ebc9abf5039db6233205f8f4cb47c3e |
| test_prepare_campaign.py | d65bed36d1aa6016dad4432787cb7b688be2228c4c2461282ae92e3df6212234 |
| test_build_campaign_record.py | 809559290a50be85ad1664c23d94c9565ebd7cc8777be67189c1eb63dbac1860 |
| h4.py (unchanged owner) | 37e8f9c2154c101456e91cf2137cd27a6e3dbb1f9f331b967a8e1634475d958f |

## Final repair recheck — PASS

The parent implementation owner repaired B1–B3. Fresh source reconstruction and reviewer-owned repetitions of all three counterexamples confirm: unowed.F remains flagged despite aa's unowed.T failure; completed sentinel add-on failure is present descriptively while primaries still select main; omission of p72aa from burden with matching argv/declaration now produces check-plan exit 2 and a runner refusal. Explicit-spec panel membership is exact; no-spec legacy configuration behavior remains preserved.

Independent focused recheck: **38 passed in 9.61 s**. Independent final complete recheck, same credential-unset offline command as above: **128 passed in 34.52 s, no skips**. `git diff --check` passed. The final full suite includes retained baseline byte-parity and actual-owner two-command shared-identity coverage. No code was changed by the reviewer. All initial blockers are closed on these bytes.

Additional requested attribution-support delta: `measure_blocks.py` maps named duty bullets and tension sublines onto the existing seven elements and preserves numbered historical mapping. Reviewer direct checks exercised historical numbered element 1, named Choices→6, Inaccessible homes→3 and tension search subline→3. Measuring retained 7.2.0 generated dist gives exact per-part sums and zero UNATTRIBUTED bytes for every six block-bearing skill. This is support-tool compatibility evidence; it does not grant the future S3 independent losslessness/mapping check or semantic edit review.

Final bounded S2b **PASS** does not close S2a, S3, final frozen-parameter operating-characteristic table publication before live launch, static/live Q5c, campaign authorizations, concurrent measurement or stakeholder adoption. They retain their stated stage owners. Frozen 10,000-resample decision execution is specified and deterministic; diagnostic simulation coverage does not replace the separately required final prelaunch table.

Final reviewed SHA-256 (unchanged identities not repeated retain the table above):

| File | SHA-256 |
|---|---|
| prepare_campaign.py | 4228ee4676ced8e6c406cb5b285ede177e19f7272df2d809bf164d2b34e8c0a8 |
| campaign_run.py | d6510f3d636d8963cf70a2ea1b4741104fb379375d38788870c8361e5ecdbf30 |
| compare_721.py | 7541b0d5e2a1c8d46de41d69ed40cee5c2cd5f9c0ae9d266085d0f1318c95db3 |
| test_arms_spec.py | 936e18bf198d01fcfaf604ce6b6682cb542611865d3e90b11bd29364087aaad9 |
| test_compare_721.py | 3806eef5fc199ab3d7976d9e090f757f0070c72a1fc17b32cf2e6f215918cea5 |
| measure_blocks.py | 8e67d239a7c5866ae50a95b605364c6fd5dd55a70e4bd496372337495a151011 |

## Population-accounting follow-up — bounded S2b PASS preserved

Independently counted only retained run metadata (`runs/main-c*/*-<arm>-r*/requirements-snapshot.json`, `expected_scoring_items` IDs, and `summary.json` episode/state). No oracle output, custody manifest/items, rubric answers or evaluator explanations were read for this follow-up. Source: `/home/samjin/ssdp70-omp-stagef/qualification/campaign-72-20261008`. All three arms p72/p66/p66b declare exactly 122 main episodes with these identical per-replicate opportunities:

| Item | Declared opportunities |
|---|---|
| null_coverage.unowed | 90 |
| delegate_request.F | 14 |
| delegate_request.R | 14 |
| delegate_request.V | 14 |
| delegate_request.T | 14 |
| delegated_finding_loss | 14 |
| tension_report | 28 |
| o1_authoring | 12 |
| detection.unnamed | 33 |
| claim_integrity | 122 |
| unauthorized_mutation | 122 |

Thus **P2=110 per replicate, 220 per two-replicate arm**, and **P3=277 per replicate, 554 per two-replicate arm**. `compare_721.py` DESIGN and DESIGN_EPISODES=122 match the retained declared metadata. The governing plan's parenthetical opportunity annotations (116/232 and263/526) are erroneous accounting, while its exact item lists correctly own executable pooling. Do not change simulator population counts to reproduce those wrong annotations. The runtime decision already computes actual item opportunities rather than hardcoding either pool total.

The p72 baseline has 122 COMPLETE_ADMISSIBLE runs; p66 has 121 plus one EXECUTION_ERROR; p66b has122 COMPLETE_ADMISSIBLE. These are declared counts, not claims that every historical comparator assessment resolved. DESIGN's separate unresolved probabilities and synthetic latent correlation remain approximation assumptions explicitly stated by the simulator; this audit establishes population counts only, not empirical adequacy of those stochastic assumptions.

Disposition: **S2b executable PASS remains** on compare hash `7541b0d5e2a1c8d46de41d69ed40cee5c2cd5f9c0ae9d266085d0f1318c95db3`; no executable repair is needed for this accounting issue. The design lead must visibly reconcile the plan accounting before S4 simulation-table publication/live release, with exact listed pools unchanged. Until that reconciliation, S4 reporting/launch accounting is unresolved. Final frozen-parameter simulation and its correctly labelled assumptions remain separately required before launch.

Aggregate results: `/tmp/ssdp721-declared-populations.json`. Exact input digest inventory: `/tmp/ssdp721-population-input-digests.json` (366 requirements snapshots), SHA-256 of inventory UTF-8 bytes `888c49be787d208425d9670b3db984e8bc7efb7b83c5b38bb0fa76ce242fbd74`.
