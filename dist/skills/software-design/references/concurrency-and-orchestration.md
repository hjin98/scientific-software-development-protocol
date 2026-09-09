# Concurrency and Orchestration Correctness

Concurrency is an execution-model choice before it is a language/runtime choice. Synchronous code, event loops, shared-memory workers, isolated processes, distributed ranks, and accelerator pipelines all create correctness obligations around ownership, failure propagation, cancellation, publication, resource budgets, and deterministic aggregation.

Read `performance-and-parallelism.md` for throughput/resource sizing. Language-specific runtime selection belongs in the active language profile.

## Choose the execution class deliberately

Use the simplest class that satisfies the applicable governed workload/resource constraints and accepted D3 architecture:

- **synchronous serial** when concurrency adds no material value;
- **asynchronous/event-driven** for high-concurrency input/output (I/O), events, network/service orchestration, or useful pipeline overlap;
- **shared-memory concurrency** when low-cost shared address-space access and clear synchronization/ownership fit the workload;
- **process isolation** for independent address spaces, failure/security/runtime isolation, external executables, or a deliberately process-oriented architecture;
- **distributed-memory execution** for multi-process/multi-node scaling when required by accepted D3 architecture or another governed constraint;
- **accelerator execution** only when architecture-authorized.

Do not equate a particular language with one class. Python may use threads, async, processes, Message Passing Interface (MPI), or native kernels depending on interpreter/runtime semantics; C++ may use native threads/task runtimes, OpenMP-like execution, processes, MPI, or async/event runtimes. The profiles own those mappings.

## Define the execution state machine

For a nontrivial orchestrated workflow, make stage/task states explicit enough to reason about transitions. Typical states may include:

```text
QUEUED -> RUNNING -> COMPLETE
                 -> FAILED
                 -> CANCELLED
                 -> BLOCKED
```

Resumable systems may need durable distinctions such as `PARTIAL`, `RECOVERABLE`, or `INVALID`, but do not proliferate states without a real semantic difference.

Define:

- who owns each task/resource;
- which transitions are durable;
- what constitutes completion;
- how parent/child failure propagates;
- what state is safe to resume;
- what cleanup is required on every terminal path.

Do not infer completion from worker disappearance, file existence, or a progress counter alone.

## Failure classification and retry policy

Classify failures before retrying. Useful classes include:

- transient infrastructure/resource failures where retry can preserve semantics;
- adaptive resource failures with a bounded corrective action, such as an out-of-memory (OOM)-safe smaller batch;
- external-service/transient I/O failures with bounded backoff where idempotency is established;
- deterministic input/configuration/scientific-invariant failures;
- programmer defects/assertion failures;
- corruption/schema/lineage mismatch;
- user cancellation/preemption.

Only retry classes whose semantics are understood. A safe retry policy defines maximum attempts, backoff/jitter where appropriate, attempt-local versus reusable state, idempotency/publication behavior, retained evidence, and terminal failure. `retryable failure != arbitrary failure`.

## Idempotency and publication

Operations that may be retried or resumed should be idempotent or use unique attempt identities plus transactional publication.

- Separate attempt-local temporary state from accepted durable state.
- Publish final artifacts only after validation.
- Prevent duplicate logical outputs from concurrent/retried attempts unless duplicates are intentional.
- Ensure a resumed stage can distinguish accepted work from partial/stale work.

For file-backed publication, coordinate with `storage-and-io.md`.

## Cancellation, signals, and preemption

Long-running user/high-performance-computing (HPC) workflows should define behavior for cancellation and common termination signals where the platform permits it.

- Stop admitting/scheduling new work once cancellation begins.
- Propagate cancellation to owned tasks/processes/ranks/coroutines/workers as the runtime supports.
- Allow bounded graceful cleanup/checkpointing only when safe and useful.
- Do not claim a checkpoint was committed unless publication completed.
- Release owned devices, file handles, temporary directories, locks, shared-memory objects, child processes, and other runtime resources.
- Preserve externally owned/user input state.

A forced kill can always occur; durable state must not make partial output appear valid.

## Backpressure and bounded in-flight work

Producer/consumer and async pipelines need bounded in-flight work.

- Bound queues/futures/tasks by count and/or resource footprint.
- Avoid reading/materializing an entire dataset merely because downstream work is slower.
- Couple admission to random-access memory (RAM), video random-access memory (VRAM), I/O, and storage budgets for heterogeneous tasks.
- Avoid unbounded result buffers, logs, pending serialization, requests, and callbacks.

When throughput stalls, distinguish compute saturation from queueing, lock contention, event-loop blocking, I/O saturation, communication, or downstream backpressure.

## Resource ownership and nested runtimes

Make ownership of scarce resources explicit:

- central-processing-unit (CPU) worker/thread/rank leases;
- accelerator/device assignment and concurrent-job limits;
- RAM/VRAM reservations or admission estimates;
- I/O concurrency budgets;
- scratch directories/cache writers;
- ports/files/locks/shared-memory objects;
- event-loop/thread affinity where the runtime requires it.

Do not allow nested runtimes to independently assume they own the entire machine. An inner numerical or framework library called from an already-parallel region should use bounded/serial inner concurrency when that is the correct resource plan.

## Determinism and aggregation

Concurrency may change completion/arrival order without permission to change externally visible semantics.

- Define whether result ordering is input order, key-sorted order, stable task order, or intentionally unordered.
- Use deterministic reductions where reproducibility requires them; document accepted floating-point nondeterminism when strict reproducibility is impractical.
- Make random seeds/task seeds independent of scheduler/rank timing when reproducibility is required.
- Avoid unordered mutation of process-global/runtime-global state unless explicitly coordinated.

## Locks and shared state

Prefer ownership/partitioning or immutable shared data over broad locking.

When locks/synchronization are unavoidable:

- define scope/order;
- keep critical sections small;
- avoid holding locks across slow I/O or blocking callbacks when possible;
- ensure exceptions/cancellation release synchronization resources;
- test concurrent creation/publication paths;
- avoid stale lock files without ownership/lease semantics.

Language/runtime-specific memory-model and race hazards belong in the active profile.

## Distributed-memory execution

When distributed execution is part of the accepted D3 architecture or directly required by another governed constraint, reason explicitly about:

- decomposition and rank ownership;
- communication volume and message size;
- collectives and synchronization points;
- failure model and cancellation semantics;
- rank-local shared-memory/threaded libraries;
- I/O topology and publication;
- deterministic/global aggregation where required.

MPI is a common concretization from both Python and C++, not a C++-only doctrine. Do not introduce distributed execution merely because an MPI runtime is installed.

## Progress and estimated time of arrival

Progress describes accepted logical work, not merely submitted tasks. Keep output convention stable within a project. Restored completed work should not be double-counted.

Estimated time of arrival (ETA) is observational: base it on representative completed work, use a consistent project-defined format, and do not let progress reporting materially perturb hot loops, event loops, communication, or disk I/O.

## Verification

Test concurrency at the state-transition/resource boundary, not only by comparing final happy-path output:

- serial/reference versus concurrent equivalence;
- deterministic ordering/seed/reduction behavior where required;
- task/worker/rank failure propagation;
- cancellation during compute, waits, communication, and publication as applicable;
- bounded retry/backoff and terminal failure;
- OOM/resource backoff only where semantically safe;
- bounded queue/backpressure behavior;
- concurrent cache/output creation;
- restart after partial completion;
- cleanup of children/tasks/temp state/locks after failure;
- nested runtime budget behavior;
- repeated stress/race checks where deterministic tests cannot expose the risk.

Each execution is an evidence realization. After material changes to orchestration ownership, retry semantics, publication, runtime/backend, or state transitions, review prior evidence applicability and rerun the relevant evidence specifications rather than assuming historical green results remain current.

## Bounded failure injection

For material orchestration/recovery claims, use controlled worker/task death, cancellation, duplicate delivery, publication interruption, or equivalent bounded failpoints when happy-path testing cannot establish the state-transition contract. Keep the real orchestration owner executing, prove trigger liveness when practical, and avoid indiscriminate chaos/resource exhaustion when a deterministic simulation provides the same evidence.

## Hard rules

- Do not equate more concurrency with correctness or performance.
- Do not retry unknown failures indefinitely.
- Do not leave orphan owned tasks/processes/ranks/resources after normal failure/cancellation paths.
- Do not let task completion race with artifact publication or manifest/state transition.
- Do not make externally visible ordering accidentally depend on scheduler timing.
- Do not allow unbounded queues/futures/tasks to become hidden memory/storage buffers.
