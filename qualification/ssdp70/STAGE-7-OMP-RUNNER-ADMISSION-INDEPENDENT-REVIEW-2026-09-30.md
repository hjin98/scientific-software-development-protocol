# OMP-only Stage F — independent Stage 7 runner-admission review

- **Review date:** 2026-09-30 (America/Chicago; 2026-10-01 UTC)
- **Governing SSDP:** 6.6.0
- **Repository:** scientific-software-development-protocol
- **Branch:** ssdp-7.0-scientific-epistemic-closure
- **Verified head:** 5fd73cb7fcf40a95083b59a277b81ca4eddcf8c7
- **Executable implementation candidate:** d03216d76d8860f42dc2ccc598e3c8d49d36203e
- **Immutable semantic subject:** db94a2dfb7fef480f37227eab5c45256e89901b8
- **Disposition:** **NO-PASS. OMP remains UNADMITTED. Protocol 7 qualification-subject execution is not authorized.**
- **Intended handoff:** D3 designer, for disposition of the D4 blockers and planning the required fresh admission evidence.

This is a derived review-evidence record. It does not amend the qualification contract, admit the profile, qualify a candidate, or issue a separate D3 acceptance.

## Background and terms

OMP is the qualification records’ label for the frozen omp executable and adapter reviewed here. D3 denotes the software-architecture owner; D4 denotes specification and executable-concretization ownership. Stage 7 runner admission is the required gate before Protocol 7 qualification subjects execute. In the containment summary below, PID means process identifier, IPC means interprocess communication, UTS is the Linux hostname/domain namespace, and seccomp is Linux system-call filtering. These explanations do not replace the contract or workplan.

## Authority and scope

The review reconstructed authority from the repository AGENTS instructions supplied for this task; the active consolidated SSDP 7.0 workplan; the Protocol 7 evaluation and qualification contract, especially portable runner-admission §1 items 1–11 and §6; both Stage 6 OMP records; and current OMP implementation under qualification/ssdp70/eval/. Direct source routes are listed at the end of this record.

The workplan requires a fresh independent pre-run checker to assess the exact adapter/profile against every §1 item and §6 before any Protocol 7 qualification subject runs. Stage 6 implementation conclusions and acceptance records were treated as evidence claims to inspect, not as admission authority.

The verified head is the expected head. Its two commits after the executable candidate update Stage 6 evidence documentation only; no executable or test source changed after d03216d76d8860f42dc2ccc598e3c8d49d36203e. The current executable review scope therefore remains that exact candidate.

## Exact profile and fresh probe

| Identity | Independently checked value |
| --- | --- |
| Profile ID | omp-headless-deepinfra-glm53-flash-stage6-repair-20261001T000313%NZ-c0cce5a575a9 |
| Profile-key SHA-256 | 86da2241272919344cd40075bcf79e61c63dbd3eb27249c8bd2f729fcca89a10 |
| Profile-document SHA-256 | 29c7578d39a8441f34309643f75aa91241047f7d226b2ecca948dab046aacac8 |
| Runtime and build | OMP 18.0.11; build 2c2e51f3b6fae6722da4f7b69751a2e9467ab063 |
| Runtime-closure identity | 6c49a21528ae33c2f8dfee60995448b3d7af795a4b2b826c164f87699d4d8499 |
| Runtime-manifest SHA-256 | 5114fe69e08c17470d4b19d7d3d1d20ad755ec20965151dc04afaf2b8c247216 |
| Provider / model / reasoning | DeepInfra / zai-org/GLM-5.3-Flash / high |
| Capability-manifest SHA-256 | f01ec2b6bda9c30ffb9495029cce8481ab762a62a0f1c3d9452c17a3d0ca0e55 |
| Installed semantic package digest | 7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8 |

Fresh probe realization inspected:

/home/samjin/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T005750650447Z-d03216d76d8860f4-5ea83cffdd46/out/E1-p70-r0/

Its run-identity SHA-256 is 509d8459969962f9fc793c6aecd717894408b3ee1a4e7feb4db4f6bc4f362e1f. Its evidence-integrity manifest SHA-256 is b47c06708ce11a7ae2b08abfddf0d571eb453a229a2386883de594df71d12d27. The terminal state is execution_mode=probe, evidence_state=COMPLETE_ADMISSIBLE, qualification_outcome=NOT_EVALUATED.

## Evidence independently executed and inspected

These checks were run against the retained probe and the exact current implementation. They are read-only evidence validation, not a new provider probe or qualification run.

- Reconstructed the run identity from the external run inputs, exact profile, capability manifest, requirements and current source implementation. The complete reconstructed identity matched the retained identity and digest.
- Validated the complete-run state, normalized events and normalization completeness. Rehashed every file listed in the evidence-integrity manifest; no listed file differed.
- Reconstructed the 145-record raw stream from observer, bridge, OMP native trace and launcher evidence, then checked the sequence hashes against the normalization map. All 145 matched. All 11 normalized events matched their mapped sources; the map classified 7 oracle-relevant raw events and contained no unclassified event.
- Observed normalized kinds were one catalog snapshot, one root selection, six resource-access events, one termination, one final-result event and one usage/timing event. This was a single-arm, read-only probe; it did not produce mutation, delegation, issue-store or external-network-action events.
- Re-ran the current OMP runtime-closure/profile validation functions against the frozen runtime manifest and reviewed the containment realization and runtime-dependency attestation.
- Scanned retained run files in memory for the supplied credential’s raw, URL-encoded and base64 representations. No match was found. The credential value was not printed or persisted.
- Inspected the terminal summary, root/package-consumption evidence, profile and capability snapshots, requirements snapshot, native trace, observer evidence, bridge evidence, launcher evidence and final evidence manifest.

The exact run identity binds the semantic subject/package and records the profile key, capability and requirements identities, core/harness/adapter identities, pair-order/replicate fields, and evidence dependencies. This establishes identity and internal consistency for this probe; it does not establish admission.

## Evidence reused but not independently re-executed

- The real-provider probe was executed by the Stage 6 operator, not by this reviewer. Its retained request/response and observation chain were inspected and hash-validated; no new network request was made.
- The retained exact-head Stage 6 acceptance record reports 248 tests and OK for candidate d03216d76d8860f42dc2ccc598e3c8d49d36203e. The acceptance log and recheck report were inspected but the suite was not rerun by this reviewer. The supplied result reports zero skips, failures and errors.
- Stage 6 offline/stand-in test outcomes were considered only for their reported scope. They do not demonstrate §6 known-good/known-broken oracle branches through this exact profile.

No Protocol 7 qualification subject, §6 branch matrix, hostile side-effect attempt, matched-pair run, concurrent-pair run or test suite was executed by this reviewer. A required check that was not executed is not a pass.

## Portable runner-admission §1 dispositions

Each row gives the overall admission disposition for that item. Positive probe evidence is limited to the exact actions and identity observed in the single retained realization.

| Item | Disposition and evidence |
| --- | --- |
| **1. Exact subject and profile identity** | **NO-PASS.** The exact semantic subject, executable candidate, installed package digest, profile key/document, OMP build, runtime closure, provider, model and reasoning configuration reproduce. The profile records provider-managed unknowns as arm-neutral: provider backend shard, host-derived workstation block, and provider-layer transient/empty-response retry behavior. The workspace realization field specifies a fresh temporary project, while the profile key binds a retained build-inventory digest rather than an attestation of the executing host kernel/OS. Source review found that profile validation checks the frozen inventory-file digest but does not compare the current host kernel/OS to a run-bound value. Because the bwrap namespace/seccomp realization depends on the host kernel, migrating the frozen profile to another kernel is not shown to invalidate its identity. This is a D4 profile-key completeness/migration gap. |
| **2. Fresh arm isolation** | **NO-PASS.** The fresh probe showed one p70 arm, the expected SSDP catalog entries exactly once, no competing SSDP arm, and fresh project state. It did not run concurrent pairs or demonstrate independence between pair realizations. |
| **3. Versioned semantic capability manifest** | **NO-PASS.** The exact profile manifest maps catalog/root activation; workspace read/search/list and create/modify/delete/rename/mode/symlink; process execution; delegation; issue/evidence-store access; repository/version-control/object-store operations; network/remote service; external writes/mutations; and credential/service-account access to scoped allow/deny/sandboxed mediation. Source inspection supports those mappings and the subject boundary. Required denied-class and equivalent-escape attempts were not exercised through this exact profile. |
| **4. Complete raw trajectory and normalized event stream** | **NO-PASS.** The observed positive read-only trajectory is complete and its applicable catalog, root, resource, termination, final-result and usage events are linked. It does not exercise the required tool-side-effect, delegate, issue-store mutation, prohibited-network or external-mutation event paths; no conclusion about those absent event kinds follows from this probe. |
| **5. Raw-to-normalized completeness** | **NO-PASS.** The 145 observed raw hashes link in order to the normalization map; all observed normalized events match, and no event was left unclassified. This probe did not exercise injected drops, reordering, truncation, unknown event types, retries, parallel tool results or side-effect normalization. |
| **6. Required evidence/scoring manifests** | **NO-PASS.** The probe requirements snapshot is run-bound and integrity-checked, but this probe has zero required oracles and zero expected scoring items. It cannot demonstrate the frozen qualification artifact/oracle/scoring closure or exact assessment dispositions. |
| **7. Fail-closed state semantics** | **NO-PASS.** The positive probe correctly distinguishes process success (execution_ok=true), evidence state (COMPLETE_ADMISSIBLE) and qualification outcome (NOT_EVALUATED). Missing/malformed evidence, missing scoring dispositions, failed termination and negative-state rejection were not exercised through this profile. |
| **8. Containment and side effects** | **NO-PASS.** The retained realization attests the qualification-supervisor, provider-control/observer and subject/executor principals; staged runtime closure; and observer credential isolation. The subject is placed in bubblewrap user/PID/IPC/UTS/cgroup/network namespaces with loopback-only networking, dropped capabilities, seccomp restrictions, synthetic system files, and no host HOME, custody or mediator-private backing state. The relay implementation checks that a relayed client socket is held solely by the authorized OMP process. The fresh probe did not execute prohibited mutation, local-IPC, alternate-route, mediator-private-state or other hostile attempts. Behavioral containment remains unproved for admission. |
| **9. Custody** | **NO-PASS.** The probe retains no credential value, and the subject boundary excludes private backing state. It contains no fixture keys or evaluator material and does not demonstrate the future qualification executor’s fixture/key denial, role/time-scoped checker/evaluator access, or custody access audit through this exact profile. |
| **10. Pair scheduling** | **NO-PASS.** Source inspection shows arms are looped sequentially within each pair; replicate and pair order participate in identity, and pairs use separate run-owned state. This realization ran one arm only; sequential matched-pair behavior and concurrent-pair state independence were not demonstrated through the exact profile. |
| **11. Evidence/cache provenance** | **NO-PASS.** The fresh run binds the observed subject/package, profile, capability, core/harness/adapter, requirements and evidence files, and its integrity manifest revalidates. Assessment-cache reuse and cache/profile/core/evaluator identity perturbations were not exercised. The unbound current-host condition in item 1 also prevents full profile-migration provenance. |

## §6 oracle-integrity readiness

**NO-PASS.** The required pre-run suite has not been demonstrated through this exact OMP adapter/profile. In particular, this review has no exact-profile evidence for:

- known-broken rejection for each §11.3 acceptance branch/disposition, including both-arms-miss subgroup, wrong binding/O3, wrong null/variant/delegate gap, false tension closure/asserter, loss before the destructive boundary, unauthorized write and version self-adoption;
- known-good acceptance, including legitimate withholding and designed termination;
- missing artifact/oracle/scoring-disposition and incomplete/failed-termination rejection;
- cache, profile, core and evaluator identity perturbations;
- catalog contamination, containment escape attempts and retained unauthorized-attempt evidence;
- ordinary-entry root selection, owner reads and result for each case class;
- complete final reports, changed/new files and tool traces reaching assessment; and
- issue/network/external-write stand-ins that capture every side effect and detect unauthorized attempts, plus an independent first-look check of the chained-delegate anomaly.

The new probe is not this suite: its requirements contain no oracle or scoring items, its profile_admission_sha256 is null, and its outcome is NOT_EVALUATED. The workplan requires this exact-profile check before any candidate qualification subject runs.

## D3/D4 routing and designer handoff

**Serious Challenge to D3: none raised.** The source and retained realization show a realizable three-principal arrangement consistent with the workplan boundary. This review does not issue a separate D3 acceptance.

**D4 blockers for design and evidence closure:**

1. Bind the actual execution-host kernel/OS (or a controlled host-image identity) into the profile/run identity and fail before launch when the realized host differs. The existing frozen build-inventory digest is not a current-host comparison.
2. After resolving item 1, obtain a fresh independent exact-profile checker result for every §1 item and the complete §6 branch matrix. Do not use the positive provider probe or the 248-test Stage 6 result as a substitute.

No Protocol 7 qualification subject was run. This review does not authorize one.

## Historical identity discrepancy

The earlier retained realization at /home/samjin/ssdp70-omp-live-probe-20260930T041652Z/out/OMP-LIVE-1-p70-r0 reports internal identity 6fe36d822c54c5dd5b0b8921937bdc32227e67b59ddfeacc4810d68757b34fdc; the operator-observed historical identity remains c88938172de9ab888692e42f7fafca4653a5cf4c289cb4ed3a6ab3a32adaaa95. The discrepancy is unresolved. No cause is assigned.

For the new realization, the historical discrepancy is non-blocking only for identification of that new run: it is stored under a distinct path, its run identity was independently reconstructed from its own inputs, and its integrity manifest validated. Source inspection confirms realization creation refuses an existing output directory rather than replacing it. These facts do not resolve the old discrepancy or close any runner-admission requirement.

## Source routes

- [Portable runner-admission contract §1](PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md#L22)
- [Contract §6 oracle-integrity suite](PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md#L103)
- [Consolidated workplan full runner-admission gate](../../workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md#L647)
- [Stage 6 evidence and closure record](STAGE-F-OMP-STAGE-6-EVIDENCE-AND-CLOSURE-2026-09-30.md#L7)
- [Stage 6 repair and recheck record](STAGE-F-OMP-STAGE-6-REPAIR-RECHECK-2026-09-30.md#L9)
- [Core profile-key construction](eval/core70.py#L336)
- [OMP profile validation and runtime closure checks](eval/adapters/omp.py#L665)
- [Subject relay socket-holder check](eval/subject_launcher.py#L49)
- [Run identity and admission binding](eval/harness70.py#L390)

## Final disposition

**NO-PASS — OMP runner not admitted for Protocol 7 qualification execution.** The smallest current gating set is the D4 host-identity/migration gap plus fresh independent exact-profile execution of all §1 and §6 admission checks. OMP remains **UNADMITTED** until both close.
