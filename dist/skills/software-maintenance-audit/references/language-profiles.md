# Language Engineering Profiles

Current Protocol 6.2 shared domain doctrine is authoritative. This reference is the **language concern router**: identify affected runtime/build surfaces, then activate only the matching language profile(s). Profiles specialize execution/type/lifetime/build/packaging/performance semantics; they do not duplicate lifecycle, testing, evidence, scientific, security, performance or representation policy.

```text
shared domain rule -> language router -> active language profile(s) -> implementation-local concretization
```

## Activation

For material executable design, implementation, refactoring, performance work, or independent review, identify every language/runtime/build surface whose semantics can affect the decision:

- Python-only -> **read [Python engineering](python-engineering.md)**;
- C++-only -> **read [C++ engineering](cpp-engineering.md)**;
- Python/C++ extension/binding/embedding/callback/shared-buffer/ownership boundary -> **read both** and apply the mixed-boundary rules below;
- generated bindings/accelerator translation units activate the profile of the runtime/build surface they materially participate in; file suffix alone is not authority;
- pure documentation/literal configuration/text or genuinely language-independent architecture need not load a leaf profile.

Do not infer global Python-vs-C++ precedence. Shared owners govern cross-cutting semantics; each language profile governs its own specialization. Ordinary links from a leaf are navigation unless an explicit decision predicate activates another concern.

## Shared owners remain canonical

Profiles may specialize but never weaken or re-own parent abstractions/constraints, workflow/authority/delegation, testing/evidence/applicability, generic performance/resource/parallelism, orchestration, scientific/numerical semantics, security/trust, storage/I/O, configuration, documentation, compatibility, release/distribution, or the Lossless Representation Rule. If a profile conflicts with a shared owner, correct the profile.

## Mixed Python/C++ boundaries

When both profiles apply:

- keep one clear owner for each object/buffer/handle/thread-affine resource/lifetime;
- use compatible view/zero-copy transfer only with explicit lifetime, mutability, stride, alignment and synchronization contracts;
- batch boundary calls when dispatch dominates rather than reflexively rewriting components;
- account for error/exception translation, callback direction, interpreter/runtime locks, thread ownership, shutdown/finalization and re-entrancy where material;
- include conversion/copy/marshaling/synchronization/import/load/packaging costs in end-to-end evidence;
- test the installed/packaged extension or real supported consumer path when that boundary is the claim;
- treat generated bindings as derived unless project authority deliberately governs them as source.

Introducing/removing a material language boundary is D3 when it changes accepted ownership, deployment, application binary interface (ABI), packaging, resource, portability or performance semantics. Equivalent local concretization beneath those boundaries remains D4.

## Evidence, complexity and performance

Runtime/compiler/backend/precision changes may invalidate evidence execution without changing the target proposition. Apply the evidence owner: preserve still-valid evidence and rerun/remap only materially affected specifications.

Use language-native mechanisms to satisfy governing semantics with minimum justified total complexity. Do not translate compensating machinery mechanically across languages. An obvious equivalent efficiency improvement that adds no material complexity may proceed without a pre-change benchmark, but correctness/regression remains required and no quantitative performance claim is valid without representative measurement.

New durable language boundaries, custom native kernels, explicit SIMD dispatch, new parallel runtimes, custom allocators, backend matrices, profile-guided/link-time optimization policy or accelerators require representative evidence and total-system justification under D3/performance owners.
