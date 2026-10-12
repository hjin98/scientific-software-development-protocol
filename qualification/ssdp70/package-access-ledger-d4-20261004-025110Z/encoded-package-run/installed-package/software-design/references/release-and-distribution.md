# Release and Distribution

Use release checks when a change affects a package, build system, entry point, generated distributable, installer, or release process.

## Build what users receive

Source-tree correctness does not prove shipped-artifact correctness. For a materially affected distributable:

- build the supported artifact from canonical source;
- validate its required structure/metadata independently of the builder that produced it;
- inspect expected modules/resources/entry points;
- exclude secrets, caches, local paths, accidental datasets, and developer scratch;
- install or ingest it through the closest supported consumer path when practical;
- exercise the user-facing import/entry point or equivalent packaged interface outside the source checkout when applicable;
- verify version/protocol metadata when identity is part of the deliverable.

These are functional integration/release checks. They augment affected-surface regression and do not create a separate qualification lifecycle.

If the actual consumer environment is unavailable, validate the package structure and closest available ingestion/interface path, then report the unavailable consumer check rather than claiming it passed.

## Scope proportionally

Test supported platform/backend combinations according to the actual release scope. Do not infer unavailable results. If a packaging change can affect multiple shipped skills/artifacts, validate every affected artifact rather than one representative package.

Use exact artifact hashes only when exact built bytes matter. Otherwise source commit plus material build conditions is usually sufficient.

## Generated outputs

Prefer reproducible generation over version-controlling generated artifacts. Track generated output only when repository/release policy makes it an authoritative shipped artifact.

When generated artifacts are tracked, distinguish two checks:

1. **artifact validity** — the generated package itself satisfies its structural/consumer contract;
2. **source-to-generated parity** — committed generated output corresponds to canonical source.

One does not substitute for the other. A builder can consistently generate an invalid artifact, and a valid artifact can still be stale relative to source.

## Completion

Record enough to reproduce or diagnose a material release issue, including the affected artifacts and consumer/interface checks actually run, but do not require hash chains, report manifests, or extra evidence documents merely for completeness.
