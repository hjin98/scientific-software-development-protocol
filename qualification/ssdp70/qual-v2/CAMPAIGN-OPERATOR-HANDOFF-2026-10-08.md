# SSDP 7.2 qualification campaign: operator hand-off

Governing SSDP version: 6.6.0. This file is data. It tells a careful operator model what to run and when to stop. It gives you no authority to choose, edit, retry or skip anything.

**STATUS: NOT READY.** Do nothing in sections 3 to 8 until the file `READY` exists in the campaign directory (section 1) and its text says `OPERATOR MAY LAUNCH`. The analyst writes it after the corpus exists, the pre-run checker has passed and the stakeholder has authorized the launch. If the file is missing or says anything else, stop and report that.

## 0. Rules (read twice)

1. You run the printed commands, in order, and save their output. You do not change a value, an input, a tool, a profile, a corpus, an oracle or a command.
2. **Any result that is not exactly the expected one is a stop.** Write an escalation packet (section 7) and wait for the analyst. Do not retry. Do not relaunch. Do not "fix" anything.
3. Never delete, move, rename or edit anything in a run directory. They are evidence.
4. Never open `keys/`, `authoring/`, `human-trial/`, any custodian store (`~/ssdp72b-fixture-custody`, `~/ssdp72-fixture-custody`, `~/ssdp71-fixture-custody`, `~/ssdp70-fixture-custody`) or any oracle source. The tools read what they need; you pass them paths and nothing else.
5. You launch from your own terminal session, not from an agent-runner session that can be torn down (an agent teardown killed the first S4 rerun attempt). The credential lives only in your shell environment. Never print it, write it to a file or paste it anywhere.
6. Reruns of lost runs are the analyst's decision (contract section 3). You never rerun.
7. At most 8 runs are in flight. The plan already enforces it; do not start a second copy of anything.

## 1. Paths and values

```bash
export REPO=$HOME/agent-skills/scientific-software-development-protocol
export W=$HOME/ssdp70-omp-stagef/qualification/campaign-72-20261008
export Q=$REPO/qualification/ssdp70/qual-v2
```

The campaign directory `$W` holds: `arms/` (the packages), `keys/` (the executor profile; the evaluator profile appears here only when the stakeholder has named the evaluator model), `campaign-identity.json`, `static-premeasurement.json`, `commands.json` and `declaration.json` (written by the analyst at plan time), `launch/`, `runs/`, `escalations/`, `authorizations/`.

Expected identities (the analyst printed these on 2026-10-08; they must match exactly):

| Item | Value |
|---|---|
| Candidate arm p72 | commit `2dedcfa3408f62bc11a696ac3776183a87b40438`, version 7.2.0, dist tree `69a310a26eb22be395b0a9b98603d8b58dd53171657bfb068ce5821518c5f622` |
| Baseline arms p66 and p66b | commit `22f4bdba53795da3a6f13f162529f3a843fc37ae`, version 6.6.0, dist tree `e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083` |
| Old arm p65 | commit `7f7b5e24858e813e45ace867a7f8ea5180f43bf0`, version 6.5.0, dist tree `7d61d8b7b19dfe40714e71daa2c46d0e4cdd62efebd96b8e96dfe3f33550429b` |
| Executor profile file sha256 | `b96dcb43155f452eec121307b83df56ff3f79ca308f6c4555206a5871088b107` |
| Executor | `deepinfra/zai-org/GLM-5.3-Flash`, 60 turns, 2400 s |

## 2. Pre-flight (no provider, no credential; read-only)

Run each command and compare. A mismatch is a stop.

```bash
cat $W/READY                                            # must say: OPERATOR MAY LAUNCH
sha256sum $W/keys/omp-primary-flash-executor-main.json  # must equal the profile sha256 above
python3 -c "import json;d=json.load(open('$W/campaign-identity.json'));print(json.dumps(d['arms'],indent=1));print(d['candidate_source_dist_diff_from_ref'])"
                                                        # arms must match the table; the last line must be: empty
python3 $Q/prepare_campaign.py check-plan --work $W     # must print "verdict": "PASS"
cat $W/static-premeasurement.json | python3 -c "import json,sys;print(json.load(sys.stdin)['verdict'])"   # must print: PASS
cat $W/expected-runs.json                               # note unconditional_runs; you will compare it later
cd $REPO && git status --short && git rev-parse HEAD    # write both outputs into your notes
```

## 3. Launch (the stakeholder is present or has said GO; the credential is in your shell)

The campaign runs in two stages, in gate order. **Stage 1** is the main panel (366 runs). **Stage 2** is the preservation panels (274 runs) and starts only after the analyst has scored stage 1 and written `$W/authorizations/stage2.ok`. If stage 1 shows the candidate has failed an earlier gate, the analyst will not authorize stage 2, and you stop there.

```bash
export SSDP70_OMP_PROVIDER_CREDENTIAL=...     # the stakeholder gives you the key; never print it
python3 $Q/campaign_run.py $W start 1         # prints: started the sequential runner for stage 1 (pid N)
```

If it prints anything else, stop. Do not run `start 1` twice. Stage 2 (only when told, with the `.ok` file present): `python3 $Q/campaign_run.py $W start 2`; it refuses otherwise.

## 4. Watch

```bash
python3 $Q/campaign_run.py $W status
```

Run it every 10 to 15 minutes and keep the output. Each command line shows RUNNING, EXIT 0, EXIT 2 or CRASHED. Meaning:

- **EXIT 0**: the command finished and every run is admissible. The runner goes on to the next command.
- **EXIT 2**: the command finished and at least one run is not admissible (for example a provider failure). The runner still goes on. Note the command key in your packet for the analyst; do not touch the runs.
- **HALT** line at the bottom, or **CRASHED**: the sequence stopped. Stop and write an escalation packet. Do not restart.
- `DONE-stage1` (or `DONE-stage2`) at the bottom: every unconditional command of that stage finished.

You may leave the terminal alone between checks. If your own session or machine goes down, do not relaunch: write what you saw into a packet and ask the analyst.

## 5. After each stage: verify (no credential needed)

The analyst gives you the gate-map path in the READY file (a file under the custodian's `operator/` directory, meant for you).

```bash
python3 $Q/prepare_campaign.py verify --work $W --map "<gate-map path from READY>" --stage <1 after stage 1, 2 after stage 2>
echo "exit=$?"
```

Expected: `"findings": []` and `exit=0`. Findings of kind `RERUN_PENDING`, `INADMISSIBLE` or `UNRESOLVED` are not your decision: copy the whole output into the packet. `UNRESOLVED` is expected until the evaluator has run (section 6).

## 6. Evaluator pass (P9): only when `$W/keys/omp-evaluator-readonly.json` exists and READY says `EVALUATION MAY START`

The evaluator pass covers the main, versioning and sentinel panels only (the other panels are scored by binding oracles or recorded bytes). It has a **pilot first**, then the rest. The evaluator key variable may differ from the executor's: use the one READY names.

```bash
EV="--keys-root <keys root from READY> --evaluator-profile $W/keys/omp-evaluator-readonly.json \
    --evaluator-capabilities $W/keys/omp-evaluator-readonly.capabilities.json --shared-rubric <rubric path from READY>"
python3 $Q/campaign_assess.py run $W $EV --parallel 4 --limit 5           # the pilot: five runs
python3 $Q/campaign_assess.py cost $W --price-in <P> --price-cached <P> --price-out <P>   # prices come from READY
```

Copy the `cost` output into your notes and **stop**. The analyst compares the measured dollars per run and the projection with the budget and writes `$W/authorizations/evaluator-full.ok` if the full pass may go ahead. Only then:

```bash
python3 $Q/campaign_assess.py run $W $EV --parallel 4
python3 $Q/campaign_assess.py collect $W --out $W/dispositions.json
python3 $Q/campaign_assess.py cost $W --price-in <P> --price-cached <P> --price-out <P>
```

Expected: `collect` prints `"problems": []`. Any problem entry goes into the packet as it is. Do not rerun an assessment.

## 7. Escalation packet (write a file, then stop and wait)

Create `$W/escalations/<UTC time>-<short name>.md` with exactly:

1. The command you ran, verbatim.
2. Its full output, or the last 40 lines if it is longer, plus the exit code.
3. `python3 $Q/campaign_run.py $W status` output.
4. For a crashed or failed command: `tail -n 40 $W/launch/<key>.log` and the names of any `*.error.txt` files under `$W/runs/<key>/`.
5. The time, the machine, and whether your session was interrupted.
6. One sentence: what you expected and what you saw. No guesses about causes. No proposed fixes.

Then tell the stakeholder the packet path and stop.

## 8. Conditional commands (only on the analyst's instruction)

Some commands (extra T7 pairs, extra sentinel and unversioned runs) run only if the analyst says so. The analyst writes `$W/authorizations/<key>.ok`. Then, and only then:

```bash
python3 $Q/campaign_run.py $W run-conditional <key>
```

The tool refuses without that file. Do not create the file yourself.

## 9. What to send back when you finish

- Your notes from section 2 and the first and last `status` outputs.
- The `verify` output and, if section 6 ran, the `collect` output.
- Every escalation packet.
- `ls $W/runs` (names only) and `cat $W/launch/*.exit`.

You never score, interpret or summarize results. The analyst does that.
