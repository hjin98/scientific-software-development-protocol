# C++ Engineering Profile

Read [Language engineering profiles](language-profiles.md) first. This profile specializes shared Protocol 6.2 domain doctrine for C++ compilation, lifetime, application binary interface (ABI), native parallelism, numerical kernels, and low-level performance. Shared architecture, testing, evidence, performance, concurrency, scientific, security, release, and representation owners remain authoritative.

## Language-native design and ownership

Use C++ to express ownership, lifetime, value semantics, and compile-time contracts directly rather than reproducing dynamic-language machinery.

- Prefer resource acquisition is initialization (RAII), deterministic destruction, explicit ownership, value semantics, const-correct interfaces, moves, standard containers/algorithms, and spans/views where they reduce copying and ownership ambiguity.
- Prefer stack/value ownership when semantically appropriate. Raw pointers/references are valid non-owning views when lifetime is clear; do not introduce manual `new`/`delete`, raw owning pointers, bespoke reference counting, or custom ownership protocols without a material need.
- Use templates/concepts/static polymorphism when they remove real duplication or material dispatch cost cleanly. Avoid template/metaprogramming complexity whose compile-time, diagnostics, binary-size, or maintenance cost exceeds its product benefit.
- Dynamic polymorphism remains valid when runtime substitution is the product model; do not force static polymorphism for ideology.
- Follow the project's accepted error/application-programming-interface (API) contract—exceptions, `expected`/result/status types, error codes, assertions, or combinations—rather than imposing one universal style. Preserve exception safety and resource ownership on every failure path.
- Avoid Python-in-C++: pervasive heap objects, dictionary-like dynamic state, late binding, wrapper-heavy object graphs, or process-based parallelism copied from Python when simpler static/value/native constructs fit the contract.
- Avoid C++ cleverness for its own sake: metaprogramming, intrusive ownership, custom allocators, hand-written single-instruction multiple-data (SIMD), wrapper layers, or abstractions that do not materially improve correctness, performance, reuse, or total complexity.

## Build semantics are part of behavior

When material, affected-surface reasoning includes compiler/family/version, language standard/definitions, optimization/debug/instrumentation mode, target instruction-set architecture (ISA)/feature dispatch, standard library/runtime and third-party ABI, include/generated-header/macros/visibility/export/exception/run-time type information policy, templates/inline consumers/rebuilds, and shared/static library packaging/runtime loading.

A correct debug/sanitizer build does not prove the supported optimized build is correct; required behavior must not depend on assertions compiled out. Production performance evidence must not come from sanitizer/coverage builds. Prefer an accurate compilation database such as `compile_commands.json` when macro/include/build configuration materially affects semantic tools.

## Correctness before optimization

Treat use-after-free/scope, invalid lifetime, out-of-bounds, invalid iterators/views, uninitialized reads, invalid alias/alignment promises, undefined-behavior dependence, data races, failure-path ownership leaks, and material ABI/one-definition-rule (ODR) mismatches as correctness defects before exploiting optimizer behavior. Do not introduce restrictive/alignment/lifetime/cast/intrinsic promises for speed without proving the underlying contract.

## Numerical kernels and data layout

Apply shared optimization order first. Prefer established validated optimized primitives when the operation and dependency/precision/portability/deployment contracts fit. Dense linear algebra normally maps to Basic Linear Algebra Subprograms (BLAS)/Linear Algebra Package (LAPACK)-class APIs or established abstractions backed by tuned kernels before custom loops/SIMD; fast Fourier transform (FFT) workloads similarly prefer FFTW/vendor/platform-tuned equivalents. Apply the same principle to sparse/eigen/convolution/domain/accelerator kernels.

API identity does not force a specific backend: OpenBLAS, BLIS, oneMKL, AMD Optimizing CPU Libraries (AOCL), Accelerate and project equivalents remain delegated where the governing contract permits. Consider contiguous/strided layout, array-of-structures/structure-of-arrays, indirection, cache/translation-lookaside-buffer locality, temporaries, allocation, copies/moves, branches, false sharing and non-uniform memory access only to the depth justified by representative evidence. Do not micro-optimize a kernel while a larger algorithmic/layout/allocation/communication/language-boundary cost dominates.

## Compiler optimization, vectorization, and SIMD

After shared performance analysis identifies compiled/vector execution as material:

1. establish correct production-like optimized baseline;
2. inspect representative profiler and compiler optimization/vectorization evidence;
3. improve data/loop/alias/lifetime/layout form for safe auto-vectorization;
4. use tuned libraries or portable SIMD/runtime multiversioning when appropriate;
5. use explicit ISA intrinsics only for a still-dominant kernel whose benefit earns the complexity;
6. adopt link-time optimization (LTO), profile-guided optimization (PGO), or target tuning as durable build policy only after representative total-system evidence.

A portable product must not silently become Advanced Vector Extensions 512 (AVX-512)-only because a development machine supports it. Prefer conservative baseline + safe runtime dispatch/multiversioning or a dispatching library. Architecture-specific builds may target AVX/AVX2/AVX-512, Arm NEON/Scalable Vector Extension (SVE), or another ISA when accepted D3/constraint requires it.

Floating-point transformations that change reassociation, contraction/fused-multiply-add policy, reciprocal approximation, denormal handling, fast-math, mixed precision, or reduction order are numerical/scientific semantic questions requiring accepted equivalence evidence.

## Native concurrency and distributed execution

Concurrency class is selected by shared performance/concurrency owners; C++ supplies native concretizations.

- `std::thread`/`std::jthread`, task pools or equivalents fit irregular shared-memory tasks/asynchronous pipelines/ownership-control; prefer bounded long-lived pools over thread-per-small-task.
- OpenMP-like execution fits regular loop/data parallelism/scientific kernels when it reduces complexity and performs well on supported toolchains.
- Processes primarily serve isolation/failure containment/independent address spaces/external executables/privilege-runtime boundaries, not as a copied default from Python multiprocessing.
- Message Passing Interface (MPI)-class execution fits distributed-memory/multi-node architecture; decomposition/communication/collectives/synchronization/rank-local threading/I/O/failure assumptions remain architecture concerns.
- Model nested execution explicitly: MPI ranks x application/task threads x OpenMP x BLAS/FFT threads x accelerator work. No layer independently owns all resources.
- Async/event-driven execution is valid for I/O/network/event/pipeline workloads; do not add coroutine/event-loop machinery to ordinary synchronous numerical kernels without need.

## Evidence across toolchain changes

Compiler/standard-library/build-mode/ISA/backend changes can invalidate evidence execution without changing the target proposition. Review applicability when optimization, ABI, precision/vector path, sanitizer/instrumentation or supported runtime can plausibly change observation/interpretation; rerun/remap the same valid specification against the new candidate.

## High-return C++ tools

Use shared relation-first routing; these are mappings, not a mandatory pipeline.

- Semantic understanding: Serena when supported; clangd/ccls/compiler AST with accurate compilation database as direct fallback/complement; Semgrep for bounded structural/syntax families; CodeQL for supported interprocedural/data-flow relations when extraction/build cost is justified.
- Static/runtime safety: compiler diagnostics/clang-tidy-class checks; AddressSanitizer (ASan) for relevant memory bounds/lifetime classes; UndefinedBehaviorSanitizer (UBSan); ThreadSanitizer (TSan) for race risk; MemorySanitizer (MSan) when economical; leak/Valgrind-like tools as targeted complement. Sanitizer silence is not proof and sanitizer builds are not performance evidence.
- Runtime/fuzz/performance: GDB/LLDB-class debuggers for stack/thread/signal/core/watchpoint state; property/generative or bounded deterministic generation for broad invariants; libFuzzer/AFL++-class fuzzing for parser/decoder/binary/memory-sensitive surfaces; representative sampling profiler first for performance, compiler vectorization diagnostics for transformation questions, hardware counters when they materially explain cache/TLB/branch/vector/bandwidth/stall behavior; MPI/OpenMP/accelerator profilers only when those runtimes are present.

Exact tools remain delegated; absence of one tool does not weaken the engineering claim.

## Accelerator concretization

Graphics-processing-unit (GPU)/accelerator work is dormant unless governed requirement or accepted D3 enables it. When enabled, choose backend to supported hardware/portability: CUDA, HIP, SYCL, OpenCL, Kokkos/RAJA-like layers, or project equivalents. Prefer tuned accelerator BLAS/solver/FFT/domain primitives before custom kernels when mapping is clean.

Acceptance includes CPU/reference numerical equivalence, host-device transfer/synchronization, device-memory bounds, runtime/device identity, packaged deployment, and end-to-end benefit. GPU-specific profilers/debuggers activate only inside this architecture-gated path.

## Python/C++ boundary

When C++ participates in Python extension/embedding, also read the Python profile and apply mixed-boundary router rules: explicit buffer ownership/lifetime/stride/alignment, copy/conversion semantics, exception translation, actual interpreter threading/global-interpreter-lock mode, callbacks/re-entrancy, batching, nested library thread pools, and packaged extension loading.

## Review challenge

For material C++ ask: Is ownership/lifetime explicit and minimal? Is the abstraction C++-native rather than translated dynamic machinery? Is optimized-build behavior correct independent of debug-only instrumentation? Have tuned kernels/auto-vectorization/layout improvements been exhausted before bespoke SIMD/allocators? Does concurrency match topology without oversubscription? Did templates/dispatch/backend matrices/native boundaries/build machinery earn their compile/binary/deployment/maintenance cost? Would a simpler C++-native concretization satisfy the same governing contract?

These are engineering questions, not style gates. Apply the Lossless Representation Rule to profile use: keep this leaf cold unless C++ semantics can change the decision, and once active load only sections relevant to the material relation rather than treating the entire profile as a mandatory appendix.
