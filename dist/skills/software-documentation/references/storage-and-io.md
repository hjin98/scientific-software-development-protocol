# Disk I/O, Storage, Caching, and Recovery

Treat storage as a first-class execution resource alongside CPU, RAM, GPU, and VRAM. A pipeline that is computationally efficient can still be unusable if it performs excessive reads/writes, creates an unbounded cache, requires long restart reconstruction, or exhausts scratch space/inodes.

## Classify every persistent artifact

Before designing persistence, classify each artifact as one of:

- **authoritative input** - user/source data that must not be modified;
- **durable output** - a result the workflow promises to preserve;
- **checkpoint/recovery state** - enough state to resume without repeating unacceptable work;
- **reusable cache/index** - regenerable acceleration state with explicit validity rules;
- **temporary/scratch state** - disposable intermediate data owned by the current run;
- **evidence/logging** - diagnostics, benchmark records, or audit output with bounded retention.

For each nontrivial artifact define owner, schema/version, expected size, creation/update mode, validity/invalidation, retention/eviction, cleanup, and recovery role. Do not let a cache become an undocumented second source of truth.

## Optimization order for storage-heavy paths

Prefer, in order:

1. eliminate unnecessary reads, writes, copies, parsing, and serialization;
2. avoid materializing data that can be streamed, recomputed cheaply, or represented by a compact manifest/index;
3. choose an access pattern and layout that match actual reads (sequential, random, chunked, field-selective);
4. reuse validated intermediates without reopening/rebuilding them inside inner loops;
5. batch small operations to reduce metadata/open/close overhead and tiny-file proliferation;
6. use compact binary/chunked representations for large numerical arrays when appropriate;
7. use compression only when measured I/O savings justify CPU/decompression cost;
8. stage hot data to suitable local scratch when shared/network storage is the bottleneck and project/HPC policy permits it;
9. add I/O concurrency only after measuring the storage device/filesystem saturation point.

Do not "optimize" recovery by persisting every intermediate. Persist only enough state to reduce expected recomputation/recovery cost without causing larger steady-state I/O and storage amplification.

## Storage admission and budgets

A long-running stage should preflight storage when it can create large artifacts.

Estimate, where practical:

- current free bytes and applicable quota;
- inode/file-count limits when many shards are possible;
- expected durable output size;
- peak temporary/scratch size;
- checkpoint/cache growth;
- copy/write amplification during compaction, conversion, or atomic replacement;
- safety headroom needed for filesystem and concurrent-job stability.

Use project-configurable minimum-free-space/maximum-footprint policies rather than a universal percentage. Refuse or degrade safely before an expected `ENOSPC` condition. Recheck during long stages when output size is data-dependent.

The stage resource plan should therefore include CPU, RAM, GPU/VRAM, **I/O concurrency, scratch location, storage budget, expected peak on-disk footprint, and recovery/checkpoint policy**.

## Layout and serialization

- Avoid text/JSON/pickle-style whole-object serialization for very large homogeneous numerical arrays when a compact typed representation is materially better.
- Avoid a single monolithic artifact when normal consumers need only small subsets and the format cannot support efficient partial reads.
- Avoid millions of tiny files when a sharded/chunked container or manifest can preserve equivalent isolation with lower metadata cost.
- Choose shard/chunk size from measured access and recovery behavior, not arbitrary round numbers.
- Keep indexes compact and reconstructible; do not duplicate full forward and inverse structures unless the saved compute/recovery time justifies the additional footprint.
- Prefer zero-copy views, memory mapping, or shared read-only buffers when appropriate, but remember that mapped data still consumes page cache/address space and can cause memory pressure.
- Avoid repeated format conversion across stages. Normalize once at the owning boundary and preserve provenance.

## Cache policy and invalidation

Every reusable cache must have an explicit validity identity derived from the inputs and assumptions that affect its contents. Depending on the project this may include:

- input/content digest or immutable source identifier;
- schema/cache format version;
- algorithm/version or feature definition;
- relevant configuration and numerical policy;
- model/checkpoint identity;
- dependency/backend identity when it can change semantics.

A cache hit is valid only after identity and integrity checks pass. File existence alone is not evidence of validity.

Prefer content-addressed or manifest-bound caches for expensive reusable artifacts. Record enough provenance to explain a hit/miss. Define eviction/retention so caches cannot grow without bound. Never silently reuse stale data merely to avoid recomputation.

## Checkpointing, journals, and restart cost

Design recovery around a **recovery-time objective**, not only write frequency.

- Persist checkpoints at a granularity that balances lost recomputation against write overhead.
- For long incremental stages, a compact snapshot plus append-only journal can be effective, but periodically compact the journal so replay time remains bounded.
- Do not require replaying an unbounded event log or rebuilding a massive index before useful work can resume.
- Persist minimal sufficient state; derive secondary structures lazily or in bounded background phases only when their reconstruction cost is acceptable.
- Make stages idempotent or explicitly resumable. A restart must distinguish complete, incomplete, stale, and corrupt state.
- Use completion manifests/markers that are written only after all required artifacts are durable and validated.
- Measure both cold start and warm resume/recovery latency for long workflows.

A fast steady-state kernel with a one-hour restart path is not operationally optimized.

## Crash consistency and integrity

For important artifacts:

- write to a run-owned temporary path, validate, then atomically publish/rename when the filesystem semantics support it;
- do not overwrite the only good checkpoint in place unless the format is explicitly crash-safe;
- use manifest/schema/version checks and checksums/digests when corruption or partial writes would otherwise look valid;
- understand that rename atomicity and durability guarantees can differ across filesystems/mounts;
- coordinate concurrent writers explicitly; avoid multiple workers racing to create or mutate the same cache artifact;
- clean partial temporary state deterministically when ownership is certain, without deleting unrelated user data.


## Schema migration versus cache invalidation

Durable authoritative/output/checkpoint formats and derived caches should not automatically share one migration policy.

- Prefer explicit READ/MIGRATE/REJECT compatibility for authoritative/durable artifacts.
- Prefer invalidation/rebuild for derived caches/indexes when migration would be more complex or risky than recomputation.
- Never destructively migrate authoritative user input as an incidental cache/load operation.
- Treat migration itself as a transaction with temporary output, validation, atomic publication, and recoverability from interruption.
- Include schema/format version and relevant resolved configuration in persisted-state identity.

See `specification-and-implementation.md` for the compatibility matrix.

## Parallel I/O and HPC/shared filesystems

More workers can reduce I/O throughput after the storage layer saturates.

- Treat I/O worker count separately from CPU worker count.
- Avoid every process/rank independently reopening, reparsing, or rewriting the same large input.
- Prefer one read/normalize step followed by shared/read-only reuse when safe.
- Aggregate small writes when durability requirements permit it.
- Avoid thundering-herd checkpointing from many workers at the same instant.
- On network/shared filesystems, benchmark metadata-heavy and random-I/O patterns separately from local scratch.
- Stage to local scratch only when inputs are immutable/copy-verified and outputs are copied back transactionally according to project policy.
- Include copy-back time and failure recovery in end-to-end performance evidence.

## Logging and progress I/O

Observability must not become an I/O bottleneck.

- Do not log once per atom/frame/item in large hot loops by default.
- Rate-limit progress updates and aggregate repeated warnings.
- Keep structured progress in memory/callbacks when possible; persist only the level needed for audit/recovery.
- Bound log retention and rotation for long campaigns.
- Never make correctness depend on log parsing when a structured manifest/state record should own the data.

## Benchmark and evidence requirements

For a storage-relevant optimization, record as applicable:

- cold-cache and warm-cache wall time;
- restart/resume/recovery time;
- bytes read/written and on-disk footprint;
- temporary peak footprint and final retained footprint;
- file/shard count when metadata pressure matters;
- cache build cost, hit validation cost, and hit/miss reason;
- sequential/random access pattern and storage class (local SSD/NVMe, HDD, network/shared filesystem, etc.);
- I/O worker count and concurrent-job conditions;
- CPU overhead of compression/serialization;
- correctness/integrity equivalence.

Do not claim an I/O optimization from a warm page-cache benchmark when real workloads are cold, and do not claim a storage optimization by moving bytes into an unmeasured temporary directory.

## Required failure/recovery tests

When persistence is material, test representative cases such as:

- truncated or partially written artifact;
- checksum/digest/manifest mismatch;
- stale cache identity;
- unsupported schema/version;
- interrupted checkpoint publication;
- restart from the latest valid checkpoint plus journal;
- `ENOSPC`/quota admission or simulated write failure where feasible;
- missing/renamed scratch path;
- concurrent cache creation or writer collision;
- cleanup after failure without deleting authoritative/external inputs;
- deterministic reconstruction and result equivalence after resume.

## Bounded fault injection

For material persistence/recovery claims, prefer deterministic failpoints or controlled simulation at publication/restart boundaries when they can establish crash/recovery behavior without destructive resource exhaustion. Establish that the failpoint fired when practical and keep the production persistence/recovery owner executing; a harness-side reimplementation is not sufficient evidence.

## Hard rules

- Do not use file existence as a completion or cache-validity contract.
- Do not duplicate large datasets/intermediates without a measured reason and explicit lifecycle.
- Do not create unbounded checkpoint, cache, log, or temporary-file growth.
- Do not optimize CPU/GPU throughput by overwhelming the disk or shared filesystem.
- Do not benchmark only the compute kernel when serialization, load, save, or recovery is part of the user-visible workflow.
- Do not delete or compact storage unless ownership and recoverability are known.
- Do not make restart require re-reading/reconstructing substantially more state than the saved work justifies without measuring and documenting that tradeoff.
