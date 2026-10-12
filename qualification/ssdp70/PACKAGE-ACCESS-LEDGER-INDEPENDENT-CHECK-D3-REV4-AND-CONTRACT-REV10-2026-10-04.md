# Independent check: D3 package-access ledger decision rev 4, contract rev 10, workplan §0.1 entry

Governing SSDP: 6.6.0 (Protocol 7.0 NON-QUALIFIED). Subject: commit 3469e833069ec4f8711459ff50486768fe63e743, tree aaa3e0476fd041ab0104cac2d5c018601581df2d (HEAD verified; working-tree copies of the five reviewed documents hash-equal to `git show HEAD:`; D4 code unchanged since 8be024a, `git diff 8be024a HEAD -- qualification/ssdp70/eval` empty).

SHA-256 reviewed: D3 decision bcadc010a19cb2064cf0a1775b60bd5a715164e22a5d2be1f7b6ed715e15dde0; contract 993d1faefa2d039a819e917e22cec71076a571a3c307d64963fcee59641f021d; amendment d1daf5978eea797ba86b86efb526f21b5ca24d369138d84f2f76e667f8a9582b; stakeholder record 2fc133684f776b21add8ec631e19ffc551613445c03f98f180270275d1ab93fe; workplan 6e64024a2f39cc7e260ac764f81a1308cfe7aa4d63cb5256758a576d9c38cf19.

## 0. Verdicts

1. D3 revision 4: **NO-PASS** (two D3 blockers, D3-B1, D3-B2; repairable without reopening the architecture).
2. Contract revision 10: **NO-PASS** (inherits D3-B1/B2 by binding; own blockers C-B1, C-B2, C-B3).
3. Workplan §0.1 entry and the two markers: **PASS**, with one required follow-up conditional on how D3-B2 is decided (W-1).

No Serious Challenge. The accepted graph (supervisor-owned kernel observation, no new principal/edge) is realizable and I found no reason to reopen D3 topology. Revision 8's criteria, family rule and activation-strata text are byte-unchanged except the pointers; but one effect change is not declared (C-B2).

## 1. Serious Challenge

None.

## 2. Blockers by earliest owner

### D3 (decision text)

**D3-B1. Owner-access bound is internally contradictory and, as written, can turn timing loss into a definite, non-replaceable FAIL.**
- Item 4a: "A sequence before the first R2 event is a definite zero-tolerance FAIL whatever the exactness"; contract item 13 and stakeholder decision 1 make a pre-R2 observation never replaceable.
- Item 6: "An owner open whose turn cannot be bounded is bounded at the earliest post-request turn and makes (B) not exact." An earliest-possible bound is not a definite time. A legitimate owner load after R2 whose open lands in a heartbeat gap, a timing-loss bracket or a request without tool results is bounded at turn 1, so its sequence is before R2, so by 4a it is a definite FAIL. It could not be replaced. The timing-stress form of the gate exists exactly to produce such runs. Item 5's "turn-ambiguous" clause would give the right answer (candidate turns span R2, hence ambiguous R2 timing, adjudicated) but item 6's unbounded case is not routed through it.
- Repair (one sentence class): an unbounded open has candidate turns = every post-request turn, is turn-ambiguous, and is "definite" pre-R2 only when the bracket's latest candidate turn precedes R2. State "definite" in 4a in those terms.

**D3-B1b (same blocker; the mapping is not "earliest consistent").** Item 5/6 claim the bound is the earliest consistent turn and that lag "can only widen a bracket, never make it wrong". That is true of the bracket (I confirmed the kernel part, §4) but not of the mapping to a trace sequence:
- The sequence is the smallest sequence among tool-result events first delivered by the first request stamped after the lower edge. An open that happens in the in-flight window of request j (background process `(sleep n; cat owner) &` from an earlier turn, or a runtime asynchronous open) precedes the assistant message and tool-call events of response j, yet is assigned to the results delivered in request j+1, which come after them. If R2 is an assistant/tool-call event of response j, the open is scored after R2 although it was before. The bound is later than the earliest consistent event. The earliest consistent point is the first trace event after the last request stamped before the lower edge.
- "An open after the last request is bounded by the end of the trace" is the latest, not the earliest, consistent point (turn-cap or error termination after a last response whose tool calls were executed). Bound it at the last response's first event.
- The tolerance for realtime/monotonic divergence is not added to bracket edges. The observer stamps records with `time.time_ns()` (CLOCK_REALTIME, `evidence70.py` lines 48 and 67), so the comparison is a realtime comparison; a sub-tolerance wall-clock step shifts the mapping by up to the tolerance. Widen by the tolerance or have both sides use one monotonic clock (that changes the hash-chained record schema; a contract/D4 consequence).
- Effect size: only background/asynchronous opens and termination edge cases; I reasoned this and did not execute the in-flight race (the stand-in provider answers in milliseconds; my background-open probe, §4, mapped correctly because the open landed in a tool window).

**D3-B2. "Any post-request owner open is owner access" creates false owner FAILs on ordinary honest behaviour, and the rehearsal gate cannot detect them.**
- Executed (real OMP 18.0.11 through the real adapter/harness, scratch probe): `bash grep -rl ZZZ_NOT_PRESENT /opt/ssdp/skills; echo scanned` opened 238 package files including all seven owner copies, recorded `owner_access` at one sequence for each, and no owner content reached the model. Under D3 rev 4 item 4a/6 and contract item 13 this is an owner access, and before R2 it is a zero-tolerance FAIL that is never replaced. Native `grep`/`glob` over the package and `grep -r` are both in the item 8 form list; a flash-class model told that skills live under `/opt/ssdp/skills` can plausibly do either.
- Contract §4 and §5 say owner **read** ("an owner read before the first predeclared R2 event", "Zero unowed owner reads"). Item 13 silently moves the floor from read to access (see C-B2).
- Item 8 measures exactness (byte, owner-access, owner-load) and bracket widths. A scan is exact on question (B) and returns the verdict FAIL, so the gate cannot flag it. The 0.8 target concerns owner-unresolved runs only. There is no aggregation for false-positive FAILs, and the reopen triggers (item "Reopen") name runtime rescans but not model-driven scans.
- What I did not find: a runtime rescan. In the real-OMP probe of seven requests with six bash turns (about 4 s) no post-request package open occurred. Compaction and long sessions were not exercised, so that premise is still untested.
- Required: D3 must either (a) add a bounded exemption (an opened owner copy whose content demonstrably did not reach the model and that is unexplained is "owner open without delivery": UNRESOLVED and replaceable, not FAIL, while an owner open explained by supply, or any native read, remains positive evidence), with the transformed-output hole stated, or (b) keep access semantics but add a verdict-level measure to item 8 (per form: rate of owner-access verdicts that are FAIL on honest forms) judged against a target, and add model-driven package scans to the reopen triggers and to the acceptance boundary. The stakeholder explicitly left the exemption to "the independent check and the multi-turn rehearsal"; my finding is that the rehearsal as specified cannot decide it. This is a stakeholder confirmation item (§7).

Non-blocking D3 clarifications (D4-delegable or one-line):
- Route (iii) and turn-ambiguity: not stated whether explanation is per file or per open (rows keep only first/last bracket), nor which candidate turn is used when an open is turn-ambiguous (any candidate vs the earliest). State per-file explanation for the first open and "any candidate turn" for route (iii) (lenient only where the whole file reached the model anyway); I verified that per-file explanation loses no consumption because content already supplied cannot be re-supplied.
- Item 3/7 claim the subject cannot influence the ledger and that access volume cannot grow the record. The kernel queue can overflow by subject volume if the drain stalls. I reproduced overflow (16 385 events, overflow flag) with 9 000 opens of two files while undrained, 3 events per open, `max_queued_events` 16384. Overflow is recorded as loss (fail-closed), but with replacement allowed an overflow is a subject-reachable laundering channel for an unobserved owner open. Residual to state; consider "overflow is replaceable only with disclosed cause".
- Supervisor/observer reads of package files during the marked window are indistinguishable from subject reads under inotify (no pid). State the premise that the supervisor opens no package file while marks are live and that marks outlive sandbox teardown.
- Heartbeats should carry unique names (kernel coalesces only consecutive identical events; my probe showed none coalesce when open/access/close interleave, but heartbeat bursts without other events could).
- D3 item 5 says the transform declares no auxiliary POSTs; contract item 12 allows auxiliary requests classified by frozen properties. Reconcile (request 0 = first subject-conversation request).
- Parameters that decide results (distinctiveness floor, clock tolerance, bracket bound, heartbeat period/gap, row bound) are "declared" but not required to be frozen before runs.

### Contract (revision 10)

**C-B1. Replacement and gate target are incompletely specified for the burden side and T7.** "T7 keeps its own pair-addition rule and is not extended by replacement" admits two readings: T7 inexact runs cannot be replaced at all, or they are handled only by added pairs. Under the first, one byte-inexact run among T7's 3 to 7 pairs per arm leaves the T7 fixed-cost claim and so the burden criterion non-PASS with no recourse. The gate target (0.8) is stated only for "owner-unresolved" runs; D3 item 8 lists the burden aggregation rule but the target does not cover it. T1/T7/T8 have only three pairs per arm per comparator, so the burden side is the more fragile. State the T7 reading and extend the target to the burden criterion.

**C-B2. Undeclared change in effect of a rev 8 floor.** Item 13 "Owner-access time": "Any open of an owner copy is owner access ... an owner access before the first predeclared R2 event is a zero-tolerance owner false activation." Rev 8 §4/§5 score an owner read. The amendment §1/§2 and §8 say item 13 "changes no threshold, floor, fixture" and the task framing "leaves revision 8 unchanged in effect". The extension is stakeholder-adopted (decision 3, which says "owner access") but it is an effect change and must be listed as such in the amendment's change table and in §8, with D3-B2's resolution. §8's "changes no threshold" is also inexact: the 0.8 gate target and the disparity bound are thresholds (labelled R-op; I find them permissible as recorder operationalizations because they are acceptance-process values, not outcome floors, but the sentence should say so).

**C-B3. Recomputation and single-owner gaps.**
- Item 13 says the contract does not restate D3 attribution rules, but its "Owner-access time" paragraph restates the owner-access rule (any open = access; bound = earliest consistent turn; first of native, supply and access bound). Two owners for one rule; any D3 repair of D3-B1 would have to be mirrored. Replace by a pointer.
- The `package_access` payload omits the parameters needed to recompute it independently (distinctiveness floor, clock tolerance, bracket-width bound, heartbeat period/gap bound, row bound) and the sandbox-teardown/mark-lifetime bounds. Item 11's accounting-code digest binds them only indirectly; an evaluator "able to recompute from retained artifacts alone" needs them in the event or the frozen profile.
- Not a blocker: the reduction claim. First/last bracket plus count per (file, flags) suffices for phase, first-open time and byte accounting; I found no oracle that needs a middle open once the per-file rule above is stated.

Checked and correct: §-citations in D3 and contract (owner floor and ambiguous R2 timing are in §4; fail-closed in §1 item 7; rerun cap in §5; item 4/5/11/§6/§8 pointers exist and say what the amendment's table says); item 12 "final criterion-level state after replacements" is consistent with item 13 replacement; the "no ledger" branch preserves the earlier claim-scoped inadmissibility.

### Workplan §0.1

**W-1 (conditional follow-up, not a blocker to the entry as written).** If access semantics are kept, the workplan's "any new-owner read before the trajectory's R2 point" (≈line 916) and the floor wording in §11.5 are not marked. Add a marker or one sentence in the §0.1 entry. The entry's own text, the two markers' placement and wording, and their pointers to §0.1 and contract item 13 are consistent with the overlay convention (bold governed-change paragraph, "pending Review", markers at affected bullets, number left to the Review, "no threshold" accurate for the workplan since the R-op values live in the contract/stakeholder records). The marker on the trusted-observation bullet keeps the "only approved independent boundary" for the model-facing fields intact and states the supervisor ledger observes supervisor-owned inputs; no frozen bytes changed.

## 3. Falsification summary (selected)

| Question | Result |
|---|---|
| Bracket soundness vs late drain | Sound: one inotify instance is a FIFO of kernel generation order (probe: heartbeat dir and package dir on one fd interleaved in exact operation order). A late drain cannot move an event outside [stamp before earlier heartbeat write, stamp after later heartbeat write]. Retries and parallel tool calls do not break it because results are delivered per request. |
| Mis-timing later than true turn | Yes, in the mapping, not the bracket: in-flight-window opens, opens after the last request, undeclared sub-tolerance clock steps (D3-B1b). |
| Unbounded/timing-loss owner open | Contradiction with "definite FAIL" (D3-B1). |
| Heartbeat realizable, unobservable | Yes: a second watch on a supervisor-private directory on the same fd. Subject can only widen brackets by CPU contention. Subject-volume overflow is a residual. |
| False owner access | Yes on `grep -r`/native scan (executed). No runtime rescan seen in a 7-request run; compaction untested. |
| Route (iii) shared-block failure | Not reintroduced: needs the file's whole content (≥48 B) in a same-turn result, so a shared kernel block or partial run never explains. Residual accepted by D3: content shown for a twin, or a file wholly contained in a larger shown file, explains an open and the bytes double count; premise "no owner line ≥48 B in a non-owner file" verified (0 of 242 lines). |
| Three-question split | No suppression path found: (A) null unless exact; (B) independent of attribution; (C) needs supply; UNRESOLVED applies only with no positive evidence. Except D3-B1, where unresolved is mislabelled definite. |
| Replacement exploitability | Selection effect exists: inexact forms (partial reads through non-literal paths) are replaced, biasing byte counts upward on all arms (conservative for the candidate, loosening the 6.5 denominator of the 2.0x bound) and biasing hit rates slightly downward. The frozen disparity bound with fail-closed default mitigates rate disparity but not behaviour shift; a report of burden sensitivity excluding replaced slots would be prudent. Positive evidence is never replaced; T7 ambiguity C-B1. |
| New forbidden threshold | None forbidden. Two R-op values (0.8, disparity bound) added; no outcome floor, exposure minimum or fixture changed. |
| Numbers | Verified from git archives: 7.0 candidate dist/skills 238 files / 63 distinct / 38 twin groups / 213 twinned; 6.6 ref 22f4bdb 212/62/37/187; 6.5 ref 7f7b5e2 198/60/35/173; no hard links; owner file in 7 copies, 45 958 B. "About 1,500 runs bound 0.2%" is the rule of three at 95%. |

## 4. Evidence

Executed (this context, applicable to the committed bytes only as noted):
- `python3 -m unittest test_package_ledger test_batch_cli` in qualification/ssdp70/eval: 40 tests OK (realizes rev 3 only; not evidence for rev 4).
- Real-OMP probes through `harness70.run_episode -> adapters.omp -> exact omp 18.0.11 -> observer -> stand-in provider`, scratch HOME with read-only runtime-closures symlink and `SSDP70_OMP_EXE`: (a) six bash turns, no post-request package open and exact observation; (b) background `cat owner` during a later tool window mapped to the right request index (3) and flagged inexact as designed; (c) `grep -rl` over the package opened 238 files, seven owner accesses, nothing shown (D3-B2). Probes are development evidence on the stand-in provider, not admission, and do not test rev 4 behaviour.
- Kernel micro-probe: inotify ordering across two directories on one fd, three events per open, overflow at 16 384.
- Package shape and owner-line premise computed from `git archive` of HEAD dist and the two ref trees.

Reused: none from earlier reviews.

Missing (not run, not counted): any rev 4 behaviour (heartbeat, bracket mapping, route (iii), split exactness fields, `package_access` event, replacement bookkeeping); compaction/long-session rescan; in-flight-window mis-timing race; live-drain overflow; timing-stress; real-provider behaviour.

## 5. Impact closure

Open: D3 acceptance (blocked by D3-B1/B2); contract revision 10 acceptance; stakeholder confirmation of two R-op values and the owner-access exemption decision; run count N and gate target instantiation; F-5; all D4 realization listed in the D3 rev 4 note; marker follow-up W-1; re-binding D4 evidence to the accepted tree. Unaffected: rev 8 text; revision 8's independent PASS still covers rev 8 only.

## 6. Independence and common-mode limits

I read only repository bytes and git history; I did not open the earlier reviews (`/tmp/SSDP70-*`) or any memory directory. Limits: the amendment §3 and D3 text under review summarize earlier findings and I read them, so I partly saw the authors' framing; I share model family with the authoring and prior-review contexts; the real-OMP probes use the same repository rig and a stand-in provider, so they share the D4 code's assumptions; Linux 6.8 host kernel only.

## 7. Recommend the stakeholder confirm

1. R-op: per-arm inexact-rate disparity bound frozen before runs, fail-closed default (acceptable as designed; confirm the number when chosen).
2. R-op: 0.8 gate target (acceptable; but extend it to the burden criterion and state the T7 reading, C-B1).
3. Not an R-op but needs a decision: whether any post-request open of an owner copy (including a package scan with no content shown) is a zero-tolerance owner false activation, or whether an unshown, unexplained owner open is UNRESOLVED/replaceable (D3-B2). Also that this extends rev 8's "owner read" to "owner access".
