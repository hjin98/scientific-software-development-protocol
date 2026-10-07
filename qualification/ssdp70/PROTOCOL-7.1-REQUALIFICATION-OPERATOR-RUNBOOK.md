---
kind: operator-runbook
role: operator (lighter model; mechanical execution only)
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (candidate; non-governing)
date_utc: 2026-10-06
owner_plan: PROTOCOL-7.1-REQUALIFICATION-PLAN.md
---

Governing SSDP version: 6.6.0.

# Protocol 7.1 requalification: operator runbook

**Your role.** You are the **operator**. You run commands exactly as written and record their verdicts. You make no decisions.
- Every judgment belongs to the analyst, the custodian, the independent checker or the stakeholder.
- When anything is not exactly as this runbook expects, you write an escalation and **stop**.
- Stopping is always correct. Guessing is always wrong.

## Rules (read every session)

1. **Phase scope.** Execute only the phase named in the analyst's current work order, its steps in order, each command **exactly** as written. All values come from the parameter file. Never type a hash, path, timeout, episode id or flag yourself.
2. **Pass condition.** A step passes only if its pass condition holds: normally exit 0 and `"verdict": "PASS"` in the saved JSON. Otherwise run `escalate <step-id> "<what you saw, facts only>"` and **stop the whole runbook**.
3. **What a stopped step forbids.** Never retry a step, rerun a command, change a flag, "fix" an input, delete an output or try an alternative. `gate` and `launch` refuse to repeat a step on purpose.
4. **Edit nothing outside `$WORK`.** Never edit, move or delete anything in the repository or in `$CUSTODY`. The only files you create are under `$WORK`, plus the access-log lines that `log_access` appends.
5. **Never open custody material.** Never open, print, list, grep or copy anything under `$CUSTODY/keys`, `$CUSTODY/authoring`, `$CUSTODY/human-trial`, `$CUSTODY/oracles` or `$CUSTODY/probes`. You only pass these paths to tools.
6. **Never judge results.** Never read run reports to judge them, never compare arms, never summarize results. Your report is the list of gate files.
7. **The harness only through `launch`.** Never run `harness70.py`, `batch_assess70.py` or any oracle directly. Never use `--mode probe` or `--only`.
8. **No git.** Never commit, push, stash, checkout or reset.
9. **Waiting.** When a step says WAIT, poll with `launch_status` at most every 10 minutes and do nothing else meanwhile. `RUNNING` means keep waiting. `CRASHED` (the launcher died without an exit code) is never a wait: `escalate <key> "launch status CRASHED"` and stop. If `launch` itself prints `STOP`, escalate and stop.
10. **Doubt is an escalation.** A step that seems wrong, ambiguous or impossible is an escalation, not a judgment call.

## Session start (every session, before any step)

```bash
source /home/samjin/agent-skills/scientific-software-development-protocol/qualification/ssdp70/requal71/campaign-parameters.env
source "$REPO/qualification/ssdp70/requal71/operator-lib.sh"
S=$(date -u +%Y%m%dT%H%M%SZ)
need REPO PY WORK && mkdir -p "$WORK"
export SSDP70_OMP_PROVIDER_CREDENTIAL="${SSDP70_OMP_PROVIDER_CREDENTIAL:-${DEEPINFRA_API_KEY-}}"
need SSDP70_OMP_PROVIDER_CREDENTIAL   # the provider API key; never print, echo or log it
gate "R0-pins-$S"  bash -c "cd '$REPO' && sha256sum -c --quiet qualification/ssdp70/requal71/tool-pins.sha256"
gate "R0-tests-$S" bash -c "cd '$EVAL_DIR' && '$PY' -m unittest test_requal71"
```

**Pass:** both `need` lines and both gates succeed.

- If `need` refuses because a value is `UNDECIDED`, the phase is not authorized yet: escalate.
- If `need SSDP70_OMP_PROVIDER_CREDENTIAL` refuses, the provider key is missing from your environment (the adapter reads `SSDP70_OMP_PROVIDER_CREDENTIAL`; it falls back to `DEEPINFRA_API_KEY`). Escalate; never type, print or paste a key yourself.

**Shorthands used below** (define them after session start):

```bash
K=$WORK/keys/omp-primary-flash-executor
KEYS="--key main=$K-main.json:$K-main.capabilities.json --key burden=$K-burden.json:$K-burden.capabilities.json --key routing=$K-routing.json:$K-routing.capabilities.json --key ordinary=$K-ordinary.json:$K-ordinary.capabilities.json"
RUNS="--runs $WORK/runs/main --runs $WORK/runs/burden --runs $WORK/runs/routing --runs $WORK/runs/ordinary"
```

## Custody snapshot procedure (contract §1 item 9(c); used by P3, P5, P6, P9)

Around **every** session of another role that touches `$CUSTODY`, and you receive the role name and session number `<n>` in the work order:

```bash
need CUSTODY && mkdir -p "$CUSTODY" "$WORK/custody"
gate "SNAP-<n>-before" $RQ custody-stat --store "$CUSTODY" --out "$WORK/custody/<n>-before.json"
#   ... the other role works; you wait for the analyst's message that it has finished ...
gate "SNAP-<n>-after"  $RQ custody-stat --store "$CUSTODY" --out "$WORK/custody/<n>-after.json"
```

**Nothing may change between two role sessions.** For every `<n>` after the first:

```bash
gate "SNAP-<n>-between" $RQ custody-compare --before "$WORK/custody/<n-1>-after.json" --after "$WORK/custody/<n>-before.json" --append-only ACCESS-LOG.md
```

**After the custodian's freeze (C-6),** every role session must also leave the store unchanged except for log growth:

```bash
gate "SNAP-<n>-session" $RQ custody-compare --before "$WORK/custody/<n>-before.json" --after "$WORK/custody/<n>-after.json" --append-only ACCESS-LOG.md
```

## Phase D (optional; only if the work order says "Phase D", stakeholder SD-5)

The analyst provides `$WORK/dev/commands.json` (development-purpose harness commands) and lists its keys.

For each listed key, in order:

```bash
launch "$WORK/dev/commands.json" <key>     # WAIT until: launch_status <key>  shows EXIT or CRASHED
```

- **Continue** if the exit is `EXIT 0` or `EXIT 2`.
- **Stop** on any other exit: `escalate <key> "dev launch exit <n>"`.
- **Stop** on `CRASHED`: `escalate <key> "launch status CRASHED"`.
- Use `launch_fg` instead of `launch` only when the analyst's work order says so.
- Report "Phase D complete" with the list of `$WORK/launch/*`.

## Phase P3: fresh custody and corpus (after the custodian's hand-over C-6)

```bash
need CUSTODY
gate P3-freeze freeze_check
gate P3-corpus $RQ corpus-check --corpus "$CUSTODY/corpus" --requirements "$CUSTODY/requirements" --disclosed "$DISCLOSED"
```

**Pass:** both PASS. Report "P3 complete".

## Phase P4: arms, keys, family, accounting manifest

```bash
need P71_ARM TIMEOUT_MAIN TIMEOUT_BURDEN TIMEOUT_ROUTING TIMEOUT_ORDINARY CUSTODY
gate P4-arms $RQ prepare-arms --arm "$P65_ARM" --arm "$P66_ARM" --arm "$P71_ARM" --expect "$P65_SHA" --expect "$P66_SHA" --expect "$P71_SHA" --out "$WORK/arms"
gate P4-key-main     $RQ derive-key --source-profile "$SOURCE_PROFILE" --source-capabilities "$SOURCE_CAPS" --panel main     --timeout-s "$TIMEOUT_MAIN"     --out-dir "$WORK/keys"
gate P4-key-burden   $RQ derive-key --source-profile "$SOURCE_PROFILE" --source-capabilities "$SOURCE_CAPS" --panel burden   --timeout-s "$TIMEOUT_BURDEN"   --out-dir "$WORK/keys"
gate P4-key-routing  $RQ derive-key --source-profile "$SOURCE_PROFILE" --source-capabilities "$SOURCE_CAPS" --panel routing  --timeout-s "$TIMEOUT_ROUTING"  --out-dir "$WORK/keys"
gate P4-key-ordinary $RQ derive-key --source-profile "$SOURCE_PROFILE" --source-capabilities "$SOURCE_CAPS" --panel ordinary --timeout-s "$TIMEOUT_ORDINARY" --out-dir "$WORK/keys"
gate P4-family   $RQ family-build $KEYS --out "$WORK/family.json"
gate P4-manifest $RQ campaign-build --family "$WORK/family.json" --corpus "$CUSTODY/corpus" --requirements "$CUSTODY/requirements" --arms-manifest "$WORK/arms/arms.json" --lineage "$LINEAGE" --out "$WORK/accounting-manifest.json"
```

**Pass:** all seven PASS. Report "P4 complete" with `family_id` and `accounting_manifest_sha256` copied from the gate JSON.

## Phase P5: admissions (evidence only; you never admit anything)

The independent checker gives you `$WORK/admission/work-order.json`, in the same format as a matrix plan (`{"commands": [{"key": ..., "argv": [...]}]}`).

For each key **in the listed order**:

```bash
launch "$WORK/admission/work-order.json" <key>     # WAIT until EXIT
```

- **Continue** only on `EXIT 0`. Anything else: `escalate <key> "admission step exit <n>"`.
- When the list is done, report "P5 evidence complete".
- The checker finalizes the bundles. The analyst then sets the `ADM_*` and `EVAL_*` parameters and re-pins the tools.

## Phase P6: freeze and pre-launch verification (after the checker's PASS report)

```bash
need ADM_MAIN ADM_BURDEN ADM_ROUTING ADM_ORDINARY PARALLEL CUSTODY
gate P6-freeze freeze_check
gate P6-candidate-frozen $RQ set-freeze-gate --gate "$CUSTODY/FREEZE-GATE.json" --field candidate_frozen
ADMS="--admission main=$ADM_MAIN --admission burden=$ADM_BURDEN --admission routing=$ADM_ROUTING --admission ordinary=$ADM_ORDINARY"
gate P6-verify $RQ verify-launch --accounting-manifest "$WORK/accounting-manifest.json" $KEYS $ADMS --corpus "$CUSTODY/corpus" --arms-manifest "$WORK/arms/arms.json" --freeze-gate "$CUSTODY/FREEZE-GATE.json"
gate P6-plan   $RQ matrix-plan --accounting-manifest "$WORK/accounting-manifest.json" $KEYS $ADMS --corpus "$CUSTODY/corpus" --arms-manifest "$WORK/arms/arms.json" --requirements "$CUSTODY/requirements" --oracles "$CUSTODY/oracles" --out-root "$WORK/runs" --parallel "$PARALLEL" --out "$WORK/matrix-plan.json"
```

**Pass:** all four PASS. Report "P6 complete".

## Phase P7: qualification launch

```bash
log_access operator "oracles/ (read by the harness after each run)" "P7 qualification launch"
launch "$WORK/matrix-plan.json" main        # WAIT until EXIT
launch "$WORK/matrix-plan.json" burden      # WAIT until EXIT
launch "$WORK/matrix-plan.json" routing     # WAIT until EXIT
launch "$WORK/matrix-plan.json" ordinary    # WAIT until EXIT
```

- After each launch, **continue only on `EXIT 0` or `EXIT 2`**. Exit 2 means some run was not complete, which is normal; `audit` reports it.
- Any other exit: `escalate <key> "matrix exit <n>"` and stop. Do not launch the remaining keys.
- After all four:

```bash
gate P7-audit $RQ audit $RUNS --accounting-manifest "$WORK/accounting-manifest.json" --corpus "$CUSTODY/corpus" --out "$WORK/audit-runs.json"
```

- **If P7-audit is STOP:** `escalate P7-audit "post-run audit stopped"` and stop. The analyst decides, under the contract, what a non-complete or undelivered run means. You never rerun anything.
- **If PASS:**

```bash
gate P7-output-frozen $RQ set-freeze-gate --gate "$CUSTODY/FREEZE-GATE.json" --field frozen_run_output_exists --audit "$WORK/gates/P7-audit.json"
```

Report "P7 complete".

## Phase P9: blinded evaluation

```bash
need EVAL_PROFILE EVAL_CAPS EVAL_ADMISSION
gate P9-plan $RQ eval-plan --accounting-manifest "$WORK/accounting-manifest.json" --runs-root "$WORK/runs" --out-root "$WORK/assessments" --keys "$CUSTODY/keys" --evaluator-profile "$EVAL_PROFILE" --evaluator-capabilities "$EVAL_CAPS" --evaluator-admission "$EVAL_ADMISSION" --parallel "$PARALLEL" --out "$WORK/eval-plan.json"
log_access evaluator "keys/ (via batch_assess70.py; operator does not open them)" "P9 blinded evaluation"
launch "$WORK/eval-plan.json" main          # WAIT until EXIT; continue only on EXIT 0, else escalate
launch "$WORK/eval-plan.json" burden        # same
launch "$WORK/eval-plan.json" routing       # same
launch "$WORK/eval-plan.json" ordinary      # same
gate P9-audit $RQ audit $RUNS --accounting-manifest "$WORK/accounting-manifest.json" --corpus "$CUSTODY/corpus" --assessments "$WORK/assessments/main" --assessments "$WORK/assessments/burden" --assessments "$WORK/assessments/routing" --assessments "$WORK/assessments/ordinary" --out "$WORK/audit-assessed.json"
```

**Pass:** P9-audit PASS. Report "P9 complete".

## Phase P10: aggregate

```bash
need AGGREGATE_CMD
gate P10-aggregate bash -c "$AGGREGATE_CMD"
```

- **Exit 0 or exit 1** (the oracle reached a PASS or a non-PASS outcome): report "P10 complete" with `$WORK/gates/P10-aggregate.json`.
- **Any other exit** (exit 3 means the oracle refused its input): escalate.
- You report the file path, never the outcome.

## Escalation packet

`escalate` writes `$WORK/escalations/<time>-<step>.md`, containing:
- the verdict JSON verbatim;
- the stderr or log tail;
- your one-line factual note.

After writing it, send the analyst only the packet path and stop. Do not add analysis, guesses or proposed fixes.
