# Performance, Memory, Data Movement, Parallelism, and Accelerators

Performance is an engineering-fitness concern, not a language-specific style rule. Optimize the materially owning/user-visible path with the minimum justified total product/system complexity, then map the shared strategy through the active language profile(s).

## Optimization order

Optimize in this order unless representative profiling provides a strong reason otherwise:

1. remove redundant work and repeated I/O/parsing/serialization;
2. improve asymptotic algorithm or search space;
3. improve data representation/layout and reuse/caching with explicit validity;
4. batch/stream work to reduce dispatch, synchronization, and allocation overhead;
5. use established optimized compiled/vectorized numerical or domain kernels;
6. reduce temporary allocations/copies and improve locality;
7. add shared-memory or asynchronous concurrency for genuinely independent work when it improves the owning path;
8. add process/distributed execution when isolation or architecture/scaling requires it;
9. add GPU/accelerator execution only when architecture-authorized and transfer/runtime overhead is amortized;
10. consider bespoke compiled kernels, explicit SIMD, architecture dispatch, or other low-level specialization only for a remaining dominant path whose benefit justifies the complexity.

Do not optimize from intuition alone when representative profiling is available. An obvious semantically equivalent efficiency improvement that adds no material complexity may be implemented without a pre-change benchmark, but a quantitative speedup/scaling/resource claim still requires comparable measurement.

Treat predicted wall time as an observability/planning estimate unless the user or project explicitly defines it as an SLA/admission contract. A benchmark-derived runtime estimate is not a physical safety limit like memory or disk capacity and should not by itself reject otherwise valid work.

## Efficiency by construction versus complexity escalation

Prefer, without benchmark ceremony when equivalence is clear and complexity does not materially grow:

- remove repeated work, conversions, allocation, serialization, parsing, and synchronization;
- choose an asymptotically better algorithm/data structure;
- avoid unnecessary materialization and preserve locality;
- reuse an already-compatible established optimized primitive;
- batch or stream work when it reduces overhead without creating extra state;
- prevent accidental nested oversubscription.

Still run ordinary correctness/regression checks. Do not report an unmeasured change as a measured speedup.

Require representative evidence before durable adoption of complexity such as:

- a new language/native boundary or bespoke kernel;
- explicit SIMD/intrinsics or CPU feature-dispatch machinery;
- an additional async/thread/process/MPI runtime or hybrid parallel layer;
- custom allocation/pooling solely for speed;
- LTO/PGO as a governed build/release dependency;
- backend/fallback proliferation;
- an accelerator implementation;
- approximation, precision, or other scientific-semantic changes.

The evidence must include the total-system tradeoff when material: source/build complexity, dependencies, compile/binary size, portability, deployment, resource use, failure behavior, and maintenance—not only isolated kernel throughput.

## Optimized kernels and vectorized/compiled execution

Prefer established validated optimized primitives when the computation maps cleanly and the dependency satisfies precision, scientific, licensing, portability, deployment, and ownership requirements.

The shared principle applies across languages. Python may reach a tuned BLAS/FFT/kernel through NumPy/SciPy or another framework; C++ may call BLAS/LAPACK/FFTW/domain libraries directly or through an abstraction. The language profile owns those mappings.

- Do not assume an API is fast merely because it looks vectorized; measure materialization, object conversion, dispatch, and backend behavior when relevant.
- Do not rewrite a well-mapped tuned operation as custom loops/SIMD merely to make low-level control visible.
- Do not convert irregular sparse/combinatorial algorithms into dense layouts solely to satisfy a generic "vectorize/no loops" heuristic.
- When replacing a hot path, protect a particular implementation form with a regression/static check only when that form is itself a real project/Frozen contract; normally protect behavior and performance instead.

## I/O and data movement

For disk-heavy persistence, caches/checkpoints, scratch sizing, or restart behavior, also read `storage-and-io.md`.

- Parse/read immutable inputs once per logical operation when possible.
- Reuse normalized/canonical intermediate forms rather than reopening files in inner loops.
- Stream/chunk when data exceeds comfortable memory, but ensure chunking does not change reduction semantics or ordering.
- Avoid serializing/copying large intermediates between workers or runtimes when a shared/read-only view, memory mapping, batching, or another ownership-preserving representation is materially better.
- Include host-device transfer and synchronization in accelerator timing.
- Include language-boundary conversion/marshaling, serialization, cold-load, write-back, cache construction, and recovery time when those costs are part of the user-visible stage.
- Treat I/O concurrency as a separate saturation domain; more CPU workers can make a storage-bound workload slower.

## Effective resource discovery

Use the effective allocation, not machine marketing specifications or a raw host-count API.

CPU evidence may include:

- process/thread affinity or cpuset restrictions;
- cgroup/container CPU quota;
- scheduler-provided allocation/environment;
- explicit user/project configuration;
- host hardware-count APIs such as Python `os.cpu_count()` or C++ `hardware_concurrency()` only as upper-bound hints.

Memory evidence may include:

- currently available host RAM;
- cgroup/container available memory;
- scheduler/job limits;
- explicit application limits;
- per-task measured peak or a conservative estimate.

Accelerator discovery, only when accelerator support is architecture-authorized, should record device availability, selected device, free/total memory, runtime/library capability, and reason for fallback.

## Default budgets

Use configurable defaults rather than hard-coding saturation:

- CPU target: at most about `0.90 * effective_cpu_threads`, rounded conservatively and never below one worker/thread when work exists;
- system RAM admission: keep estimated/measured peak at or below about `0.80 * currently_available_ram` unless the project/user defines another bound;
- accelerator memory: keep meaningful headroom; `<=0.90` of currently free/allocatable VRAM is a reasonable soft ceiling when no project-specific policy exists.

These are upper budgets, not targets. Use fewer resources when throughput saturates, memory estimates are weak, latency/responsiveness matters, CI is shared, or nested execution would oversubscribe.

## Execution classes

Choose the execution class from workload and architecture before choosing a language-specific runtime.

- **Synchronous serial:** default when parallelism would not materially improve the owning path or when reproducibility/debuggability dominates.
- **Asynchronous/event-driven:** appropriate for high-concurrency I/O, event processing, network/service orchestration, or pipeline overlap when it reduces thread/process complexity.
- **Shared-memory concurrency:** appropriate for work that benefits from low-cost shared address-space access and has clear ownership/synchronization.
- **Process isolation:** appropriate for independent address spaces, failure/security/runtime isolation, external executables, or runtime constraints; not automatically the best CPU-speed mechanism.
- **Distributed memory:** appropriate when product/Frozen architecture requires multi-process/multi-node scaling or a representative single-node limit drives Design to distributed execution.
- **Accelerator execution:** architecture-gated; hardware availability alone does not create a requirement.

The Python and C++ profiles specialize how these classes map to GIL/free-threaded interpreter modes, native threads/OpenMP/task runtimes, processes, MPI, and other runtimes.

## Nested parallelism and resource ownership

Model the whole stage, not each library independently.

Approximate CPU demand as the product/sum of simultaneously active outer and inner execution layers as appropriate. Explicitly account for application workers/tasks, language/runtime threads, BLAS/FFT/OpenMP/framework thread pools, MPI ranks, and concurrent accelerator jobs.

Do not let nested schedulers independently assume they own the entire machine. A library called inside an already-parallel region should be able to run with bounded/serial inner concurrency when that is the correct resource plan.

For long-running user-facing workflows, make resource ownership observable when it materially helps operation: effective allocation, outer concurrency, inner library threads, accelerator jobs, RAM/VRAM estimates, and I/O/scratch budget. Keep numerical kernels decoupled from ad-hoc stdout; use project-appropriate structured diagnostics/progress.

## GPU/accelerator policy

Accelerator implementation is **dormant unless accelerator support is a Tier-1 requirement or explicitly Frozen architecture decision**. Do not require GPU probing, dependencies, builds, tests, or profiler tooling for CPU-only architecture.

When enabled, require:

1. supported hardware/runtime detection consistent with the product portability contract;
2. a workload large/parallel enough to amortize transfer/launch/runtime overhead;
3. required operations without pathological host-device ping-pong;
4. bounded/adaptive VRAM use;
5. CPU/reference equivalence within accepted scientific semantics;
6. explicit and tested fallback only when the product supports fallback;
7. end-to-end representative evidence showing material benefit.

Prefer established optimized accelerator libraries before custom kernels when operations map cleanly. Include transfer/synchronization, initialization, conversion, and device-memory effects in performance evidence. Record backend/device/precision/batch configuration when material.

For OOM-sensitive pipelines, reduce batch/concurrency and retry only when the transformation is semantically safe; cap retries and surface terminal failure clearly.

## Benchmark acceptance

Before calling an optimization successful, provide enough evidence for the claim:

- baseline and candidate on comparable representative inputs/environment;
- correctness/scientific equivalence;
- repeated wall-time/throughput evidence when speed is claimed;
- peak/bounded memory evidence when relevant;
- I/O bytes/footprint and cold/warm/recovery evidence when storage behavior is relevant;
- scaling across enough sizes/workers/ranks/devices to expose the claimed trend;
- material build/backend/runtime/ISA differences needed to interpret the comparison;
- explanation of regressions/tradeoffs;
- conservative default/auto-selection rule when one is introduced.

Do not accept speedup obtained by lowering scientific resolution, changing estimator semantics, weakening validation, changing precision policy without approval, omitting required output, moving work outside the timed region, or comparing debug/instrumented and optimized builds as if they were equivalent candidates.

For compiled code, record materially relevant compiler/toolchain, optimization/build mode, target ISA, LTO/PGO state when used, sanitizer/coverage instrumentation, numerical backend, parallel runtime/thread settings, and hardware. Debug/sanitizer versus production comparisons may answer a build-overhead question but do not establish product speedup.

Existing expensive baseline evidence may be reused when source/input/benchmark-method/environment identity remains compatible with the comparison. A later date or new agent session alone does not invalidate it.

## Longitudinal performance regression tracking

For mature hot paths or workflows whose performance materially matters, keep stable benchmark scenarios in addition to one-change before/after measurements.

Record enough identity to compare fairly: source/package version, representative input distribution/size, hardware/runtime/backend/precision, CPU/thread/worker/rank/device configuration, warm-up/repeat method, wall time/throughput dispersion, peak RAM/VRAM, and I/O/recovery footprint where material.

Define an acceptable regression band appropriate to measurement noise and user impact. Do not silently replace the baseline after a regression; record why a new baseline is accepted. Track trends separately from gate-local claims so gradual performance loss across many individually small changes remains visible.
