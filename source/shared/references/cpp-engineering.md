# C++ Engineering Profile

Read [Language engineering profiles](language-profiles.md) first. This profile specializes shared Protocol 6 domain doctrine for C++ compilation, lifetime, ABI, native parallelism, numerical kernels, and low-level performance. Shared architecture, testing, performance, concurrency, scientific, security, and release owners remain authoritative.

## Language-native design and ownership

Use C++ to express ownership, lifetime, value semantics, and compile-time contracts directly rather than reproducing dynamic-language machinery.

- Prefer RAII, deterministic destruction, explicit ownership, value semantics, const-correct interfaces, moves, standard containers/algorithms, and spans/views where they reduce copying and ownership ambiguity.
- Prefer stack/value ownership when semantically appropriate. Raw pointers/references are valid non-owning views when lifetime is clear; do not introduce manual `new`/`delete`, raw owning pointers, bespoke reference counting, or custom ownership protocols without a material need.
- Use templates/concepts/static polymorphism when they remove real duplication or material dispatch cost cleanly. Avoid template/metaprogramming complexity whose compile-time, diagnostics, binary-size, or maintenance cost exceeds its product benefit.
- Dynamic polymorphism remains valid when runtime substitution is the product model; do not force static polymorphism for ideology.
- Follow the project's accepted error/API contract—exceptions, `expected`/result/status types, error codes, assertions, or combinations—rather than imposing one universal style. Preserve exception safety and resource ownership on every failure path.
- Avoid **Python-in-C++**: pervasive heap objects, dictionary-like dynamic state, late binding, wrapper-heavy object graphs, or process-based parallelism copied from Python when simpler static/value/native constructs fit the contract.
- Avoid **C++ cleverness for its own sake**: metaprogramming, intrusive ownership, custom allocators, hand-written SIMD, wrapper layers, or abstractions that do not materially improve correctness, performance, reuse, or total complexity.

## Build semantics are part of behavior

C++ source is interpreted through a toolchain and build graph. When material, affected-surface reasoning includes:

- compiler and version/family;
- language standard and compile definitions;
- optimization/debug/instrumentation mode;
- target architecture/ISA and feature dispatch;
- standard library/runtime and relevant third-party ABI;
- include paths, generated headers, feature macros, visibility/export settings, exceptions/RTTI policy where governed;
- headers/templates/inline code and all consumers that must rebuild;
- shared/static library packaging and runtime loading.

A correct debug or sanitizer build does not prove the supported optimized build is correct. Required behavior must not depend on assertions or validation compiled out in production. Conversely, production-performance evidence must not come from sanitizer/coverage/instrumented builds.

For semantic tooling, prefer an accurate compilation database such as `compile_commands.json` or an equivalent project/toolchain model when macros/includes/build flags materially affect the question.

## Correctness before optimization

Treat these as correctness defects before exploiting optimizer behavior:

- use-after-free/use-after-scope and invalid object lifetime;
- out-of-bounds access and invalid iterator/reference/view lifetime;
- uninitialized reads;
- invalid aliasing/alignment promises;
- signed-overflow dependence or other undefined behavior where material;
- data races and unsynchronized shared state;
- exception/failure paths that leak or leave invalid ownership/state;
- ABI/ODR mismatches when the supported product boundary makes them material.

Do not introduce `restrict`-like promises, alignment assumptions, unchecked casts, lifetime extension tricks, or intrinsics merely to induce optimization without proving the underlying contract.

## Numerical kernels and data layout

Apply the shared optimization order first.

- Prefer established validated optimized primitives when the operation maps cleanly and dependency/precision/portability/deployment constraints are satisfied.
- Dense linear algebra should normally map to BLAS/LAPACK-class APIs or an established abstraction backed by tuned kernels before custom loops or SIMD.
- FFT workloads should normally map to FFTW-class or vendor/platform-tuned equivalents before custom FFT implementations.
- Apply the same rule to sparse solvers, eigensolvers, convolutions, domain kernels, and accelerator libraries.
- Distinguish mathematical/interface contracts from performance backends: a BLAS/LAPACK API does not imply the reference implementation is the intended performance backend. OpenBLAS, BLIS, oneMKL, AOCL, Accelerate, vendor libraries, or project equivalents remain delegated choices.
- Account for contiguous/strided layout, AoS/SoA, indirection, cache/TLB locality, temporary objects, allocation frequency, copies/moves, branch behavior, false sharing, and NUMA only to the depth justified by representative evidence.

Do not micro-optimize a kernel while a larger algorithmic, layout, allocation, communication, or language-boundary cost dominates.

## Compiler optimization, vectorization, and SIMD

After the shared performance owner identifies compiled/vector execution as material, prefer this realization order:

1. establish a correct production-like optimized baseline;
2. inspect representative profiler evidence and compiler optimization/vectorization diagnostics;
3. improve data/loop form, alias/lifetime clarity, and layout so safe auto-vectorization can succeed;
4. use established libraries or portable SIMD abstractions/runtime multiversioning when portability matters;
5. use explicit ISA intrinsics only for a still-dominant kernel whose benefit justifies the complexity;
6. adopt LTO, PGO, or target-specific tuning as durable build policy only after representative evidence establishes total-system value.

A portable x86 product must not silently become AVX-512-only because a development machine supports it. Prefer a conservative baseline plus safe runtime dispatch/multiversioning or a library that performs dispatch. Architecture-specific builds may target AVX/AVX2/AVX-512, Arm NEON/SVE, or another ISA when that target is accepted D3 architecture or another governed constraint.

Compiler transformations that change floating-point semantics—reassociation, contraction/FMA policy, reciprocal approximations, denormal handling, fast-math classes, mixed precision, or reduction order—are scientific-semantic decisions and require accepted equivalence evidence.

## Native concurrency and distributed execution

Concurrency class is selected by the shared performance/concurrency owners; C++ supplies efficient native realizations.

- Use `std::thread`/`std::jthread`, project task pools, or equivalent runtimes for irregular shared-memory tasks, asynchronous pipelines, or ownership/control that does not map cleanly to loop parallelism. Prefer bounded long-lived pools over thread-per-small-task creation.
- Use OpenMP-like shared-memory execution for regular loop/data parallelism and scientific kernels when it materially reduces implementation complexity and performs well on supported toolchains.
- Use processes primarily for isolation, failure containment, independent address spaces, external executables, privilege/runtime boundaries, or an explicitly process-oriented architecture—not as the default analogue of Python multiprocessing.
- Use MPI-class execution when distributed-memory/multi-node architecture is required. Treat decomposition, communication volume, collectives, synchronization, rank-local threading, I/O, and failure assumptions as material architecture concerns.
- Model nested execution explicitly: MPI ranks x application/task threads x OpenMP x BLAS/FFT threads x accelerator work. Each runtime must not independently assume ownership of all cores/resources.
- Async/event-driven execution is valid for I/O, network, event, or pipeline workloads; do not add coroutine/event-loop machinery to ordinary synchronous numerical kernels without need.

## High-return C++ tools

Use shared relation-first routing. These are high-return mappings, not a mandatory pipeline.

### Semantic understanding

- Use Serena for supported symbol owner/definition/reference/caller/implementation questions when available. For C/C++, a clangd/ccls-class backend is most reliable when it sees the actual compilation database and generated/include configuration.
- Direct clangd/compiler AST information is an appropriate fallback or complement when it more directly models the question.
- Use Semgrep for bounded structural/syntax families when its active C/C++ engine adequately models the pattern; do not treat it as a substitute for full compiler type/lifetime/build semantics.
- Use CodeQL for supported C/C++ interprocedural/data-flow relations when the claim and extraction/build cost justify it.

### Local static and runtime safety

- Use compiler diagnostics and clang-tidy-class AST checks for high-signal local semantic, API, portability, suspicious-conversion, modernize, and performance issues relevant to the affected code. Equivalent GCC/MSVC/vendor tools remain valid.
- Use ASan-class instrumentation for relevant out-of-bounds/use-after-free/use-after-scope/invalid-free defects.
- Use UBSan-class instrumentation for relevant undefined-behavior classes.
- Use TSan-class instrumentation when changed shared-memory synchronization creates material race risk.
- Use MSan-class instrumentation for uninitialized-memory risk only when platform/dependency support makes it economical.
- Use leak analysis or Valgrind-like tooling as a targeted complement/fallback where its model adds value; do not prefer it merely because it is traditional.

Sanitizer silence does not prove all schedules/lifetimes safe, and sanitizer builds are not performance evidence.

### Runtime state, fuzzing, and performance

- Use GDB/LLDB-class debuggers for stack/frame/thread/signal/core/watchpoint/runtime-state questions when debugger evidence is more direct than added logging.
- Route broad C++ input/state invariants to an available property/generative mechanism or bounded deterministic generation. Use libFuzzer/AFL++-class fuzzing for parsers, decoders, binary formats, and memory-sensitive input surfaces when appropriate.
- Start performance diagnosis with representative sampling profiling (`perf`, Instruments, VTune, or project/vendor equivalent) before heavy instrumentation.
- Use compiler vectorization reports for transformation questions; use hardware counters for cache/TLB/branch/vector/bandwidth/stall questions only when those measurements materially explain the bottleneck.
- Use MPI/OpenMP or accelerator-specific profilers only when those runtimes are actually part of the architecture.

Exact tool names remain delegated, and absence of one tool does not weaken the required engineering claim.

## Accelerator realization

GPU/accelerator work is dormant unless an applicable governed requirement or accepted D3 architecture enables it.

When enabled, choose the backend according to the supported hardware and portability contract: CUDA, HIP, SYCL, OpenCL, Kokkos/RAJA-like portability layers, or project equivalents. Prefer optimized accelerator libraries such as BLAS/solver/FFT primitives before custom kernels when the computation maps cleanly.

Acceptance must include CPU/reference numerical equivalence, host-device transfer/synchronization, device memory bounds, runtime/device identity, packaged deployment, and end-to-end benefit. GPU profiling/debugging tools become relevant only inside this architecture-gated path.

## Python/C++ boundary

When C++ participates in a Python extension or embedding boundary, also read the Python profile and apply the router's mixed-boundary rules. In particular, account for buffer ownership/lifetime/stride/alignment, copies/conversions, exception translation, actual interpreter threading/GIL mode, callbacks/re-entrancy, batching, library thread pools, and packaged extension loading.

## Review challenge

For materially affected C++ code ask:

1. Is ownership/lifetime explicit and simpler than the alternatives?
2. Is the abstraction appropriate for C++ rather than a translated dynamic-language pattern?
3. Is optimized-build behavior correct and independent of debug-only assertions/instrumentation?
4. Have tuned kernels/auto-vectorization/data-layout improvements been exhausted before bespoke SIMD or allocators?
5. Does concurrency match workload topology without nested oversubscription?
6. Did templates, dispatch, backend matrices, native boundaries, or build machinery earn their compile/binary/deployment/maintenance cost?
7. Would a simpler C++-native realization satisfy the same governing parent/side-constraint contract with equal or better engineering fitness?

These are engineering questions, not style gates. Equivalent stylistic preferences without material correctness, performance, ownership, portability, or maintenance effect do not block acceptance.
