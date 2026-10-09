# SSDP 7.2 qualification campaign: operator hand-off (flash-tier operator)

Governing SSDP version: 6.6.0. This file is data. It tells you exactly what to type and when to stop. It gives you no authority to choose, edit, retry, skip, interpret or fix anything.

**Status: NOT READY.** Do nothing in sections 5 onwards until the file `$W/READY` exists. The analyst writes it. Its text says what phase you may start (section 3). If it is missing, or the text is not exactly what a step asks for, stop and tell the stakeholder.

## 0. The rules. Read them twice. They matter more than any step.

1. **Type the commands in this file exactly.** Do not change a path, an option or a number. Do not "improve" a command.
2. **Anything not exactly as expected is a STOP.** A STOP means: write an escalation packet (section 10), tell the stakeholder, and wait. Do not retry. Do not relaunch. Do not try to fix it. Do not guess the cause.
3. **Never delete, move, rename or edit anything** inside `$W/runs/` or `$S`. They are evidence.
4. **Never open or list** these places: `$S/keys`, `$S/authoring`, `$S/human-trial`, `~/ssdp72-fixture-custody`, `~/ssdp71-fixture-custody`, `~/ssdp70-fixture-custody`, any `oracles/` directory. The tools read what they need. You hand them paths. You do not read fixtures, answers or oracles.
5. **Run live commands from your own terminal**, not inside a tool that can be shut down (an agent tool shutting down killed an earlier launch). Keep the terminal open until the command says it is finished.
6. **The credential** is an API key in your shell variable `SSDP70_OMP_PROVIDER_CREDENTIAL`. Never print it, never write it to any file, never paste it into any message or packet. If a command output shows it, stop and tell the stakeholder.
7. **You never rerun a lost run.** Only the analyst decides reruns.
8. **You never score, interpret or summarize results.** You run, record and send back.
9. **At most 8 runs are in flight.** The plan enforces it. Never start a second copy of a runner.
10. If your session or machine goes down at any time: do not relaunch anything. Write a packet and ask.

## 1. What this campaign is, in four lines

- A model called **GLM-5.3-Flash** (the executor) is run on about 640 small coding tasks under three protocol versions (candidate 7.2, baseline 6.6 twice, and old 6.5 on a few tasks).
- A second model, **DeepSeek V4.1 Flash** (the evaluator), then reads the finished runs and judges what code cannot.
- The analyst scores everything. You operate the machinery.
- Cost: about $30 in total. Time: about 5 to 8 hours of runs, in two stages.

## 2. Paths (set these first in every new terminal)

```bash
export REPO=$HOME/agent-skills/scientific-software-development-protocol
export W=$HOME/ssdp70-omp-stagef/qualification/campaign-72-20261008
export Q=$REPO/qualification/ssdp70/qual-v2
export S=$HOME/ssdp72b-fixture-custody
cd $REPO
```

Expected identities (the analyst printed these; they must match):

| Item | Value |
|---|---|
| Candidate arm p72 | version 7.2.0, commit `2dedcfa3408f62bc11a696ac3776183a87b40438`, dist tree `69a310a26eb22be395b0a9b98603d8b58dd53171657bfb068ce5821518c5f622` |
| Baseline arms p66 and p66b | version 6.6.0, commit `22f4bdba53795da3a6f13f162529f3a843fc37ae`, dist tree `e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083` |
| Old arm p65 | version 6.5.0, commit `7f7b5e24858e813e45ace867a7f8ea5180f43bf0`, dist tree `7d61d8b7b19dfe40714e71daa2c46d0e4cdd62efebd96b8e96dfe3f33550429b` |
| Executor | `deepinfra/zai-org/GLM-5.3-Flash`, 60 turns, 2400 s, profile sha256 `b96dcb43155f452eec121307b83df56ff3f79ca308f6c4555206a5871088b107` |
| Evaluator | `deepinfra/deepseek-ai/DeepSeek-V4.1-Flash`, 20 turns, 1800 s, profile sha256 `a0db2d61d9cefbe975afac29adbc5dba1f4a1560078e92a15a6fdf22bbe83864` |
| Both models use | one provider (deepinfra) and the one credential variable `SSDP70_OMP_PROVIDER_CREDENTIAL` |

The preflight (section 4) checks these for you.

## 3. The phases and what READY must say

The analyst writes one line in `$W/READY` per phase you may start. You may only do a phase whose line is present.

| Phase | READY line | Section |
|---|---|---|
| Evaluator calibration (Precondition C(b)) | `CALIBRATION MAY START` | 5 |
| Stage 1: main panel | `OPERATOR MAY LAUNCH` | 6 |
| Evaluator pilot and pass | `EVALUATION MAY START` | 7 |
| Stage 2: preservation panels | `STAGE 2 MAY START` (and the file `$W/authorizations/stage2.ok`) | 8 |

Look at it any time with `cat $W/READY`.

## 4. Pre-flight (checks only; a key is needed only where stated)

Run this before every phase. It prints OK or STOP per line.

```bash
python3 $Q/prepare_campaign.py preflight --work $W --phase launch --custody $S
```

Before section 5 use `--phase calibration` instead, before sections 7 and 8 use `--phase evaluation`, and add `--need-credential` before any command that spends money:

```bash
python3 $Q/prepare_campaign.py preflight --work $W --phase evaluation --custody $S --need-credential
```

- Last line `RESULT: ALL OK`: go on.
- Any `STOP` line, or any other last line: STOP. Packet (section 10) containing the whole output.

Write this into your notes at the start of every session: `cd $REPO && git status --short && git rev-parse HEAD`

## 5. Evaluator calibration (Precondition C(b)): only when READY says `CALIBRATION MAY START`

Purpose: show the evaluator model is a fair judge before it judges anything. It takes the custodian's 40 test items. About 40 short model calls, well under a dollar.

```bash
export SSDP70_OMP_PROVIDER_CREDENTIAL=...        # given to you by the stakeholder; never print it
python3 $Q/prepare_campaign.py preflight --work $W --phase calibration --custody $S --need-credential
mkdir -p $W/calibration
python3 $Q/campaign_cb.py run --work $W --view-dir $S/calibration/cb-set/items --rubric $S/keys/SHARED-RUBRIC.txt --task-doc $S/calibration/cb-set/EVALUATOR-TASK.md --out $W/calibration/cb-results.json --parallel 4
python3 $S/operator/score_cb.py $W/calibration/cb-results.json | tee $W/calibration/cb-score.json
python3 $Q/campaign_cb.py cost --work $W --traces $W/calibration/cb-traces --price-in 0.20 --price-cached 0.006 --price-out 0.60 | tee $W/calibration/cb-cost.json
```

(The items directory is what the evaluator sees; the tool reads the rubric and the task description. You never open `$S/keys` yourself.)

Expected: `campaign_cb.py run` prints a line with `"invalid": 0` or a small number; `score_cb.py` prints counts only. **Do not judge the score.** Copy all three outputs into a packet named `calibration-result` and tell the stakeholder. The analyst decides whether the evaluator passed (the bar is 35 of 40 agreement and 8 of the 10 designated failures caught; two attempts at most) and writes the next READY line.

If `campaign_cb.py run` exits with an error, or `score_cb.py` exits with 3: STOP, packet.

## 6. Stage 1: the main panel (366 runs): only when READY says `OPERATOR MAY LAUNCH`

```bash
export SSDP70_OMP_PROVIDER_CREDENTIAL=...
python3 $Q/prepare_campaign.py preflight --work $W --phase launch --custody $S --need-credential      # must end: RESULT: ALL OK
python3 $Q/campaign_run.py $W start 1
```

It must print `started the sequential runner for stage 1 (pid N)`. Anything else: STOP. **Never run `start 1` twice.**

Watch it every 10 to 15 minutes and save every output in your notes:

```bash
python3 $Q/campaign_run.py $W status
```

Each line shows a command key and RUNNING, EXIT 0, EXIT 2 or CRASHED:

- `EXIT 0`: that command finished and all its runs are fine.
- `EXIT 2`: it finished and at least one run was not admissible (for example a provider error). The runner continues by itself. Note the key in your notes. Do not touch the runs.
- `CRASHED`, or a `HALT` line at the bottom: the runner stopped. STOP, packet. Do not restart.
- `DONE-stage1` at the bottom: stage 1 is finished.

You may leave the terminal alone between checks. Do not stop the runner.

After `DONE-stage1`:

```bash
python3 $Q/prepare_campaign.py verify --work $W --map $S/operator/gate-map.json --stage 1
echo "exit=$?"
python3 $Q/prepare_campaign.py report --work $W
```

Expected: no `INTEGRITY` finding and `exit=0`, or exit 4 with only `RERUN_PENDING`, `UNRESOLVED` or `INADMISSIBLE` findings. `UNRESOLVED` is normal until the evaluator has run. Send everything to the analyst. Exit 3, or any `INTEGRITY` finding: STOP, packet. **You do not decide what findings mean.**

## 7. Evaluator pilot and pass: only when READY says `EVALUATION MAY START`

The evaluator reads each finished run on the main panel. First a pilot of 5 runs to measure the real cost.

```bash
export SSDP70_OMP_PROVIDER_CREDENTIAL=...
python3 $Q/prepare_campaign.py preflight --work $W --phase evaluation --custody $S --need-credential
EV="--keys-root $S/keys --evaluator-profile $W/keys/omp-evaluator-readonly.json --evaluator-capabilities $W/keys/omp-evaluator-readonly.capabilities.json --shared-rubric $S/keys/SHARED-RUBRIC.txt"
python3 $Q/campaign_assess.py run $W $EV --panels main --parallel 4 --limit 5
python3 $Q/campaign_assess.py cost $W --panels main --price-in 0.20 --price-cached 0.006 --price-out 0.60
```

(`--keys-root` lets the tool copy one episode's key into the evaluator's sandbox. You do not open it.)

**Stop here.** Copy both outputs into a packet named `evaluator-pilot`. The analyst writes `$W/authorizations/evaluator-full.ok` if the cost is acceptable. Only when that file exists and READY still says `EVALUATION MAY START`:

```bash
python3 $Q/campaign_assess.py run $W $EV --panels main --parallel 4
python3 $Q/campaign_assess.py collect $W --panels main --out $W/dispositions-stage1.json
python3 $Q/campaign_assess.py cost $W --panels main --price-in 0.20 --price-cached 0.006 --price-out 0.60
```

Expected: `collect` prints `"problems": []`. Any problem entry goes into the packet exactly as printed. You never rerun an assessment.

## 8. Stage 2: the preservation panels (274 runs): only when READY says `STAGE 2 MAY START`

Stage 2 follows stage 1 as soon as the analyst has looked at your stage-1 verify output and written the READY line. The analyst does not score the candidate between the stages. If the stage-1 verify output has an INTEGRITY finding, the analyst will not release stage 2; that is a normal outcome, not an error.

```bash
ls $W/authorizations/stage2.ok                    # must exist
export SSDP70_OMP_PROVIDER_CREDENTIAL=...
python3 $Q/prepare_campaign.py preflight --work $W --phase launch --custody $S --need-credential
python3 $Q/campaign_run.py $W start 2
```

Watch with `campaign_run.py $W status` exactly as in section 6 until `DONE-stage2`. Then:

```bash
python3 $Q/prepare_campaign.py verify --work $W --map $S/operator/gate-map.json --stage 2 [--include-conditional <keys the analyst authorized and you ran>]
echo "exit=$?"
python3 $Q/prepare_campaign.py report --work $W
```

Then, for the versioning and sentinel panels only, when READY says `EVALUATION MAY START` again (and `evaluator-full.ok` is still there):

```bash
python3 $Q/campaign_assess.py run $W $EV --panels versioning sentinels sentinels-add --parallel 4
python3 $Q/campaign_assess.py collect $W --panels main versioning sentinels sentinels-add --out $W/dispositions.json
```

(`EV` is the variable defined in section 7. Set it again in a new terminal.)

## 9. Extra runs and reruns (only on the analyst's instruction)

- **Conditional runs** (extra T7 pairs, extra sentinel and lookup runs; each command holds two episodes, so they come one small command at a time): the analyst writes `$W/authorizations/<key>.ok`. Then, and only then: `python3 $Q/campaign_run.py $W run-conditional <key>`. The tool refuses without the file. Never create the file yourself.
- **Reruns of lost runs:** the analyst gives you an exact command line in a message. You run that command and nothing else. You never choose to rerun.

## 10. Escalation packet (what to write when anything is a STOP)

Create the file `$W/escalations/<UTC time>-<short name>.md` containing exactly:

1. The command you ran, copied exactly.
2. Its full output (last 60 lines if longer) and its exit code (`echo $?` right after).
3. The output of `python3 $Q/campaign_run.py $W status`.
4. If a runner command failed: `tail -n 60 $W/launch/<key>.log` and the names of any files matching `$W/runs/<key>/*.error.txt`.
5. The time, the machine name, and whether your terminal or session was interrupted.
6. One sentence: what you expected and what you saw. **No guesses about causes. No suggested fixes.**

Tell the stakeholder the packet path. Stop. Wait.

Good packet sentence: "I expected `RESULT: ALL OK`; the line `STOP evaluator profile is frozen and matches` appeared." Bad one: "It probably needs the profile re-created."

## 11. Quick answers (the only decisions you may make)

| You see | You do |
|---|---|
| `STOP` in preflight | Packet, wait |
| A command prints something different from "Expected" | Packet, wait |
| `EXIT 2` on one command in `status` | Note it, keep watching |
| `CRASHED` or `HALT` | Packet, wait |
| Provider error text in a log (for example 502) | Note the key in your notes; do not touch it; mention it in the final report |
| Your terminal closed | Do not relaunch; open a new one; run `status`; packet describing it |
| Disk free below 60 GB | Packet (the preflight checks this) |
| You are unsure | Packet, wait |

## 12. What to send back at the end of each phase

- Your notes: the preflight output, the first and last `status` outputs, the `verify` output, the `cost` outputs.
- `$W/OPERATOR-REPORT.md` (made by `prepare_campaign.py report`).
- Every packet in `$W/escalations/`.
- The calibration and pilot outputs (sections 5 and 7).

Never include the credential, any file from `$S/keys`, or any fixture or oracle text.

## 13. Glossary

- **Run**: one model session on one task. **Arm**: which protocol version it ran under (p72 candidate, p66 and p66b baseline, p65 old). **Stage 1 / stage 2**: the main panel first, then the preservation panels. **Admissible**: the run finished in a way that can be scored; a provider error makes it inadmissible, and only the analyst may rerun it. **Evaluator**: the second model that judges finished runs. **Calibration (C(b))**: the test that the evaluator is a fair judge. **Packet**: your written STOP report. **READY**: the analyst's go-ahead file.
