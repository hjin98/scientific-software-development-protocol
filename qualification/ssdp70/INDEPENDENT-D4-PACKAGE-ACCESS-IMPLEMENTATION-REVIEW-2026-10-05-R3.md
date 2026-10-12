# Independent D4 package-access implementation Review R3

Governing SSDP **6.6.0**; Protocol 7.0 remains **NON-QUALIFIED**. Independent `code_review` context; author of neither candidate nor D3 texts. Review is data, not runner/profile admission or qualification acceptance.

## Verdict and first demonstrated blocker

**NO-PASS.** No Serious Challenge demonstrated. One owner-local D4 blocker: **R3-B1, a standing non-T7 replacement drops retained critical-failure dispositions from scoring tallies when its evidence is inadmissible.** Stopped at this first demonstrated blocker; full regression and further falsification are incomplete. No overall qualification false PASS was demonstrated. The concrete defect is the false zero-critical-failure tally and omitted fail disposition, despite selecting that failure as the slot's standing run.

Canonical reconstruction preceded reading the previous R2 report. Global invariants reconstructed outside the author's test matrix: every open must be explained before exact bytes; native/owner-class positive evidence survives observation loss; negative owner conclusions require intact conservative observation; failed pairing cannot authorize route (iii); one scored run per slot, all available questions resolved, every declared failure retained and standing, no reserve overrides a clean original, and two attempts per affected case. The stakeholder-retained R4-1 observation-bound disposition limitation is an availability cost, not a new blocker or a PASS waiver.

### R3-B1: discarded critical fail in a selected non-T7 standing replacement

Owner: `qualification/ssdp70/eval/batch_assess70.py`, `score_slots`, scored-run disposition loop (approximately lines 365–368 in the reviewed candidate). `replacement_slots` correctly selects the failing replacement and marks `standing_failure: true`; the next owner reads only `actual.get("dispositions", [])`. A production inadmissible assessment retains independent fail judgments in `original_dispositions`, not `dispositions`: `core70.production_assessment` retains the former whenever dispositions are supplied and publishes the latter only for `COMPLETE_ADMISSIBLE` evidence. `hard_failure`/`blocks_rerun` explicitly recognize this retained form. The T7 owner-only standing-failure loop already falls back to `original_dispositions`, so the defect is confined to the normal scored-run loop.

Authority: clarification B.2 defines `fail` disposition as a hard failure, says a replacement block stands for the slot whatever its evidence state and that no definite failure is discarded. Contract item 13 / section 5 preserve declared failure and prohibit favorable-run selection; clarification B.5 explicitly illustrates retained critical/disposition tallies for the T7 exception. Ordinary non-T7 selection must preserve that same failure, not report it as absent.

Executable probe (production scorer; synthetic controlled input, not a provider observation):

```python
from test_batch_cli import SlotScoringComposition
p = SlotScoringComposition(); p.setUp()
try:
    r = p.build(replaced="T1-p70-r0", question="bytes", owner_replacement={
        "evidence_state": "INADMISSIBLE", "qualification_outcome": "NOT_EVALUATED",
        "dispositions": [],
        "original_dispositions": [{"item": "i1", "measure": "critical", "critical": True, "result": "fail"}]})
    assert r["scored_slots"]["T1-p70-r0"] == "T1-p70-r0-repl"
    assert r["package_access_replacements"]["records"][0]["standing_failure"] is True
    assert r["critical_failures"] == {}                         # defect: expected p70:1
    assert r["arms"]["p70"]["dispositions"]["fail"] == 0        # defect: expected 1
finally:
    p.tearDown()
```

An empty `dispositions` list here represents the absent production field; the offending `.get(..., [])` and hard-failure fallback behave identically for absence. The input judgment is retained and the production `score_slots` executes; no substitute scorer is used. Raw reproducible script `/tmp/cr5logs/probe.py`, output `/tmp/cr5logs/probe.json`; command from `/tmp/cr5/qualification/ssdp70/eval`: `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 /tmp/cr5logs/probe.py`. Probe SHA-256: b9ec491bafe2c4d7554b45bdc375a393f1c050ff655430db65bc10c69581137e. Minimal repair route: have the ordinary selected-run tally consume the same retained failure form as the standing-failure predicate/T7 loop; pin it through the real slot scorer. No D3 semantics change is required.

## Exact reviewed assembly

Baseline commit `3ca1891a0415ace6026bfb452377a557bc6947d6` **plus uncommitted bound four-file delta**, copied into an isolated clone with Git history (`/tmp/cr5`). This report does not claim the baseline commit contains the new bytes.

| Changed candidate file under `qualification/ssdp70/eval/` | SHA-256 |
|---|---|
| `package_ledger.py` | `d8c408eda659cd4a8515a3f5db882077d3e089ee3d556caef0c32102c61eac39` |
| `core70.py` | `6d40340ee7bbdbb130f22ea6e1c0067294353ad3bc7c88efceacc32f3fdb84bd` |
| `test_package_ledger.py` | `906751dcc856e63631ea875e95a7ba8b6def672ec08549f8fdc6f65a91298755` |
| `test_activation_accounting.py` | `b59e97feda838e34c2b65923b25f0de534cea90534060e11a821f99b94692553` |

D3 decision `fccb9a3a44afd89338eb19c8b3238a9943fab7c88ee694428dc7d6ce124fd783`; premise closure `5f713e2bd816950a2fd0962c6732242631295b3416387beb761c8b40906a3316`; contract `c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920`; window/replacement clarification `b7bead4ecb139732683d1919740a19ce3342740f2e8dace00781d4159c99e87f`; pairing delta `c2f7a3a348a9e9e1ef448b81e0db456e4e6720afdd5994f14b22068035edee9c`; independent text R2 `670e03fd8fbb80c194e21a72e50fc22b1214fdf077744031bb74f34488e7f6f6`. Identities and final diff independently read/checked. New gate only enables route (iii) for literal true complete adapter pairing metadata, with valid null/integer positions; routes (i)/(ii), delivered/native explanations and positives remain separate. No new gate defect demonstrated before stop; that is not a complete gate acceptance.

## Executed and incomplete evidence

All runtime testing used real OMP/observer/adapter/harness/core with the local stand-in provider only. No production provider credential read/execution. Initial default-sandbox attempts hit socket `PermissionError` before runtime: activation 3 pure tests passed and 21 runtime tests errored in each run; integration 54 runtime tests errored in each run. Retained `/tmp/cr5logs/a1`, `a2`, `i1`, `i2`; these are environment-denied attempts, not semantic code failures.

Authorized escalated launches ran two activation and two integration suites concurrently, 2 workers each (8 runtime test processes, unique short `/tmp/crh.*` HOME and runtime-closures symlink). At first blocker stop: activation **9 of 24 completed, all 9 passed**, in each of `a1e` and `a2e`; integration **10 of 54 completed, all 10 passed**, in each of `i1e` and `i2e`. These are partial counts, never suite PASS. Logs/results and adapted runner retained under `/tmp/cr5logs`; no remaining suite completion is claimed. Reviewer-owned process group `699371` received TERM; own scratch homes removed; escalated process inspection found no surviving process with review clone/home/log paths. No repository code/authority mutation, commits, push or modification of historical failed evidence occurred.

Required complete runtime repetitions, fast affected regressions, broad final regressions and remaining prior-R2 nonblocking case probes were not completed because of first-blocker stop. Prior-R2 report findings were used only as targets after own reconstruction, not as present candidate proof. Production premise witness/independent exclusion warrants, executor rehearsal on all arm shapes, frozen N/0.8 gate instantiation, byte disparity bound and qualification/admission remain outside this functional Review and open at their own gates. Source/dist unchanged; no protocol-source package release acceptance is claimed.

## Independence, history and scope

Shared model family, repository corpus and author test rig are common-mode limits. Probe derives its expected tally from canonical failure-preservation rules and exercises the actual slot scorer; its fixture construction is reused from a test utility, not independent end-to-end evidence. Prior memory registry entries at `MEMORY.md:26-59` were a search aid only; present authority and code were re-read, no memory-derived state accepted as current. Project PEM stayed cold: narrow local consumer defect, no mature subsystem replacement or history-dependent decision. This is tooling/evidence review, with no scientific simulation/model results produced or interpreted; the local scripted/synthetic results cannot establish provider behavior or qualification rates.
