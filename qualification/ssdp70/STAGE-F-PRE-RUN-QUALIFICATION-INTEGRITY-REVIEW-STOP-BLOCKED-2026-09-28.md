---
kind: independent-stage-f-pre-run-qualification-integrity-review
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: F-pre-run
result: STOP/BLOCKED
review_date: 2026-09-28
reviewed_branch: ssdp-7.0-scientific-epistemic-closure
reviewed_tooling_head: 1d2ac73ceabb8efce40005540c118e5fbfc407af
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
comparison_subjects:
  protocol_6_5: 7f7b5e24858e813e45ace867a7f8ea5180f43bf0
  protocol_6_6: 22f4bdba53795da3a6f13f162529f3a843fc37ae
active_serious_challenge: none
---

# Protocol 7.0 Stage F pre-run qualification-integrity review — STOP/BLOCKED

## Disposition

**STOP/BLOCKED. Do not begin the fresh 6.5/6.6/7.0 comparative qualification campaign.**

This review independently reconstructed the governing repository authority and inspected the Stage F qualification machinery at exact branch head `1d2ac73ceabb8efce40005540c118e5fbfc407af`. It did not inherit a prior agent's PASS/NO-PASS conclusion. No Protocol 7 candidate run, paired 6.5/6.6 run, scoring run, or human-trial exposure was performed.

Two classes of blocker prevent a genuine pre-run PASS:

1. required independent withheld evidence and actual-harness execution are unavailable in this review environment; and
2. the reviewed D4 qualification tooling contains fail-open paths that can make wrong-subject, incomplete, or insufficient evidence look admissible enough to proceed.

The immutable semantic candidate `db94a2d...` was not changed.

## Authority and exact subjects reconstructed

The governing workplan is `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`. Its `protocol_version` is 6.6.0 and its target is 7.0.0. Root `AGENTS.md`, the active authority index, `PROTOCOL-RELEASE-STATE.yaml`, the Stage F qualification contract, the single-participant stakeholder decision, its independent contract recheck, and the Stage A/Stage E records were read as current routing/evidence.

The immutable execution subjects supplied by `prepare_arms70.py` are correct:

- 6.5: `7f7b5e24858e813e45ace867a7f8ea5180f43bf0`, expected 6.5.0;
- 6.6: `22f4bdba53795da3a6f13f162529f3a843fc37ae`, expected 6.6.0;
- 7.0: `db94a2dfb7fef480f37227eab5c45256e89901b8`, expected 7.0.0.

Independent repository inspection also found exactly the same seven SSDP skill package names at all three immutable refs. `prepare_arms70.py` resolves each ref to a commit, checks `source/PROTOCOL_VERSION`, archives `dist/skills`, verifies each expected package `PROTOCOL_VERSION`, and records a package-tree digest. These are sound positive controls.

## Required withheld and execution evidence unavailable

The Stage A independent framework recheck explicitly left the following for Stage F pre-run: withheld classification rationale; every exposure denominator; per-R2 class assignments; unnamed eligibility; critical keys and acceptable dispositions; oracle branches and R2 events; withheld route classes; the human-trial material; every actual-harness known-good/known-broken branch probe; complete-capture and side-effect probes; ordinary-entry probes; and the chained-delegate cheap-first-look probe.

The later single-participant human-trial recheck also explicitly says that the actual one-participant material still needs a withheld check covering the random draw, matched templates, frozen questions/answers, time protocol, and permitted assistance.

Those custody materials are not available to this review environment. The designated out-of-repository custody directory is not mounted here. The local execution environment also has no `claude` executable and no repository clone from which the actual Stage F runner can be executed; direct GitHub network access from the execution container is unavailable. Repository authority could be inspected through the connected GitHub interface, but that does not substitute for the required custody or actual runner.

Per the frozen contract, synthetic or self-authored fixtures cannot replace these checks. None was used to manufacture qualification evidence.

## D4 qualification-tooling blockers found by hostile review

These defects are independently blocking even after custody/execution access is restored.

### F1 — run identity does not bind the immutable subject identity

`prepare_arms70.py` records the resolved commits in `arms.json`, but `harness70.py` does not consume or bind that manifest. A run identity contains an arm label and `dist_tree_sha256`, but not the requested/resolved protocol commit or the prepared-arm manifest identity.

Therefore two different semantic subjects that happen to yield the same generated package tree are cache-equivalent, and a mislabeled package tree can be run without the run record proving which immutable ref supplied it. This violates exact-subject evidence binding even though package-byte identity is recorded.

The recent `1d2ac73...` repair correctly added replicate and pair-order identity, but it did not close this subject-provenance gap.

### F2 — cache identity omits material executor/reasoning identity

The run identity binds the model string, episode configuration, fixture/stub/oracle/package trees, harness file hashes, tool allow/disallow lists, replicate and pair order. It does not bind the actual Claude Code runner/version or an explicit reasoning/thinking mode, although the qualification contract requires execution conditions including reasoning mode to be declared.

A cache can therefore remain "exact" across a material runner/default-reasoning change that can alter tool semantics or trajectory behavior.

### F3 — an incomplete executor trace can become `admissible: true`

`run_episode` sets:

`execution_ok = proc.returncode == 0 and not bool(summary.get("is_error"))`

The inherited trace parser returns an empty/default result record when no terminal `type=result` event exists. With process exit 0 and an init event sufficient for catalog isolation, the absence of a terminal result is not itself rejected. Such an incomplete trace can therefore satisfy both `execution_ok` and catalog isolation and become admissible.

This violates the rule that incomplete traces and execution failures cannot masquerade as admissible evidence.

### F4 — matrix status prints `ok` for an inadmissible completed run

`run_pair` appends `("...", "ok")` whenever `run_episode` returns without raising, regardless of `summary["admissible"]`. A run whose summary says execution/catalog admissibility failed can therefore be surfaced by matrix orchestration as `status: "ok"`.

The cache correctly refuses such a run later, but the orchestration status is still a false-green state representation.

### F5 — evaluator bundle construction is fail-open for missing evidence

`assess70.prepare_bundle` copies each expected evidence item only `if src.exists()`. Except for the summary that is read before bundle construction, missing final report, diff/new-file evidence, side-effect log, raw trace, tool-call log, oracle output, issue state, or final tree does not cause assessment to fail closed.

The evaluator prompt says the complete bundle is available, but the wrapper does not prove that statement. A missing artifact can therefore silently disappear from the manifest instead of becoming `MISSING/INADMISSIBLE`.

### F6 — evaluator schema permits omitted scoring obligations

`validate_verdict` validates each returned disposition but does not require any disposition to exist or require the returned item set to cover the frozen key/rubric obligations. An empty `dispositions: []` object with otherwise valid fields passes schema validation.

Without an independently enforced exact expected-item set, a malformed/incomplete evaluation can omit a critical branch rather than producing FAIL/UNRESOLVED/MISSING.

### F7 — deterministic oracle output is truncated before durable assessment

For each deterministic oracle, `harness70.py` stores the pass bit and return code but truncates stdout to the last 2000 characters and stderr to the last 1000 characters in `oracle.json`. No separate complete oracle stdout/stderr artifacts are retained.

A failing return code remains a failure bit, so this does not directly flip FAIL to PASS, but it violates the required complete deterministic-oracle evidence path and can conceal the detail needed to interpret a critical failure or distinguish oracle defect from subject defect.

### F8 — external write/network containment is not complete

The contract requires sandboxed stand-ins/capture that can detect unauthorized external writes and network actions. The current harness does not establish such a containment boundary. It post-processes tool-call text with regular expressions.

A focused tooling counterexample (not a qualification fixture) showed that the current detector misses, among others:

- a relative shell escape such as `printf x > ../escaped.txt`;
- `cp source.txt ../escaped.txt`;
- Python `open("../escaped.txt", "w")`;
- dynamically constructed Python network use that avoids the literal network regex.

Because `Bash(python:*)` and `Bash(git:*)` remain executable capabilities, command-text matching is not equivalent to filesystem/network containment or complete side-effect capture. This is a path-containment and unrecorded-side-effect hole.

### F9 — owner-load summary can miss a real owner read

`new_owner_read_indices` is computed from the inherited reduced trace. That reducer truncates each tool input to 400 characters. A tool call whose full input contains `scientific-inspectability-and-initiative.md` after character 400 is present in the complete raw tool-call evidence but absent from the reduced input used by `owner_reads`.

A focused unit counterexample confirmed this exact false negative. That can corrupt the owner-load and false-activation summary, including the zero-tolerance early-owner-read condition. The complete raw trace makes later manual recovery possible, but the current metric is not trustworthy as its own oracle.

### F10 — deterministic-oracle collection is optional at run level

`--oracles` is optional, and an episode with no supplied oracle directory remains run-admissible. `summary["oracle_collection"]` can be empty without changing admissibility. Combined with F5/F6, a required deterministic oracle that was never supplied or collected is not mechanically prevented from flowing into assessment as though the run were complete.

The contract requires a required check that did not execute to remain non-PASS.

## Positive integrity findings

The hostile review also found important protections that are implemented correctly at `1d2ac73...`:

- exact 6.5/6.6/7.0 extraction refs and package-version checks are correct in `prepare_arms70.py`;
- the current three immutable refs each contain exactly the seven expected SSDP skill packages;
- `run_identity` binds manifest, episode configuration, fixture tree, stub tree, package tree, episode-oracle tree, both harness files, stub tools, model, tool policy, replicate and pair order;
- `cache_valid` requires exact identity equality plus prior `execution_ok` and `admissible`;
- the `1d2ac73...` repair correctly prevents cache reuse across replicate and counterbalanced order;
- `matrix_plan` records pair order, and `run_pair` executes arms sequentially inside each episode/replicate pair;
- parallelism is only across distinct pairs with separate temporary projects and output directories;
- normal completed runs retain full raw stream trace, a full tool-call-input log, final report, intent-to-add diff/new-file content, final tree, side-effect log and issue-store state;
- the evaluator model is restricted to `Read Glob Grep` and denied shell/write/network/skill/agent tools, so its model-facing evidence access is read-only;
- assessment wrapper execution errors, unparseable JSON, and invalid schema are distinct nonzero statuses rather than PASS.

These positives are insufficient to override the blockers above.

## Harness discrimination and prose-only judgments

The required actual known-good/known-broken discrimination matrix was **not executable in this review environment**, so no branch-level PASS is claimed. In particular, there is no valid evidence here for the both-arms-miss critical subgroup, wrong binding/O3, null/variant/delegate-gap, false tension closure/asserter, destructive-boundary loss, unauthorized write, version self-adoption, designed termination, ordinary-entry per-case capture, or chained-delegate cheap-first-look branches.

Some Stage F judgments are honestly not fully mechanical and should remain key-bound independent evaluation rather than be converted into shallow string tests. Examples include:

- whether a limitation is sufficiently specific and whether the omitted area really lay outside a cheap first look;
- whether a planted mechanism is genuinely out-of-list rather than a disguised listed mechanism;
- semantic claim-integrity/misleading-projection judgments in free-form scientific prose;
- some tension applicability/binding judgments whose correctness depends on the implicated authority rather than a path token.

Those branches still require executable known-good/known-broken *trajectories* around the evaluator/rubric path, but the final semantic judgment may legitimately remain evaluator-owned.

## Protocol-specific Stage F invariants

From source inspection, the normal evidence bundle is capable of carrying ordinary-entry skill selection, raw owner-read evidence and final outcome; scripted delegate requests are fully logged; and issue-state mutations are captured by the issue stand-in. However F9 makes the derived owner-read metric unsafe, and the required actual ordinary-entry/chained-delegate probes have not run. Owner-load floors, false-activation floors and inherited 6.6 preservation therefore remain unqualified.

No claim is made that the cheap-first-look hidden-anomaly behavior or all 6.6 preservation obligations are currently discriminated.

## Human-trial readiness

The **framework** is internally consistent with the stakeholder's single-participant decision and the independent revised-contract recheck:

- stakeholder is the sole participant;
- exactly one different fixture per arm;
- a pre-exposure random draw fixes fixture assignment and arm order;
- at least 20 routine and 4 critical questions per arm;
- zero materially wrong critical answers;
- at least 80% routine correctness;
- candidate median answer time no more than 2.0 times baseline;
- unanswered questions are wrong except a recorded non-material non-completion produces a non-discriminating, never-PASS trial;
- assistance, unblinding, arm order and time must be recorded.

But the recheck itself says the actual custodian human-trial material remains pending. This review could not inspect the randomization record, matched templates, frozen questions/answers, permitted assistance, timing protocol, or custody-access attestation. No frozen answer or solution-bearing custodian material was exposed to this reviewer.

The recheck's minor ambiguity over who adjudicates a non-completion reason as unrelated to the material also remains; it is not by itself a framework blocker, but the actual trial plan should assign that assessment to the custodian/evaluator rather than the participant alone.

## Repair disposition

No D4 tooling repair was committed by this reviewer.

The defects above are generally within qualification-tooling authority, but this environment cannot run the required affected harness regression, cannot access the withheld oracle/key material, and cannot supply a fresh independent post-repair reviewer. Editing the harness here and then self-accepting the repair would violate the same independence and evidence rules this gate is meant to enforce.

The correct next cycle is:

1. restore a runner with the exact repository and independent custody mounted, while keeping the candidate author blind to solution-bearing material;
2. repair F1–F10 without weakening the frozen qualification contract;
3. run focused tooling regression plus the required actual-harness known-good/known-broken, containment, capture, ordinary-entry and chained-delegate probes against the withheld corpus;
4. have a fresh context that authored neither the candidate/fixtures nor those repairs perform the exact-commit pre-run recheck;
5. begin the 6.5/6.6/7.0 campaign only if that recheck returns genuine PASS.

## Gate state

```text
SERIOUS CHALLENGE: NONE
SEMANTIC CANDIDATE: db94a2dfb7fef480f37227eab5c45256e89901b8 — UNCHANGED
REVIEWED TOOLING HEAD: 1d2ac73ceabb8efce40005540c118e5fbfc407af
WITHHELD-INSTANCE CHECKS: UNAVAILABLE / NOT RUN
ACTUAL-HARNESS DISCRIMINATION: UNAVAILABLE / NOT RUN
HUMAN-TRIAL MATERIAL CHECK: UNAVAILABLE / NOT RUN
D4 TOOLING HOSTILE REVIEW: BLOCKING DEFECTS F1–F10
COMPARATIVE QUALIFICATION CAMPAIGN: NOT AUTHORIZED TO START
STAGE F PRE-RUN GATE: STOP/BLOCKED
```
