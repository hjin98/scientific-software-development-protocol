# Security and Trust Boundaries

Treat every boundary where data, code, credentials, files, processes, networks, plugins, models, native libraries, compiler/build hooks, or generated artifacts cross ownership as a security boundary. Scientific and internal tools are not exempt: trusted datasets may still be malformed, while nominally data-oriented formats/loaders may execute code or trigger unsafe native parsing.

Language profiles specialize API/runtime consequences; this shared owner defines the trust model.

## Establish the trust model before implementation

For nontrivial input, persistence, plugin, subprocess, network, archive, model-loading, native-library, or document-rendering work, identify:

- **asset** — source data, repository state, credentials, compute quota, model weights, generated results, filesystem, remote services;
- **actor/source** — user, repository, dependency, external service, downloaded artifact, collaborator, generated file, cache/checkpoint, plugin;
- **trust level** — trusted, authenticated-but-untrusted-content, untrusted, or unknown;
- **boundary** — parser, archive extraction, deserializer, subprocess, network client, plugin loader, renderer, filesystem write, cache restore, model/native loader;
- **capability granted** — read/write files, execute code, access network, allocate resources, use credentials, mutate repository/remote state;
- **failure impact** — code execution, data corruption/loss, secret exposure, path escape, denial of service, scientific-result corruption, supply-chain compromise.

Use least privilege: a component receives only the files, credentials, network access, write scope, execution capability, and resource budget it actually needs.

## Input validation is not only type validation

At every user/external boundary, validate syntax plus resource/security properties.

- Bound input byte size, item count, nesting depth, dimensions, decompressed size, and amplification factors when malformed/hostile input could exhaust CPU/RAM/VRAM/disk.
- Reject impossible or unsupported shapes/ranges before expensive allocation.
- Treat text/JSON/XML/YAML and binary formats as capable of denial of service even when direct code execution is not expected.
- Do not trust filename extensions alone when content can change parser behavior.
- Preserve enough provenance to trace an invalid/suspicious result to its source artifact.

Scientific correctness and security are complementary. Scientifically plausible input may still violate parser, path, resource, or execution constraints.

## Executable deserialization and object construction

Do not load untrusted data through a mechanism that can instantiate arbitrary objects, invoke callbacks/constructors, execute code, or load native/executable content.

Prefer data-only formats with explicit schemas for interchange. When a loader offers a restricted/data-only mode, prefer it and test compatibility. Bind trusted caches/checkpoints to provenance/integrity metadata when material; trust and validity are separate questions. Do not weaken loader safety merely because a legacy artifact fails to load—migrate or re-export trusted artifacts instead.

Python `pickle`/`shelve`, object checkpoints, language/runtime object archives, plugin/native-module loaders, and model/package formats whose loader can execute code are examples of this generic rule. The Python profile may state API-specific consequences; examples here do not make the shared rule Python-specific.

## Archives and compressed inputs

Archive extraction is a filesystem write operation.

Before extracting untrusted/external archives:

- reject absolute paths and traversal outside the designated extraction root;
- reject or constrain symlinks, hard links, device files, FIFOs, and other special entries unless required;
- bound member count, total expanded bytes, per-member size, compression ratio, and nesting where archive bombs are plausible;
- extract into a run-owned temporary directory, validate, then move only approved files;
- do not overwrite repository files or authoritative user data implicitly;
- use well-maintained library extraction-safety facilities when available rather than duplicating incomplete path logic.

Do not recursively unpack nested archives without an explicit depth/size policy.

## Filesystem and path boundaries

- Resolve/validate output roots before writes when user-controlled paths are involved.
- Prevent traversal, absolute-path, symlink, mount, or normalization tricks from escaping a designated write root.
- Do not follow symlinked directory trees during destructive cleanup or broad scans unless explicitly intended.
- Use run-owned temporary directories and restrictive permissions for sensitive intermediates.
- Avoid predictable temporary filenames where another actor/process could replace them.
- Publish important artifacts transactionally; partial output must not look complete.
- Treat external/read-only datasets as immutable even when OS permissions technically allow writes.

Before deletion, cleanup, cache eviction, or compaction, prove ownership of the target rather than relying on a broad path pattern.

## Subprocess and shell execution

Prefer direct argument-vector/process APIs over shell command construction.

- Do not concatenate untrusted strings into shell commands.
- Keep shell interpretation disabled unless shell semantics are genuinely required; in Python, `shell=False` is one API-specific example of this shared rule.
- If a shell is required, strictly define and quote/escape the accepted input domain and document why direct process execution is insufficient.
- Set working directory and environment intentionally; do not leak all parent credentials/environment without need.
- Bound runtime/output for tools that can hang or flood output.
- Check process status and validate produced artifacts; successful exit is not sufficient evidence of semantic success.
- Never execute files merely because they are present in an archive, generated directory, or dependency cache.

Package-manager, compiler, linker, build-hook, code-generator, and test execution can run arbitrary code and are privileged execution of the selected source/dependency tree.

## Network, downloads, and remote services

When fetching models, datasets, packages, schemas, toolchains, or other artifacts:

- use authenticated transport where available;
- prefer official/primary distribution sources;
- verify expected digest/signature when provided or when exact identity is security/reproducibility material;
- record source/version/digest in provenance when material;
- bound download size and timeout/retry behavior;
- do not automatically feed a downloaded file into an executable/deserialization/loading path without a trust decision;
- do not send local source, private data, findings, tokens, or full environment/configuration to remote services without explicit authorization.

Network availability must not silently change scientific semantics. Cache remote inputs only with explicit identity/invalidation rules.

## Credentials and sensitive data

- Never hard-code secrets, tokens, passwords, private keys, or credentials in source, fixtures, docs, manifests, logs, command histories, benchmark/profiler output, generated packages, or binaries.
- Prefer the repository/platform's established secret provider or environment injection mechanism.
- Pass only the credential needed for the action and scope it narrowly.
- Redact secrets and sensitive paths/metadata from durable diagnostics/evidence.
- Review staged diffs and generated packages for accidental credential/private-data inclusion.
- Do not commit `.env`, credential stores, cloud config, SSH material, browser state, or machine-specific auth caches unless the repository explicitly defines a safe non-secret fixture.

If a secret may have been exposed, report it so rotation/history remediation can occur; deleting only the latest file is insufficient.

## Dependencies, compilers, native code, and supply chain

A dependency, build backend, compiler plugin, native extension, or generated executable runs with the process/build privileges available to it.

- Reuse established dependencies before adding new ones.
- Prefer maintained packages/libraries/toolchains from authoritative sources with clear licensing/provenance.
- Pin/lock versions where reproducibility or compatibility requires it; update deliberately.
- Inspect dependency/toolchain changes separately when they can materially alter behavior/trust.
- Avoid arbitrary Git branches, URLs, local archives, unofficial mirrors, unreviewed binary blobs, or compiler plugins unless explicitly justified and provenance is recorded.
- Keep optional accelerators/plugins optional when the core product does not require their universal import/build authority.
- Treat editable installs, native-extension builds, post-install hooks, code generators, CMake/build scripts, compiler/linker hooks, and package build backends as code-execution surfaces.

Security updates may justify dependency changes even when performance/functionality do not; compatibility still requires validation.

## Plugins, callbacks, and extension points

Plugins and arbitrary callbacks execute in the host process unless an actual isolation boundary exists.

- Do not describe an in-process plugin API as a security boundary.
- Define which extension points are trusted-code-only.
- Validate declarative plugin configuration before loading implementation code.
- Keep discovery deterministic and avoid executing every file found in user-controlled directories.
- Isolate untrusted third-party extensions into a lower-privilege process/container when true trust separation is required.

The same rule applies to notebook execution, template/render filters, compiler hooks, ML callbacks, dynamic libraries, Python extensions, and C++ plugin systems.

## Document/rendering boundary

Document rendering is active processing. Markdown/HTML/CSS may reference local/remote resources, and filters/custom writers can execute code.

- Render trusted repository/user-authored source with the normal local toolchain.
- Do not enable arbitrary executable filters, shell escapes, or user-supplied render hooks by default.
- Use repository-owned templates/styles rather than downloading assets implicitly.
- Treat remote images/styles and user-controlled HTML/CSS as external inputs under the same network/resource policies.
- Render untrusted documents only in an appropriately isolated environment with restricted filesystem/network/resources.
- Verify generated output before publication; renderer success does not prove source safety.

## Resource exhaustion and denial of service

Security includes compute/storage availability. Apply resource-admission rules to untrusted or unusually large inputs: CPU time/workers, RAM/allocation shape, accelerator memory, disk/inodes, decompression/materialization amplification, network bytes/time, logs/output, parser recursion, and subprocess runtime.

Prefer actionable rejection over allowing malformed input to consume the node/filesystem.

## Security-sensitive tests

When a changed boundary is security-relevant, add focused tests for the defense class, such as traversal/absolute paths, symlink/hard-link escape, bounded decompression/resource amplification, malformed nesting, shell metacharacters as ordinary argv data, hostile filenames, stale/tampered cache identity, unauthorized output roots, secret redaction, rejection before unsafe object construction, and unapproved renderer/network execution.

Test the defense mechanism, not one malicious string.

## Security completion check

Before closing a gate that crosses a trust boundary, answer:

1. What input/code is trusted, untrusted, or unknown?
2. What filesystem/network/process/credential/resource capabilities does it receive?
3. Can it cause code execution, path escape, data loss, secret exposure, or unbounded resource use?
4. Where is validation performed, and is it before the dangerous operation/allocation?
5. Are persistence/caches protected against stale/tampered state where material?
6. Are logs/evidence/packages free of secrets and unintended private data?
7. Are dependencies/plugins/build toolchains/renderers part of the explicit trust model?
8. What security-relevant tests were actually executed?

Do not claim a component is "secure" in absolute terms. Report reviewed boundaries/mitigations and residual or unverified risks.

## Implementation-detail sources

Use current official language/runtime/library documentation when implementing concrete controls. Python `pickle`, archive extraction APIs, C/C++ parser/library contracts, compiler/toolchain behavior, and rendering/sandbox details can change independently of this shared doctrine.
