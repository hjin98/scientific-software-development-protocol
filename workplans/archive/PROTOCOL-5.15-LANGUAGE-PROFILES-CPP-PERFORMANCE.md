---
kind: implementation-workplan
workplan_id: PROTOCOL-5.15-LANGUAGE-PROFILES-CPP-PERFORMANCE
protocol_version: 5.14.0
---

# Protocol 5.15 Language Engineering Profiles and Cross-Language Performance Workplan

## Objective / problem invariants / non-goals

### Original problem

Protocol 5.14 has a strong language-agnostic engineering doctrine, but it was developed primarily in Python scientific-software work. Most governing principles transfer cleanly to C++, while some operational guidance encodes Python execution assumptions directly. Earlier Protocol 5.15 drafts also over-corrected by placing several actually language-agnostic performance concepts inside the C++ profile.

The required outcome is one protocol that is structurally capable of producing excellent Python, C++, and mixed Python/C++ software while preserving all prior Protocol 5 doctrine. Shared references must continue to own durable engineering principles; language profiles must contain only justified consequences of each language/runtime/build model. The skills must optimize product performance and engineering quality using the minimum justified total code/system complexity rather than either translating Python habits into C++, forcing C++ machinery into Python, or duplicating shared doctrine across language branches.

### Product invariants

1. **One protocol, one doctrine.** Product truth, Tier-1/Frozen/Tier-2 authority, active simplicity, workplan semantics, affected-surface reasoning, proxy-proof acceptance, scientific correctness, security, storage, release, documentation, convergence, and development-economy rules remain language-agnostic and canonical.
2. **Shared owner before language specialization.** A language profile may refine how a shared requirement is realized; it must not redefine, weaken, duplicate, or outrank that shared requirement.
3. **Language-native engineering.** Python code should exploit Python's high-level runtime/library strengths; C++ code should exploit C++'s static type/lifetime/value/compile-time and native-performance strengths. Equivalent product behavior does not imply mechanically similar source structure.
4. **Material code-writing activates the relevant profile.** For material executable Python or C++ implementation/design/review, the active language profile is part of the normal reasoning path, not only an optional performance appendix. Purely generic architecture/documentation questions need not load language profiles.
5. **Performance-aware by default, complexity escalation by evidence.** Prefer clearly lower-work/lower-movement/lower-allocation and established optimized primitives when they do not materially increase complexity. Require representative evidence before adding durable complexity such as bespoke SIMD, new parallel runtimes, architecture-specific dispatch, PGO/LTO policy, custom allocators, new language boundaries, or accelerator backends.
6. **Performance claims still require evidence.** An obvious low-complexity efficiency improvement may be implemented without a pre-change benchmark, but a claimed speedup/scaling/resource improvement requires representative measurement unless the claim is purely structural and explicitly framed as such.
7. **Minimum justified codebase/system complexity remains lexicographically below product fitness.** Performance improvements that materially complicate ownership, portability, build/release, failure behavior, scientific semantics, dependency surface, binary size, compile/build time, or maintenance must justify their total-system cost when those dimensions are material.
8. **Mixed-language composition is first-class.** Python orchestration/API plus C++ kernels may activate both profiles. Boundary cost, ownership, error translation, build/package integration, threading/runtime mode, and data movement are part of the architecture rather than incidental glue.
9. **No global Python-vs-C++ profile precedence.** Each profile governs its own runtime/build side. Mixed-boundary rules compose the two; one profile does not silently override the other.
10. **Capability-based tool routing remains shared.** Tool choice follows the relation under the engineering claim. Language profiles map generic capability classes to appropriate language-specific tools and build/runtime evidence.
11. **Scientific semantics remain authoritative over optimization.** Backend replacement, vectorization, parallel reduction, compiler floating-point transforms, mixed precision, and accelerators require accepted exact/tolerance/invariant evidence where they can change scientific results.
12. **CPU performance mechanisms are ordinary supported capabilities, not universal product requirements.** Tuned kernels, vectorization, asynchronous/event-driven execution, shared-memory concurrency, process isolation, and distributed execution are selected by workload/architecture, not enabled merely because a machine/runtime supports them.
13. **GPU/accelerator support is architecture-gated.** GPU probing, dependencies, implementation, profiling, and qualification activate only when accelerator support is a Tier-1 requirement or explicitly Frozen architecture decision.
14. **Tool/backend identities remain delegated unless independently governed.** Serena, clangd, sanitizers, BLAS vendors, MPI implementations, profilers, and similar mechanisms are preferred or routed because of capability, not promoted into Tier 1 through protocol wording.
15. **Historical and repository-local implementation choices are not language doctrine.** The protocol repository's own Python build/validation scripts and archived workplans remain valid repository/history artifacts; do not rewrite them merely to make the protocol appear language-neutral.

### Non-goals

- Do not create separate Python/C++ lifecycle roles, duplicated protocol trees, or language-specific copies of generic architecture/testing/scientific/security doctrine.
- Do not require every C++ project to use OpenMP, MPI, intrinsics, LTO, PGO, sanitizers, multiple numerical backends, or GPU support.
- Do not require every Python project to use NumPy, multiprocessing, JIT compilation, native extensions, async I/O, or a particular framework when the workload does not justify them.
- Do not prescribe one compiler, standard library, build system, test framework, debugger, profiler, BLAS/FFT implementation, MPI implementation, property-testing library, or accelerator stack globally.
- Do not move clearly language-agnostic principles into profiles merely because their current examples arose in Python or C++.
- Do not retain language-specific hard requirements in generic shared references when the same requirement can be stated generically and specialized in a profile.
- Do not create a reference page per tool or optimization technique without independent methodological value.
- Do not retroactively rewrite archived Protocol workplans to 5.15 semantics; version binding remains authoritative.
- Do not rewrite `source/build_skills.py`, repository validation commands, or other protocol-repository implementation purely for language neutrality when their Python implementation is only this repository's Tier-2 machinery.

## Frozen high-level architecture and engineering envelope

### Frozen architecture

Protocol 5.15 uses three layers:

```text
shared doctrine / domain owners
        |
        v
thin language-profile routing
        |
        +--> Python engineering profile
        +--> C++ engineering profile
        +--> both for mixed-language boundaries
```

1. **Shared canonical owners remain authoritative.** Existing references continue to own workflow/workplans, architecture/simplicity, testing/acceptance, tool-capability selection, performance/scaling, concurrency/orchestration, scientific fidelity, storage/I/O, security/trust, release/distribution, configuration, documentation, and protocol versioning.
2. **Add one thin language-profile router plus compact Python and C++ engineering profiles.** The router classifies affected runtime/build surfaces and sends only language-dependent questions to the relevant profile(s). It must not become a second policy layer.
3. **Material executable work routes deterministically.** Design, Implementation, and independent review must read the relevant language profile for material executable work in Python or C++; mixed surfaces read both. Tiny text/config-only work can remain on shared doctrine when language semantics are immaterial.
4. **Profiles are differential.** They contain language/runtime/build-specific idioms, hazards, tools, packaging, and optimization realizations. They inherit shared doctrine by reference and do not restate it except for short local cross-links needed to explain specialization.
5. **Shared performance owns the conceptual optimization hierarchy.** Generic performance doctrine owns algorithm/work reduction, data representation/movement/locality, established optimized kernels, vectorization as a capability, parallelism classes and oversubscription, accelerator gating, effective-resource discovery, benchmark comparability, and performance-versus-complexity evidence. Profiles map those concepts into Python- and C++-appropriate realization.
6. **Shared concurrency owns execution-class semantics.** Synchronous serial execution, asynchronous/event-driven execution, shared-memory execution, process isolation, distributed-memory execution, nested parallelism, failure/cancellation, resource ownership, and deterministic aggregation are generic concepts. Python and C++ profiles explain how runtime models change preferred mechanisms.
7. **Shared tool-assisted engineering owns relation classes.** Semantic navigation, structural analysis, broad invariant generation, interprocedural flow, runtime state, memory/resource diagnosis, race diagnosis, and performance diagnosis are capability classes. Existing generic tool methods remain canonical where cross-language; profile-local methods cover genuinely language-specific evidence.
8. **Language-specific normative content is not allowed to leak into shared references without qualification.** Shared references may use Python/C++ examples, but the durable rule must be generic. Tool-specific references such as Hypothesis may remain intentionally language-specific because their subject is the tool itself.
9. **Mixed-language composition uses simultaneous profiles, not a third lifecycle.** Boundary-specific rules live in the thin router or compact shared boundary section; they must not duplicate both full profiles or introduce arbitrary profile precedence.
10. **Language placement is architecture-sensitive.** Introducing/removing a Python/C++ boundary or moving a materially owning component across languages is a Design-level architecture decision when it changes Frozen ownership/build/distribution/resource/performance boundaries; otherwise implementation-local realization remains delegated.
11. **Protocol 5.15 is a backward-compatible minor strengthening.** It changes no lifecycle or governing doctrine and does not reinterpret older workplans implicitly.

### Shared engineering envelope: performance with minimum justified complexity

The shared performance owner must distinguish two optimization classes.

**Efficiency by construction — no pre-change benchmark prerequisite when the choice is clearly semantically equivalent and does not add material complexity:**

- eliminate redundant work, parsing, I/O, copies, allocation, conversions, and synchronization;
- select appropriate asymptotic algorithms/data structures;
- preserve locality and avoid unnecessary materialization;
- reuse established optimized library primitives already compatible with the product;
- batch or stream work where doing so simplifies or preserves the architecture;
- avoid accidental nested oversubscription;
- use the actual effective CPU/memory/device allocation rather than raw hardware-count APIs as resource authority.

These changes still require ordinary correctness/regression evidence. They do **not** authorize an unmeasured quantitative speedup claim.

**Complexity-increasing optimization — representative evidence required before durable adoption:**

- new bespoke native kernels or language boundaries;
- explicit SIMD/intrinsics or architecture dispatch machinery;
- additional async/thread/process/MPI runtimes or hybrid parallel layers;
- custom allocation/pooling solely for speed;
- LTO/PGO as a governed build/release dependency rather than a local compiler experiment;
- backend proliferation or fallback matrices;
- accelerator implementation;
- scientific approximation/precision changes.

Performance evidence must measure the materially owning/user-visible path and include relevant complexity, portability, resource, build/deployment, and maintenance tradeoffs rather than only isolated kernel throughput.

### Shared build-mode correctness rule

Required product correctness must not depend on debug-only assertions, disabled validation, sanitizer instrumentation, or another non-production build property. When compile/runtime mode can change behavior, acceptance must exercise a production-like/optimized configuration in addition to any checked/instrumented configuration needed to detect defects. Instrumented builds remain correctness evidence, not production-performance evidence.

### Python engineering profile envelope

The Python profile must optimize for the actual interpreter/runtime model rather than assume one universal CPython execution mode.

- Prefer clear high-level language/standard-library/project abstractions; use context managers and deterministic resource scopes where they simplify lifetime handling; use iterators/generators/streaming where they reduce materialization; use data classes/protocol/type annotations or equivalent constructs when they improve API clarity without creating parallel schema machinery.
- Avoid unnecessary dynamic metaprogramming, reflection, wrapper layers, object churn, or abstraction whose only effect is indirection.
- Keep large dense numerical work in established compiled/vectorized kernels where practical. Treat NumPy/SciPy/framework operations as compiled execution only when they actually avoid Python elementwise work; `numpy.vectorize`/`frompyfunc` remain convenience, not acceleration.
- Account for dtype, shape, stride, contiguity, broadcasting, temporary arrays, Python-object crossings, serialization, and FFI copies on hot paths.
- **Derive concurrency from the actual Python runtime/interpreter mode.** Traditional GIL-constrained execution, free-threaded CPython, alternative interpreters, and native extensions can have different thread semantics. Do not encode `Python => GIL => processes` as a universal rule. Where a GIL is active, account for whether dominant native work releases it; where free-threading is active, treat shared-state synchronization and extension compatibility explicitly.
- Use asynchronous/event-loop execution for high-concurrency I/O or event-driven workloads when it reduces thread/process complexity and matches project architecture; do not introduce async machinery into ordinary synchronous numerical code without need.
- Choose processes when independent address spaces, isolation, or actual Python runtime constraints justify them and serialization/duplication cost is acceptable.
- Escalate to JIT/native extension/Cython-like/custom C++ kernels only when the remaining bottleneck and total integration cost justify it.
- Use Python-appropriate runtime/debug/profiling evidence when needed: debugger-class tools for runtime state, allocation/memory profilers for resource questions, sampling or Python profilers for CPU hotspots, and Hypothesis for broad property/state invariants. Exact tools remain delegated.
- Treat interpreter/version/build mode and relevant extension compatibility as part of performance/concurrency/package identity when they can change semantics. In free-threaded configurations, extension modules that require/re-enable a GIL or need separate binaries are an affected compatibility surface rather than an invisible implementation detail.
- Preserve normal Python packaging/import/environment semantics and test the installed/packaged consumer path where release claims depend on them.
- Follow project error/API conventions; do not import C-style error-code/state plumbing where normal Python exceptions/context semantics are simpler and sufficient.

### C++ engineering profile envelope

The C++ profile must optimize for C++'s actual strengths and hazards rather than emulate Python.

- Prefer RAII, explicit ownership, value semantics, const-correct interfaces, moves, spans/views, standard containers/algorithms, and clear lifetime boundaries when they reduce complexity and data movement.
- Prefer stack/value ownership and deterministic destruction when semantically appropriate; do not introduce manual `new`/`delete`, raw owning pointers, custom ownership protocols, or bespoke allocators without material need.
- Use templates/concepts/static polymorphism when they reduce duplicated code or remove material runtime cost cleanly; avoid template/metaprogramming complexity whose build/debug/maintenance cost exceeds product benefit. Dynamic polymorphism remains valid when runtime substitution is the actual product model.
- Follow the project's accepted error/API contract (exceptions, expected/status/result types, error codes, assertions) rather than imposing one universal C++ error style; preserve exception safety and resource ownership across failure paths. Debug-only assertions must not be the sole enforcement of required external/product validation.
- Treat compiler/toolchain/build configuration, ABI, headers/templates, compile definitions, standard library/runtime, target ISA, binary/runtime dependencies, and materially affected build time/binary size as part of the affected surface when they can change product behavior or total-system cost.
- Treat undefined behavior, lifetime/bounds/initialization defects, invalid alias/alignment promises, signed-overflow dependence, and data races as correctness defects before optimization.
- Prefer tuned numerical libraries and compiler auto-vectorization before explicit intrinsics when they satisfy the contract; use architecture dispatch or target-specific builds only when portability/architecture authority justifies them.
- Prefer native threads/task runtimes or OpenMP-like shared-memory execution according to workload shape; use event/coroutine runtimes only when asynchronous structure is genuinely part of the problem; use processes primarily for isolation/process architecture; use MPI-class execution when distributed-memory/multi-node architecture is required. Compose these with BLAS/FFT thread pools explicitly.
- Treat `std::thread::hardware_concurrency()`-class hardware counts as hints/upper bounds, not authoritative scheduler allocation when affinity/cgroups/HPC allocation define a smaller effective resource set.
- Use compiler-native semantic/static evidence, sanitizer-class runtime checks, debugger-class tools, sampling/hardware-counter profilers, vectorization reports, property/fuzz tools, and existing Serena/Semgrep/CodeQL capabilities according to the claim. Exact tool identity remains delegated.
- Exercise relevant optimized/release builds in acceptance where `NDEBUG`, optimization, link-time behavior, ABI, or compiler transformations can materially change results.

### Mixed Python/C++ boundary envelope

When both profiles apply:

- keep one clear owner for each object/buffer/resource and define lifetime across the boundary;
- prefer compatible buffer/array views and zero-copy transfer only when lifetime/stride/alignment contracts remain explicit and safe;
- batch calls when language-boundary dispatch dominates;
- account for exception/error translation, Python runtime threading mode, GIL acquisition/release when present, extension free-threading compatibility, callback direction, thread ownership, and interpreter shutdown where material;
- benchmark end-to-end boundary cost before rewriting large components merely to move language boundaries;
- test the packaged/imported extension or real consumer path, not only direct kernel invocation;
- treat generated binding code as derived unless the project governs it as source;
- introducing a new language boundary must justify build/package/dependency/ABI complexity against the product benefit, not merely local kernel speed.

## Implementation obligations and delegated solution space

### O1 — Perform a protocol-wide language-specificity census before editing

**Concern / rationale:** Python-specific normative wording exists in performance, tool routing, security, and user-facing routing. A partial extraction would leave inconsistent doctrine ownership.

**Required end state / constraint:** Inspect canonical current shared references and role/README routing surfaces for language-specific normative statements. Classify each occurrence as:

1. genuinely shared and generalizable;
2. a language-specific realization that belongs in a profile;
3. an intentionally language-specific tool/reference (for example Hypothesis);
4. a harmless example whose generic rule is already clear;
5. repository-local implementation/history that should remain untouched.

Generalize or route categories 1-2. Do not mechanically purge language names from examples. Do not rewrite archived workplans or this repository's own Python build/validation implementation merely for neutrality.

**Expected surfaces:** at minimum `performance-and-parallelism.md`, `tool-assisted-engineering.md`, both role entrypoints, `source/README.md`, root `README.md`, `PORTABILITY.md`, `security-and-trust-boundaries.md`, `testing-and-validation.md`, `concurrency-and-orchestration.md`, `release-and-distribution.md`, current qualification scenarios, and current package-generation registry/routing.

**Acceptance evidence:** no remaining unqualified Python/C++ implementation requirement in a generic owner unless the owner itself is intentionally language/tool specific; historical/version-bound artifacts remain historically intact.

### O2 — Implement the thin language-profile router and composition rule

**Required end state / constraint:** Introduce a compact canonical route:

```text
shared domain rule -> active language profile(s) -> implementation-local choice
```

For material executable Design, Implementation, and independent review, identify every materially affected implementation/runtime language and read the corresponding profile. Documentation-only, metadata-only, or purely generic architecture questions need not load profiles when language semantics cannot affect the decision.

The router must explicitly handle Python-only, C++-only, Python calling C++, C++ embedding Python, generated bindings, alternative/free-threaded Python runtimes, and accelerator translation/runtime surfaces. File suffix alone is insufficient.

When both profiles apply, compose them by boundary ownership; do not define Python-over-C++ or C++-over-Python precedence.

**Anti-shortcut:** Do not duplicate this routing logic independently in Design and Implementation entrypoints beyond short mandatory links to the canonical router.

### O3 — Refactor generic performance doctrine around shared concepts

Keep these concepts in `performance-and-parallelism.md`:

- work/asymptotic/data-layout/data-movement optimization order;
- efficiency-by-construction versus evidence-required complexity escalation;
- distinction between no pre-benchmark requirement for obvious low-complexity improvement and evidence required for quantitative performance claims;
- established optimized kernels/libraries before bespoke low-level machinery when they satisfy product constraints;
- vectorization/compiled execution as a capability, not a Python- or C++-specific syntax rule;
- representative profiling before non-obvious optimization;
- serial, async/event-driven, shared-memory, process-isolation, distributed-memory, and nested-parallel execution classes;
- effective allocation/resource discovery rather than raw host hardware counts;
- benchmark comparability and longitudinal regression;
- GPU/accelerator architecture gate.

Language profiles map these concepts to concrete realizations.

### O4 — Build a full Python engineering profile, not only a performance appendix

The Python profile must cover language-native abstraction/API/resource/error style, interpreter/runtime variants, object-model costs, numerical execution, concurrency including async and free-threaded/GIL-constrained modes, testing/tooling, packaging, and mixed-boundary behavior.

It must preserve valid existing Python rules while explicitly avoiding:

- **C++-in-Python:** excessive manual lifecycle/state machinery, low-level loops, thread assumptions, or native rewrites when high-level Python/library code is simpler and sufficient;
- **Python-performance denial:** retaining Python-level work on a dominant numerical path merely because the code is concise when an established compiled/vectorized realization is materially better and no more complex overall;
- **GIL monoculture:** treating the GIL as a universal Python language property instead of a runtime/build/extension condition.

### O5 — Build a full C++ engineering profile, not only a performance/tool appendix

The C++ profile must cover idiomatic ownership/lifetime/value design, compile-time/runtime abstraction choice, error contracts, build/ABI, memory/UB/race safety, numerical kernels, vectorization/SIMD, concurrency, tooling, packaging, and mixed-boundary behavior.

It must explicitly avoid:

- **Python-in-C++:** pervasive heap/dynamic dictionaries/late binding/wrapper layers or process-based parallelism copied from Python where static/value/native C++ constructs are cleaner;
- **C++ cleverness for its own sake:** template metaprogramming, bespoke allocators, intrusive ownership, custom SIMD, or abstraction scaffolding without material correctness/performance/complexity benefit;
- **debug-build correctness:** relying on assertions/instrumentation that disappear or materially change in the shipped optimized build.

### O6 — Preserve generic optimized-kernel doctrine and specialize library maps

**Shared rule:** Prefer an established validated optimized primitive when the algorithm maps cleanly and the dependency satisfies precision, portability, licensing, deployment, and ownership requirements.

**Python map:** NumPy/SciPy and established framework kernels, including tuned BLAS/LAPACK/FFT/sparse backends underneath them where relevant. Avoid assuming a Python API is fast merely because it is vector-looking; materialization and Python-object paths still require profiling when performance matters.

**C++ map:** BLAS/LAPACK-family interfaces, FFTW-class FFTs, sparse/eigensolver/domain libraries, and vendor-tuned equivalents such as OpenBLAS/BLIS/oneMKL/AOCL/Accelerate or project-approved alternatives. Distinguish mathematical/interface contract from selected performance backend.

### O7 — Preserve generic concurrency classes and specialize runtime selection

**Shared owner:** concurrency/orchestration + performance own serial versus async/event-driven execution, resource topology, deterministic aggregation, nested parallelism, failure/cancellation, oversubscription, process isolation, and distributed-memory semantics.

**Python specialization:** actual interpreter/runtime threading mode; GIL-aware behavior only when a GIL is active; free-threaded shared-state synchronization and extension compatibility when applicable; native-library thread pools; async/event-loop I/O where appropriate; serialization/shared-memory costs; MPI through project-appropriate Python interfaces when distributed execution is Frozen.

**C++ specialization:** native threads/task pools for irregular shared-memory work; OpenMP-like execution for regular loop/data parallelism; coroutine/event-loop runtimes where asynchronous architecture warrants them; processes for isolation/process architecture; MPI-class execution for distributed/multi-node architecture; hybrid MPI + threads/OpenMP + BLAS/FFT composition.

**Anti-shortcut:** Do not make MPI or GPU a C++-only concept, or the GIL a universal Python concept.

### O8 — Preserve generic effective-resource discovery and specialize APIs

**Shared rule:** use actual scheduler/affinity/cgroup/container/job/user allocation as authority; hardware counts are hints/upper bounds. Account for RAM/VRAM/I/O allocations similarly.

**Python examples:** `os.cpu_count()` and similar APIs are not automatically effective allocation; use affinity/cgroup/scheduler/project information when material.

**C++ examples:** `std::thread::hardware_concurrency()` and system APIs are not automatically effective allocation; use platform/scheduler/project information when material.

Do not hard-code either language API into generic doctrine.

### O9 — Preserve generic accelerator gating and specialize accelerator realizations

**Shared rule:** No accelerator obligations exist unless Tier-1/Frozen architecture enables accelerator support. When enabled, acceptance requires end-to-end benefit, numerical/reference equivalence, transfer/synchronization cost, memory bounds, backend/device identity, and target-hardware evidence.

**Python examples:** CuPy/JAX/PyTorch/Numba or project-equivalent accelerator execution when compatible with the architecture.

**C++ examples:** CUDA, HIP, SYCL, OpenCL, Kokkos/RAJA-like portability layers, or project-equivalent execution according to supported hardware/portability contract.

Prefer optimized accelerator libraries before custom kernels when operations map cleanly. Exact frameworks remain delegated.

### O10 — Generalize tool-capability routing and map language-specific tools

`tool-assisted-engineering.md` and role routing must express generic relation classes first, then concrete methods:

- literal/path/text relation -> ordinary repository search/read;
- symbol owner/definition/reference/caller relation -> Serena or another supported semantic capability under existing policy;
- AST/syntax/structural relation -> Semgrep where supported;
- broad/combinatorial input/state invariant -> language-appropriate property/generative method; Python -> Hypothesis when available; C++ -> project property/generative method or bounded deterministic generation;
- interprocedural flow/taint/source-to-sink -> CodeQL where supported;
- runtime state/crash -> language-appropriate debugger when it materially reduces uncertainty;
- memory/lifetime/UB/resource -> language-appropriate runtime/static instrumentation;
- race/synchronization -> language-appropriate race/concurrency evidence;
- performance bottleneck/vectorization -> language-appropriate profiler/compiler/hardware evidence.

Existing Serena/Semgrep/CodeQL/Hypothesis references remain canonical for their tool methods. Do not create a second Serena/clangd navigation architecture.

**Python mapping:** existing Serena/Semgrep/CodeQL/Hypothesis plus Python debugger/profiler/memory tools as appropriate; exact additional tool names remain delegated.

**C++ mapping:** existing Serena/Semgrep/CodeQL where supported; compiler diagnostics and clang-tidy-class AST checks; ASan/UBSan-class checks for relevant memory/UB risk; TSan-class checks for relevant shared-memory race risk; MSan/leak analysis when material and economically supportable; GDB/LLDB-class debugger for runtime state; sampling profilers/vectorization reports/hardware counters for performance; libFuzzer/AFL++-class fuzzing where the input surface warrants it. These are capability examples, not a fixed pipeline.

### O11 — Add C++ compiler/vectorization/SIMD realization without moving generic doctrine

After the shared performance owner selects vectorization/compiled optimization as relevant, the C++ profile should use this evidence-directed order:

1. production-like optimized compiler baseline;
2. compiler optimization/vectorization diagnostics plus representative profiler evidence;
3. data/loop changes that allow safe auto-vectorization;
4. established portable SIMD/library abstraction or runtime multiversioning when portability matters;
5. explicit SSE/AVX/AVX2/AVX-512 or NEON/SVE-class intrinsics only for a still-dominant kernel with justified complexity;
6. LTO/PGO/target tuning after representative evidence if they become durable build policy.

A portable product must not silently become AVX-512-only because the development machine supports it. An architecture-specific build may use AVX-512 when target ISA is explicitly product/Frozen authority.

No alias/alignment/restrict-like promise may be introduced solely to induce vectorization without a proved lifetime/layout contract.

### O12 — Make language-native abstraction quality an explicit review dimension

For materially affected executable work, Design, Implementation final reconciliation, and independent review must ask:

- Is the realization idiomatic for the active language/runtime and compatible with project architecture?
- Does it use the language's simpler native ownership/resource/data/error/abstraction mechanisms instead of reproducing another language's compensating machinery?
- Does an abstraction reduce total complexity or duplicate it?
- Is a performance-critical abstraction actually zero/low-cost enough for its role, or is runtime cost accepted by Tier-1 requirements?
- Would a simpler language-native realization satisfy the same product/Frozen contract?
- Did the chosen realization create material build/compile/binary/dependency complexity that should count against its benefit?

This is an engineering challenge, not a style-policing gate. Equivalent stylistic preferences with no material correctness/performance/maintenance benefit do not block acceptance.

### O13 — Generalize security wording where shared owner leaks Python APIs

Keep generic rules in the shared security owner:

- prefer direct argument-vector/process APIs over shell interpretation;
- do not execute untrusted deserialization/object-construction formats;
- bound parser/input/resource amplification;
- treat compiler/build/package hooks as privileged execution.

Language-specific examples may remain, but Python-specific API directives such as `shell=False` or pickle details belong in the Python profile or must be clearly examples of the generic rule. C++ profile may add relevant parser/loader/system-call/build-hook consequences without duplicating trust doctrine.

### O14 — Preserve scientific doctrine as shared authority across profiles

Do not move numerical invariants/tolerances/reference-oracle/approximation/provenance rules into a profile. Profiles only map where language/runtime/compiler choices can perturb those semantics.

Python examples include dtype/backend changes, interpreter/runtime mode, compiled library replacement, multiprocessing/threading ordering, JIT, and accelerator substitutions.

C++ examples include floating-point contraction/reassociation, `fast-math`-class flags, vector reductions, OpenMP/MPI reduction order, vendor BLAS/FFT changes, mixed precision, and accelerator substitutions.

Do not widen tolerances merely to bless a faster realization.

### O15 — Reconcile release/build/package integration without duplicating release doctrine

`release-and-distribution.md` remains language-agnostic: build what users receive and exercise the supported consumer path.

Python profile specializes interpreter/package/import/environment semantics, runtime threading/free-threading compatibility, and native-extension packaging when present.

C++ profile specializes compiler/build configuration, optimized-versus-instrumented modes, shared/static libraries, exported interfaces, headers/templates, runtime dependencies, ABI compatibility only where product promises it, and supported platform/toolchain combinations.

Mixed Python/C++ products must test the installed extension through the packaged Python import/call path plus any direct C++ consumer boundary independently supported.

Required runtime validation must not live solely in debug-only assertions that may be disabled in a supported production mode.

### O16 — Reconcile documentation, portability, qualification, and package generation

Implementation must update every duplicated/exposed current routing surface, including:

- `source/PROTOCOL_VERSION`;
- `source/README.md` and root `README.md`;
- both core role `SKILL.md` files;
- `PORTABILITY.md`;
- `source/shared/references/performance-and-parallelism.md`;
- `source/shared/references/concurrency-and-orchestration.md` where generic execution classes/resource routing need clarification;
- `source/shared/references/tool-assisted-engineering.md` and existing tool method pages as needed;
- `source/shared/references/security-and-trust-boundaries.md` for genericized language leakage;
- `source/shared/references/testing-and-validation.md` where generic build-mode/property/runtime evidence semantics need clarification;
- `source/shared/references/scientific-software.md` only for minimal cross-links if required; do not duplicate doctrine;
- `source/shared/references/release-and-distribution.md` only for generic compiled-artifact wording that belongs there;
- new thin language router + Python/C++ profile references;
- `source/shared/references/protocol-versioning-and-compatibility.md`;
- `source/build_skills.py` only as needed to package the new references, not to rewrite its Python implementation;
- `qualification/tool-routing/SCENARIOS.md`, portability/reference-routing qualification where affected, and repository tests such as `tests/test_protocol_portability.py`;
- generated `dist/` artifacts and indexes.

Archive/history policy:

- do not edit `workplans/archive/` merely to adopt Protocol 5.15 terminology;
- do not reinterpret completed older workplans under 5.15;
- update only current documentation/qualification/source that exposes the live protocol contract.

Bundle the minimum references required for deterministic routing. Do not put every language/tool reference into unrelated specialists solely for completeness.

## Implementation authority

### Frozen

- Protocol 5 governing hierarchy, two-role lifecycle, accepted-workplan semantics, active simplicity, convergence, snapshot completeness, proxy-proof acceptance, and development-economy doctrine remain unchanged.
- Shared canonical domain owners outrank and constrain language profiles.
- One thin language router plus differential Python/C++ engineering profiles; no parallel protocols.
- Material executable work in Python/C++ deterministically activates the relevant profile; mixed-language work composes both without arbitrary precedence.
- Language profiles cover general language-native engineering, not only performance.
- Shared performance owns common optimization concepts and evidence thresholds; profiles own language-specific realization.
- Shared concurrency owns execution classes including async/event-driven execution; profiles own runtime-specific selection.
- Shared tool-assisted engineering owns relation/capability classes; profiles/tool references own language/tool-specific methods.
- Shared resource discovery treats hardware-count APIs as hints rather than effective allocation authority.
- Mixed Python/C++ surfaces activate both profiles and explicit boundary reasoning; introduction/removal of a material language boundary follows normal Frozen-architecture rules.
- Python profile must not assume a universal GIL; actual interpreter/runtime/extension threading semantics govern concurrency decisions.
- Required correctness must survive supported production/optimized modes rather than depend on debug-only assertions or instrumentation.
- GPU/accelerator obligations are activated only by Tier-1/Frozen architecture.
- Scientific semantics remain shared authority over all language/backend/compiler optimizations.
- Historical workplans and protocol-repository Python implementation are not retroactively generalized merely for appearance.
- Protocol target is 5.15.0 and is backward-compatible under existing version-binding rules.

### Delegated

- Exact names/internal structure of the thin router and two profile files, provided canonical ownership and progressive disclosure remain clear.
- Exact compiler, build system, sanitizer, debugger, profiler, property/fuzz framework, BLAS/LAPACK/FFT backend, thread/task/async runtime, MPI implementation, accelerator framework, SIMD abstraction, and package manager.
- Serena versus another equally reliable supported semantic backend in a concrete environment, subject to existing deterministic capability-routing policy; reuse existing Serena capability when available/suitable rather than building duplicate machinery.
- Exact C++ exception/result/error style when project/product authority has not fixed it.
- Exact Python type/data-class/protocol/error mechanisms when project architecture has not fixed them.
- Whether a downstream product uses serial, async/event-loop, threads, OpenMP-like runtime, processes, MPI, or a hybrid unless product architecture freezes the choice.
- Exact architecture dispatch and CPU feature-selection mechanism.
- Exact Python interpreter/runtime mode unless product compatibility requirements fix it; implementation must still detect/honor the actual supported mode when behavior depends on it.

### Reopen only on evidence

Reopen Design only if implementation evidence shows:

- shared doctrine cannot be kept canonical without materially duplicating it in language profiles;
- deterministic profile routing cannot be packaged without unacceptable always-loaded duplication or ambiguity;
- mixed-language boundaries require a materially different authority/lifecycle model rather than simultaneous profiles;
- a Frozen platform/portability requirement makes the shared optimization model infeasible;
- an explicitly accelerator-first architecture conflicts irreconcilably with the shared default route and requires a different high-level performance architecture.

Ordinary absence/weakness of a tool/backend/runtime is not redesign; use capability fallback. Ordinary project preference for another idiom/tool is delegated unless it changes product/Frozen architecture.

## Affected surface and task-specific acceptance

The affected surface must be re-derived after implementation. Initial expected surfaces are those listed in O16 plus generated skill bundles.

Task-specific acceptance must demonstrate:

1. **Doctrine preservation:** no change weakens Tier-1 product truth, Frozen architecture semantics, active simplification, acceptance integrity, convergence, snapshot completeness, or development-economy guarantees.
2. **Shared/profile precedence:** a profile cannot override a shared scientific/security/testing/performance requirement.
3. **Profile activation:** material Python/C++ executable design/implementation/review deterministically reads the relevant profile; mixed work reads both; generic non-code work need not load irrelevant profiles.
4. **Mixed-profile composition:** Python and C++ profile rules compose at their boundary without a global precedence rule.
5. **Shared-reference purity:** generic references express durable rules independently of Python/C++, with language names appearing only as examples, explicit routes, or intentionally language/tool-specific sections.
6. **Historical/repository-local preservation:** archived workplans and the protocol repository's own Python build scripts are not rewritten merely for language neutrality.
7. **Python-native design scenario:** a representative numerical/data task yields high-level Python orchestration plus appropriate compiled/vectorized primitives rather than a literal C++-style low-level translation.
8. **Python runtime-variant scenario:** a GIL-constrained runtime, a free-threaded runtime, and an extension that changes threading compatibility do not all receive the same thread/process prescription.
9. **Python async scenario:** high-concurrency I/O can route to an async/event-driven realization without imposing async on ordinary synchronous numerical code.
10. **C++-native design scenario:** the analogous task yields clear value/lifetime/resource semantics and native compiled execution rather than Python-like dynamic/process machinery.
11. **Performance-versus-complexity scenario:** an obvious zero/low-complexity efficiency improvement may be adopted without pre-benchmark ceremony, while complexity-increasing optimization requires representative evidence.
12. **Performance-claim integrity:** an unbenchmarked efficiency-by-construction change cannot be reported as a measured speedup; quantitative claims require comparable evidence.
13. **Build-mode correctness:** required behavior remains correct in a supported production-like/optimized configuration and does not rely solely on debug assertions or sanitizer instrumentation.
14. **Common optimized-kernel scenario:** the same BLAS/FFT-class requirement routes through one shared optimized-library principle and then to different Python/C++ realizations.
15. **Common parallelism scenario:** async/event-driven, shared-memory, process isolation, and MPI/distributed execution are generic architecture classes; Python and C++ choose different runtime mechanisms where justified.
16. **Effective-resource scenario:** `os.cpu_count()`/`hardware_concurrency()`-class host counts cannot override a smaller scheduler/affinity/cgroup allocation.
17. **Nested parallelism scenario:** Python/C++ outer execution plus BLAS/FFT/OpenMP/MPI layers cannot each independently claim the full machine.
18. **Tool-routing scenario:** semantic, structural, property/generative, interprocedural, runtime-state, memory/UB, race, and performance questions route by capability and language rather than one fixed C++ stack.
19. **C++ safety scenario:** memory/lifetime/UB/race risk can route to sanitizer/compiler/runtime evidence without making those tools universal gates.
20. **C++ vectorization scenario:** missed vectorization is diagnosed before intrinsics; portable code does not become AVX-512-only without architecture authority.
21. **Python performance scenario:** Python elementwise hot loops are challenged when compiled primitives exist, while bounded orchestration loops remain valid.
22. **Security transfer scenario:** shared shell/deserialization/trust rules remain language-agnostic; Python/C++ profiles provide justified API-specific consequences without duplicating trust model.
23. **Scientific-equivalence scenario:** `fast-math`, dtype/precision/backend changes, vector/parallel reductions, and accelerators cannot obtain a pass by relaxing tolerances without authority.
24. **Mixed-language scenario:** Python/C++ binding performance, copies, ownership, actual Python threading mode/GIL behavior, exceptions, packaging, and real-boundary integration are evaluated together.
25. **Language-boundary architecture scenario:** a cross-language rewrite or new binding layer that materially changes build/ownership/performance architecture cannot be introduced as an incidental local optimization without appropriate Design authority.
26. **GPU gating:** CPU-only architecture loads no GPU implementation/tooling obligations; explicitly GPU-enabled architecture activates target-device numerical/performance/resource evidence in either Python or C++.
27. **Documentation/routing parity:** root/source README, role entrypoints, PORTABILITY, qualification scenarios, and built skill bundles agree on the new routing model.
28. **Package integrity:** every routed reference exists in each role bundle that links to it; unrelated specialists do not acquire unnecessary profile payload.
29. **Repository-required final checks:** run the canonical Protocol 5.15 equivalent of:

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

These Python commands are this repository's validation implementation, not language-specific product doctrine.

Production qualification is unnecessary for the protocol repository itself. Downstream products require target-machine qualification when Tier-1 claims depend on actual CPU ISA, NUMA topology, MPI/network topology, accelerator hardware, production-scale I/O, interpreter/runtime mode, or production-scale performance.

## Implementation sequence and genuine redesign / simplification triggers

### Stage 1 — Protocol-wide language-specificity census

Audit current canonical shared references and exposed routing/docs. Produce the minimal ownership map: shared rule, Python specialization, C++ specialization, intentional tool-specific rule, or repository/history implementation that remains untouched. Generalize shared language leakage before adding new language content.

Close with focused documentation/routing tests proving existing Protocol 5.14 doctrine is still represented.

### Stage 2 — Install the three-layer routing architecture

Add the thin language router and compact Python/C++ engineering profiles. Update role routing and skill packaging. Establish shared > profile > implementation-local precedence, mandatory profile activation for material executable work, and mixed-profile composition without global language precedence.

Close routing/package tests before substantive profile expansion.

### Stage 3 — Refactor shared performance/concurrency/tool/security ownership

Move common concepts out of language-specific wording: optimized kernels, vectorization capability, async/shared/process/distributed parallelism classes, effective resource discovery, profiling, GPU gating, generic property relation, shell/deserialization wording, build-mode correctness. Preserve current valid Python behavior through the profile while removing universal-GIL assumptions.

### Stage 4 — Complete Python and C++ language-native engineering profiles

Add general idiomatic engineering, runtime variants, performance realization, async/concurrency, build/package semantics, tooling maps, and mixed-boundary consequences. Add C++ compiler/sanitizer/debugger/SIMD detail only here or in justified tool-specific references; keep generic owners clean.

### Stage 5 — Qualification integration

Add counterfactual scenarios for language-native design, runtime variants, shared-versus-profile ownership, performance-versus-complexity escalation, performance-claim evidence, optimized build correctness, effective resource discovery, async execution, tool routing, optimized kernels, parallelism, security transfer, mixed Python/C++, language-boundary architecture, and GPU gating. Update root/source documentation and portability qualification.

### Stage 6 — Version/package/final acceptance

Bump to 5.15.0, reconcile version history, regenerate `dist/`, re-derive final affected surfaces, run complete repository checks, and inspect built bundles for routing completeness and unnecessary duplication. Preserve archived workplans under their historical versions.

### Active simplification triggers

Before adding another durable file/tool abstraction/route, simplify or re-derive if implementation shows:

- shared doctrine copied into both profiles;
- separate Python/C++ versions of performance, concurrency, security, or testing references;
- a language router that becomes a policy owner instead of a thin selector;
- a fixed C++ tool pipeline instead of relation-directed selection;
- separate Serena and clangd semantic-navigation architectures solving the same problem;
- one page per compiler/sanitizer/profiler with no distinct method;
- duplicated MPI/GPU/async doctrine across profiles;
- wrappers around BLAS/FFT/SIMD created only to satisfy protocol wording rather than reduce product complexity;
- language profiles prescribing style preferences without material engineering effect;
- qualification tests freezing exact prose/file/tool identity rather than semantic routing;
- accelerator machinery leaking into CPU-only tasks;
- cross-language rewrites being proposed before boundary/data-movement/algorithm simplification has been considered;
- repository-local Python implementation or historical workplans being rewritten merely for appearance;
- runtime assumptions such as universal GIL behavior being encoded where a capability/runtime check is more accurate.

### Genuine redesign triggers

Return to Software Design only if evidence demonstrates that shared doctrine plus differential simultaneous profiles cannot represent the required product, or that Frozen portability/accelerator/language-boundary architecture itself must change. Individual tool/backend availability, interpreter build mode, compiler choice, library choice, or idiomatic implementation preference is not redesign unless product/Frozen authority makes it so.

## Independent review rework — implementation blockers

Independent Design review of implementation commit `8ae1ba726931974d80b431c1189a4a73cde68e58` returned **NO PASS** on two implementation nonconformances. The Frozen three-layer architecture remains valid; this is bounded implementation repair, not redesign.

### R1 — Complete Python accelerator specialization under the existing shared gate

**Problem:** the shared performance owner correctly makes accelerator support dormant unless Tier-1/Frozen architecture enables it, and the C++ profile contains a differential enabled-accelerator realization, but the Python profile does not yet carry the corresponding language-specific realization required by O9/O14.

**Required end state:** keep all generic accelerator policy, evidence thresholds, and scientific equivalence in shared owners. Add only the Python-specific consequences needed once accelerator architecture is enabled: project-compatible Python array/compiler/framework backend selection, established accelerator-library preference before custom kernels, dtype/precision/backend identity, transfer/synchronization/device-memory accounting, CPU/reference equivalence, package/runtime/device compatibility, and explicit fallback only when the product supports fallback. CPU-only architecture must incur no Python GPU dependency/probing/tooling obligation. Exact framework/tool identity remains delegated.

**Acceptance:** a CPU-only counterfactual leaves accelerator machinery dormant; a GPU-enabled Python counterfactual activates language-specific realization while still routing numerical equivalence and performance evidence to shared owners. The profile must not encode absence of a particular framework name as the gating invariant.

### R2 — Replace brittle wording/implementation-identity acceptance with directional semantic and real-package checks

**Problem:** the initial 5.15 regression file primarily asserted selected prose, concrete tool names, exact profile filenames, and the internal `LANGUAGE_PROFILES` build variable. That can remain green in the presence of contradictory authority text and freezes delegated Tier-2 identities contrary to the accepted plan's simplification trigger.

**Required end state:** retain lightweight structural tests only where structure is Frozen or objectively packaged. Derive active profile resources from lifecycle-entrypoint routing rather than duplicating their filenames/build-variable identity in the test oracle. Exercise the real package builder and verify that derived routed resources are present in lifecycle bundles and absent from unrelated specialists. Add directional/counterfactual checks for shared-over-profile authority, no global Python-vs-C++ precedence, runtime-sensitive Python concurrency, disabled-versus-enabled accelerator behavior, evidence-before-complexity escalation, and architecture-sensitive language boundaries. Keep named tools/frameworks as examples, not acceptance identities.

**Acceptance integrity:** a representative contradictory shared/profile precedence statement or global language-precedence statement must be rejected by the directional guard; package acceptance must follow the real generated bundle rather than inspect an internal Python constant; changing a delegated tool/framework example must not by itself fail the protocol contract.

### Rework scope and closure

Expected repair surface is limited to the active workplan, `source/shared/references/python-engineering.md`, the existing Protocol 5.15 qualification scenarios, the Protocol 5.15 regression test, and generated `dist/` descendants. Do not add a new lifecycle role, policy layer, validator framework, tool page, compatibility wrapper, or accelerator dependency. Re-run the complete repository suite, canonical package generation/validation, committed-distribution parity, and whitespace checks on the assembled candidate.

## Design verdict

**REOPENED — bounded implementation repair required; Frozen architecture unchanged.**

The final reviewed plan preserves prior Protocol 5 doctrine as sole shared authority, treats Python and C++ as language-native realizations rather than parallel protocols, moves common performance/parallelism/tool concepts back to shared owners, broadens profiles into complete engineering profiles, removes accidental tool/backend freezing, distinguishes implementation permission from performance-claim evidence, handles modern Python runtime variants rather than assuming a universal GIL, protects optimized/release-build correctness, generalizes effective resource discovery and asynchronous execution, preserves historical/version-bound artifacts, and makes performance-versus-complexity optimization explicit. The structure is intended to produce high-performance code with minimum justified total code/system complexity in either language while remaining capable of clean mixed Python/C++ scientific software.
