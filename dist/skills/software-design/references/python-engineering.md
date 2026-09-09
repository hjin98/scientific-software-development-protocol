# Python Engineering Profile

Read [Language engineering profiles](language-profiles.md) first. This profile specializes shared Protocol 6 domain doctrine for Python execution and packaging. Shared architecture, testing, performance, concurrency, scientific, security, and release owners remain authoritative.

## Language-native design

Prefer Python mechanisms that keep product behavior explicit while avoiding machinery that exists only to compensate for lower-level languages.

- Prefer clear high-level functions/modules and the project's established abstractions before adding frameworks, registries, wrapper hierarchies, or dynamic metaprogramming.
- Use context managers and deterministic resource scopes when they simplify ownership of files, locks, temporary state, transactions, devices, or external resources.
- Use iterators, generators, streaming, and lazy traversal when they reduce unnecessary materialization without obscuring failure or ordering semantics.
- Use dataclasses, protocols, typed records, enums, and type annotations when they materially improve contracts and tooling; do not create a second schema/type system merely for symmetry.
- Prefer simple immutable/read-only data flow where practical. Avoid avoidable object churn, reflection, monkeypatch-oriented production architecture, and abstraction whose only effect is indirection.
- Follow the project's established error model. Exceptions are normal Python control/error propagation; do not reproduce C-style status plumbing unless a real API/boundary contract requires it.

Avoid **C++-in-Python**: manual lifetime state machines, low-level elementwise loops, thread assumptions copied from native code, bespoke ownership wrappers, or native rewrites when direct Python/library code is simpler and sufficient.

## Numerical and data-path performance

Apply the shared optimization order first.

- Keep large dense numerical work in established compiled/vectorized kernels when practical. NumPy/SciPy/framework operations count as compiled execution only when the actual path avoids scalable Python elementwise work.
- `numpy.vectorize` and `frompyfunc` are convenience interfaces, not acceleration.
- Bounded orchestration loops over fields, species, chunks, stages, sparse states, or irregular control flow are valid; do not densify a sparse/combinatorial algorithm merely to remove Python syntax loops.
- Account for dtype, shape, stride, contiguity, broadcasting, temporary arrays, Python-object dtype/boxing, copies, conversions, and FFI crossings on hot paths.
- Prefer existing compiled library primitives before JIT/native/custom kernels when they satisfy the scientific and deployment contract.
- Escalate to Numba/JIT, Cython-like compilation, a native extension, or a custom C++ kernel only when a remaining representative bottleneck justifies the build/package/boundary complexity.

An API that looks vectorized is not performance evidence. Measure the owning end-to-end path before claiming speedup.

## Interpreter/runtime and concurrency

Do not assume one universal Python threading model.

- Derive concurrency from the actual supported interpreter/runtime mode. Traditional GIL-constrained CPython, free-threaded CPython, alternative interpreters, and native extensions can expose different thread semantics.
- When a GIL is active, threads are appropriate for I/O, shared-read orchestration, or dominant native kernels that release it; Python-bytecode-bound CPU work may need processes or a compiled realization when that is cheaper overall.
- When free-threading is active, ordinary shared-state synchronization and extension compatibility become explicit correctness concerns; do not assume all installed extensions are free-thread-safe merely because the interpreter build is.
- Use asynchronous/event-loop execution for high-concurrency I/O or event-driven workloads when it reduces thread/process complexity and matches project architecture. Do not spread async through synchronous numerical code without a material need.
- Use processes for isolation, independent address spaces, external executables, or actual runtime constraints. Account for startup, serialization, duplicated memory, shared-memory lifetime, and IPC.
- Distributed-memory/MPI execution is an architecture capability, not a C++ feature. Use the project-appropriate Python MPI/runtime interface when distributed execution is required by accepted D3 architecture or a governed constraint.
- Model nested execution explicitly: Python workers/threads/async tasks can call BLAS, FFT, OpenMP, framework, MPI, or accelerator runtimes. Do not let each layer independently claim the full allocation.

## Effective resources

Use effective allocation from the shared performance owner. `os.cpu_count()` or similar host counts are only hints and must not override a smaller scheduler, affinity, cgroup/container, or explicit user allocation.

For long-running orchestration, keep worker counts overrideable and preserve a bounded serial/debug path when the product can support one cleanly.

## Architecture-gated accelerator realization

Accelerator work is **dormant unless** an applicable governed requirement or accepted D3 architecture enables accelerator support. CPU-only Python work must not acquire GPU probing, dependencies, device initialization, accelerator profilers, or backend fallback machinery merely because an accelerator stack is available.

When enabled, map the shared accelerator contract through the project-compatible Python execution stack. CuPy, JAX, PyTorch, Numba, or equivalent array/compiler/framework backends are examples rather than required identities.

- Prefer established accelerator array, BLAS/solver/FFT, framework, or domain kernels before custom device kernels when the computation maps cleanly.
- Treat backend/device/runtime, dtype and precision policy, compilation/JIT mode, and materially relevant library versions as execution identity when they can change scientific or performance behavior.
- Compare final governed observables against the accepted CPU/reference path under the shared scientific exact/tolerance/invariant rules; do not widen tolerances merely to accept an accelerator backend.
- Include host-device conversion and copies, transfer, synchronization, compilation/warm-up, device-memory peak/batching, and fallback transitions in owning-path performance/resource evidence when material.
- Preserve packaging/runtime/device compatibility for the supported consumer path. A fallback is required only when the product contract supports one; hardware/backend unavailability may instead be a clear unsupported configuration.

Backend availability alone does not authorize acceleration, and a framework-specific API must not become shared doctrine. The shared performance and scientific owners remain authoritative for benefit, resource bounds, and numerical equivalence.

## Tools and validation

Use shared relation-first tool routing, then select Python-appropriate evidence.

- Serena remains appropriate for supported semantic symbol/reference questions; Semgrep for supported structural families; CodeQL for supported interprocedural flow.
- Broad/combinatorial Python input or state invariants route to [Hypothesis](tool-hypothesis.md) when available and materially useful.
- Runtime state/crash questions may use `pdb`/debugpy-class debuggers or project equivalents.
- Allocation/resource questions may use `tracemalloc`, allocation/memory profilers, or framework/runtime metrics appropriate to the claim.
- CPU bottlenecks may use Python/sampling profilers plus native/backend profiling when time is spent below Python.
- Concurrency tests must reflect the actual interpreter/runtime mode; a passing GIL-constrained test does not establish free-threaded safety.

Exact tool identity remains delegated. Tool absence never relaxes the engineering claim.

## Fast static correctness

For material Python changes, use the project's configured fast lint/type/static checks when they provide high-information evidence for the changed surface. Ruff-class lint/format diagnostics and Pyright/mypy-class type analysis are representative capabilities, not mandated vendors.

Run the checks at the scope/configuration the project actually supports. A type/lint tool is not product truth, but ignoring an available configured check merely because unit tests pass discards cheap evidence. Do not introduce a second type/schema system or a new checker solely for protocol symmetry.

## Packaging and native boundaries

Preserve the project's supported interpreter/package/import/environment contract.

- Test installed/package import paths when release behavior depends on them rather than accepting source-tree imports alone.
- For native extensions, include compiler/runtime/library compatibility, extension loading, wheel/package contents, and supported interpreter threading mode where material.
- Across Python/C++ boundaries, follow the mixed-boundary rules in the router: explicit ownership/lifetime, copy/stride semantics, exception translation, runtime-lock/GIL behavior, callback/thread ownership, batching, and packaged integration.
- Generated bindings remain derived unless deliberately governed as source.

## Review challenge

For materially affected Python code ask:

1. Is the implementation using Python's high-level/library strengths instead of reproducing another language's compensating machinery?
2. Is dominant numerical work kept out of scalable Python-level loops when an equally simple compiled primitive exists?
3. Does concurrency match the actual interpreter/runtime and nested-library behavior rather than a universal GIL assumption?
4. Did a JIT/native/binding/async/process layer earn its integration and maintenance cost?
5. Would a simpler Python-native realization satisfy the same governing parent/side-constraint contract with equal or better performance fitness?

These are engineering questions, not style gates. Equivalent stylistic preferences without material correctness, performance, ownership, or maintenance effect do not block acceptance.
