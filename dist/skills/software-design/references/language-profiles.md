# Language Engineering Profiles

Current Protocol 6 domain doctrine is authoritative. Language profiles specialize that doctrine for execution, type, lifetime, build, packaging, and performance semantics that genuinely differ by language; they do not create parallel lifecycle, testing, scientific, security, or performance policies.

Use this precedence:

```text
shared domain rule -> active language profile(s) -> implementation-local realization
```

## Activation

For material executable design, implementation, refactoring, performance work, or independent review, identify every language/runtime/build surface whose semantics can affect the decision.

- Python-only executable surface -> **MUST read** [Python engineering](python-engineering.md).
- C++-only executable surface -> **MUST read** [C++ engineering](cpp-engineering.md).
- Python/C++ extension, binding, embedding, callback, shared buffer, or ownership boundary -> **MUST read both** profiles and apply the mixed-boundary rules below.
- Generated bindings or accelerator translation units activate the profile of the runtime/build surface they materially participate in; file suffix alone is not authority.
- Pure documentation, literal configuration/text edits, or genuinely language-independent architecture questions need not load a language profile when language semantics cannot change the result.

Do not infer a global Python-over-C++ or C++-over-Python precedence. Each profile governs its own side; shared owners govern cross-cutting product semantics.

## Shared owners remain canonical

Profiles refine, but do not duplicate or weaken:

- applicable parent abstractions and governed constraints, accepted-current authority versus cycle-scoped decisions, delegated realization, active simplicity, workflow, convergence, and development economy;
- testing, affected regression, integration, proxy-proof acceptance, and evidence integrity;
- generic performance order, optimized-kernel preference, data movement, resource discovery, parallelism classes, benchmark comparability, and accelerator gating;
- orchestration correctness, cancellation, failure propagation, resource ownership, and deterministic aggregation;
- scientific/numerical invariants, tolerances, provenance, and reference-oracle semantics;
- security/trust boundaries, storage/I/O, configuration, documentation, compatibility, and release/distribution.

If profile wording appears to conflict with a shared owner, the shared owner controls and the profile must be corrected. Language-specific examples in a shared reference do not convert the shared rule into language-specific doctrine.

## Mixed Python/C++ boundaries

When both profiles apply:

- keep one clear owner for each object, buffer, handle, thread-affine resource, and lifetime;
- prefer compatible buffer/view transfer and zero-copy only when lifetime, mutability, stride, alignment, and synchronization contracts remain explicit and safe;
- batch calls when boundary dispatch dominates rather than rewriting whole components reflexively;
- account for exception/error translation, callback direction, interpreter/runtime locks, thread ownership, shutdown/finalization, and re-entrancy where material;
- include conversion, copy, marshaling, synchronization, import/load, and packaging costs in end-to-end performance evidence;
- test the installed/packaged extension or real supported consumer path rather than accepting direct kernel invocation as a proxy;
- treat generated binding code as derived unless project authority explicitly governs it as source.

Introducing or removing a material language boundary is a D3 decision when it changes accepted architecture/ownership, deployment, ABI, packaging, resource, portability, or performance semantics. A local equivalent realization beneath those boundaries remains D4 discretion.

## Complexity and performance

Use language-native mechanisms to satisfy the governing contract with minimum justified total complexity. Do not translate compensating machinery from one language into another mechanically.

An obvious semantically equivalent efficiency improvement that does not add material complexity may be implemented without a pre-change benchmark. It still requires normal correctness/regression evidence, and no quantitative speedup or scaling claim may be made without representative measurement.

Escalations that add durable build/runtime/dependency machinery—new language boundaries, custom native kernels, explicit SIMD dispatch, new parallel runtimes, custom allocators, backend matrices, PGO/LTO policy, or accelerators—require representative evidence and total-system justification under the shared performance and architecture owners.
