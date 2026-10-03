# STAGE 7 OMP SEMANTIC-ADMISSION EXECUTOR REALIZATION & SERIOUS CHALLENGE REPORT

**Role:** STAGE 7 OMP EXECUTOR / OPERATOR  
**Governing SSDP Version:** 6.6.0  
**Date:** 2026-10-03  
**Status:** EXECUTED — ALL 244 RUNS PRE-LAUNCH TERMINATION (`EXECUTION_ERROR`) — FORMAL SERIOUS CHALLENGE RAISED  

---

## 1. Executive Summary & Identity Baseline

This report documents the launch, execution, append-only retention, cryptographic freeze, and root-cause failure analysis of the **Stage 7 OMP Semantic-Admission Matrix Realization**.

The matrix execution was launched using the real qualification harness ([`qualification/ssdp70/eval/harness70.py`](file:///home/samjin/agent-skills/scientific-software-development-protocol/qualification/ssdp70/eval/harness70.py)) on 2026-10-03 across all 122 episodes in the frozen semantic custody package under arms `p66` and `p70`.

### Exact Bound Identities
- **Local Repository:** `/home/samjin/agent-skills/scientific-software-development-protocol`
- **Live Branch:** `ssdp-7.0-scientific-epistemic-closure`
- **Live HEAD:** `c9e79dba0227739638c3a452f8edd213074ede98` (clean working tree)
- **Executor Candidate Commit:** `d50dcb539334582cd8a848dcc0d72ed5c7f4f897`
- **Immutable Protocol 7 Semantic Subject:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **OMP Profile Key:** `3ce07101a33bb427453dcfa862f811bfdf276a073d4e2662e3624b924a0be8b6`
- **Campaign Root:** `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/`
- **PEM Base Commit:** `2585b73f00420daca185a4fbb9ac42a79473eda1` (0 diff against `main`)
- **Gate 1 Pre-Run Directory:** `/home/samjin/ssdp70-omp-stagef/pre-run-checks/independent-20261003T162341.174577Z/` (Verdict: `PRE-RUN PASS`)
- **Sealed Public First-Look SHA256:** `dd7869f00bafad5392e3f3ff81661856c87dc22fcaaa77da81911224f760a3b9`
- **Frozen Custody Subject:** `/home/samjin/ssdp70-omp-stagef/semantic-custody-20261003T161129.024432Z`
  - Manifest SHA256: `be7d76d7d2d9d6a79447462ae1679f303cb3ae8f009d5077bcfc8e7cad62ad7d`
  - Recorded `FREEZE.utc`: `2026-10-03T16:14:47.260081114Z`
  - Payload Files: 423 files, mode 0500/0400, 0 writable bits, 0 symlinks
- **Retained Realization Directory:**  
  `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/semantic-runs/20261003T165129Z-e67dbf6109/`
  - `FREEZE.utc`: `2026-10-03T16:53:51.899564Z`
  - `FREEZE.sha256.digest`: `1c6af7aa8a1f03eb5aa43ae22351e6dee1295598f220d9ba898c2d9f747ff80c`
  - Total Sealed Payload Files: 1,222

---

## 2. Execution Boundary & Contract Conformance

The matrix realization was launched via the approved campaign contract without altering candidate source, harness, adapter, or frozen custody:

```bash
export SSDP70_OMP_PROVIDER_CREDENTIAL="$SSDP70_DEEPINFRA_API"
export DEEPINFRA_API_KEY="$SSDP70_DEEPINFRA_API"
export PYTHONUNBUFFERED=1
python3 qualification/ssdp70/eval/harness70.py matrix \
  --corpus /home/samjin/ssdp70-omp-stagef/semantic-custody-20261003T161129.024432Z/public/corpus \
  --arms-manifest /home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/arms.json \
  --out /home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/semantic-runs/20261003T165129Z-e67dbf6109 \
  --profile /home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/profile.json \
  --capabilities /home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/capabilities.json \
  --requirements /home/samjin/ssdp70-omp-stagef/semantic-custody-20261003T161129.024432Z/public/requirements \
  --oracles /home/samjin/ssdp70-omp-stagef/semantic-custody-20261003T161129.024432Z/public/oracles \
  --adapter omp --mode probe --parallel 2 --arm p66 --arm p70
```

### Protocol Invariant Compliance
1. **Output Confinement:** Output directory was placed strictly beneath `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/` in compliance with `record_proof` roots.
2. **Append-Only Retention:** No prior realizations were overwritten; every run attempt was captured with run-identity snapshots and `.error.txt` diagnostic logs.
3. **Strict Separation:** The executor never mounted or accessed `/home/samjin/ssdp70-omp-stagef/semantic-custody-20261003T161129.024432Z/withheld/`.
4. **Machine Isolation:** Bubblewrap sandbox substrate (`/usr/bin/bwrap`) executed with loopback network namespace, stripped ambient credentials, and clean environment.

---

## 3. Realization Results

- **Matrix Pairs:** 122 pairs planned across episodes C001–C122.
- **Arm Runs:** 244 total runs (122 for `p66`, 122 for `p70`).
- **Scheduler Events:** [`matrix-scheduler.jsonl`](file:///home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/semantic-runs/20261003T165129Z-e67dbf6109/matrix-scheduler.jsonl) logged all 122 `pair_start`, `arm_start`, `arm_end`, and `pair_end` events without scheduler trace error (`scheduler_trace_errors()` returned `[]`).
- **Realization State:** All 244 runs terminated with `evidence_state: "EXECUTION_ERROR"`.

Every run produced a diagnostic record containing:
```text
CalledProcessError(1, ['git', 'init', '-q'])
```
and standard error:
```text
/home/samjin/ssdp70-omp-stagef/logs/runtime-state/<run-id>/project/.git: Permission denied
```

---

## 4. Root Cause Analysis

The failure across all 244 episodes is 100% deterministic and stems from a direct structural contradiction between the **custody freeze invariant** and the **harness project-staging implementation**:

1. **Custody Freeze Mode:**  
   The frozen custody package enforces strict mode `0500` (read and execute only, 0 writable bits) on all directories in `semantic-custody-20261003T161129.024432Z/public/corpus/fixtures/*/project`. This satisfies Gate 1's temporal and immutable custody check.

2. **Harness `build_project` Staging:**  
   In [`qualification/ssdp70/eval/harness70.py:168`](file:///home/samjin/agent-skills/scientific-software-development-protocol/qualification/ssdp70/eval/harness70.py#L168-L179):
   ```python
   def build_project(corpus: Path, episode: dict[str, Any], project: Path, control_names: list[str]) -> None:
       fixture = corpus / "fixtures" / episode["fixture"]
       if not fixture.is_dir():
           raise core70.ContractError(f"fixture directory is missing for {episode['id']}")
       project.mkdir(parents=True)
       script = fixture / "build_history.sh"
       if script.is_file():
           subprocess.run(["bash", str(script)], cwd=project, check=True, capture_output=True)
       if (fixture / "project").is_dir():
           shutil.copytree(
               fixture / "project",
               project,
               dirs_exist_ok=True,
               ignore=shutil.ignore_patterns("__pycache__"),
           )
       if not (project / ".git").is_dir():
           subprocess.run(["git", "init", "-q"], cwd=project, check=True)
   ```
3. **Stat Copy & Permission Denial:**  
   Python's `shutil.copytree(..., dirs_exist_ok=True)` unconditionally calls `copystat(src, dst)` on directory entries. As a consequence, the working directory `project` inside `logs/runtime-state/<run-id>/` has its permission mode mutated to `0500` (read-only).  
   When line 179 subsequently calls `subprocess.run(["git", "init", "-q"], cwd=project, check=True)`, git attempts to create the directory `.git` inside `project`. Because `project` has been rendered mode `0500`, the Linux kernel rejects the `mkdir` syscall with `EACCES` (`Permission denied`).
4. **Subsequent Agent Inoperability:**  
   Even if `.git` were initialized, the files copied by `copytree` retain mode `0400`, preventing the subject agent from performing legitimate file edits during qualification episodes.

---

## 5. Formal SERIOUS CHALLENGE

> [!CAUTION]
> ### SERIOUS CHALLENGE: Structural Contradiction Between Frozen Custody Mode and Harness Execution Contract
> **Affected Domains:** D3 Software Architecture / D4 Harness Implementation & Fixture Custody  
> **Contradiction:**  
> The accepted custody authority mandates mode `0500`/`0400` with zero writable bits across all frozen files and directories in `semantic-custody-*`. Conversely, the frozen harness implementation [`qualification/ssdp70/eval/harness70.py`](file:///home/samjin/agent-skills/scientific-software-development-protocol/qualification/ssdp70/eval/harness70.py) relies on standard `shutil.copytree()`, which transfers `st_mode` (`0500`) directly onto the mutable working project directory before attempting `git init -q` and file mutations.  
>
> **Authority Constraint:**  
> Under SSDP 6.6.0 (`AGENTS.md`), the Executor role is explicitly prohibited from repairing candidate source, harness, adapter, or frozen custody files ("Do not repair candidate source, harness, adapter, or frozen custody files"). Furthermore, [`qualification/ssdp70/eval/harness70.py`](file:///home/samjin/agent-skills/scientific-software-development-protocol/qualification/ssdp70/eval/harness70.py) is cryptographically frozen into `profile.json` (SHA256: `b01485bcc1513aed71afe62d9502b2de08e60993fc926737485df564f5689821`) and `campaign.json`. Modifying `harness70.py` without an upstream architecture/campaign repair invalidates the profile key and campaign invariants. Modifying custody files invalidates `FREEZE.sha256` and Gate 1.
>
> Therefore, this contradiction cannot be resolved by the executor and is formally routed upstream.

---

## 6. Actionable Resolution Paths for Upstream Owners

1. **Path A — D4 Harness Repair (Recommended):**  
   Update `build_project()` in [`qualification/ssdp70/eval/harness70.py`](file:///home/samjin/agent-skills/scientific-software-development-protocol/qualification/ssdp70/eval/harness70.py) to explicitly ensure write permissions on mutable working copies:
   ```python
   # After copytree or using a custom copy_function:
   for root, dirs, files in os.walk(project):
       for d in dirs:
           os.chmod(os.path.join(root, d), 0o755)
       for f in files:
           os.chmod(os.path.join(root, f), 0o644)
   os.chmod(project, 0o755)
   ```
   *Implication:* This changes `harness70.py` SHA256, requiring re-freezing the profile template, minting a new profile key, updating `profile.json`/`capabilities.json`, and re-initializing the campaign.

2. **Path B — Fixture Custodian Packaging Repair:**  
   The custodian repackages fixtures such that mutable project directories are generated dynamically by `build_history.sh` rather than copied from a static `project/` directory frozen at mode `0500`, or adjusts how the fixture project template is isolated.  
   *Implication:* Requires minting a new semantic custody freeze and re-running Gate 1 (Independent Pre-Run Check).

3. **Path C — Evaluator Downstream Completion on Retained Realization:**  
   If desired by the stakeholder, Gate 3 (Evaluator Admission) and Gate 4 (Evaluator / `assess70.py`) can be executed over copies of the current retained realization (`20261003T165129Z-e67dbf6109`) to formally produce the negative qualification record and complete the blinded evaluation trail prior to authorizing candidate repair.
