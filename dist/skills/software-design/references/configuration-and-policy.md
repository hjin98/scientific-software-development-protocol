# Configuration and Policy Resolution

Configuration is part of the executable contract. A scientifically or operationally meaningful run must be explainable from one resolved configuration, not from scattered defaults, hidden environment variables, and late policy decisions.

## Canonical resolution

For any nontrivial configurable workflow, define one canonical resolution path. If the repository does not already define precedence, a conservative default is:

1. built-in/project defaults;
2. explicit configuration file or profile;
3. explicitly supported environment-variable overrides;
4. explicit CLI/API/user overrides.

Do not let arbitrary environment variables silently change scientific semantics. Environment-based configuration should use a documented allowlist and should normally be reserved for deployment/resource concerns or intentional overrides.

Normalize aliases and deprecated names before validation so downstream code consumes one canonical representation.

## Resolved configuration object

After resolution, produce one validated representation containing as applicable:

- configuration schema/policy version;
- effective values after defaults and overrides;
- source/provenance of material values (`default`, config file, environment, CLI/API, automatic policy);
- normalized units/types/enums;
- derived values such as worker counts, batch sizes, selected backend, precision, thresholds, storage paths, and resource budgets;
- rationale for automatic selections when users may need to understand or reproduce them.

Validate semantic constraints on the resolved configuration, not only on individual parser inputs. Reject incompatible combinations before expensive work begins.

For long or scientifically important workflows, persist a redacted canonical snapshot with the run/evidence record so the exact executed policy can be reconstructed.

The resolved values, origins and automatic-policy rationale here are the source that scientific decision provenance reuses; [Scientific inspectability and epistemic initiative](scientific-inspectability-and-initiative.md) owns their scientific presentation, including actor and binding status, without adding a configuration registry.

## Dynamic defaults and automatic policy

Values derived from runtime state are still configuration once resolved. Examples include:

- effective CPU allocation;
- available RAM/VRAM/disk space;
- worker count selected from measured saturation;
- batch size after resource admission;
- backend selected by `auto` policy;
- cache/storage strategy selected from estimated footprint.

Capture the chosen value and selection reason at run start or at the point the policy becomes stable. Do not make later reproduction depend on recomputing a historical dynamic default from a different machine state.

Automatic policy should have an explicit override/fallback and should not silently change scientific semantics.

## Configuration identity and persisted state

Any configuration field that materially changes the meaning of a cache, checkpoint, index, compiled artifact, or model evaluation must participate in its semantic identity or compatibility check.

A useful abstraction is:

```text
state_identity = H(
    input identity,
    schema/algorithm versions,
    semantically relevant resolved configuration,
    model/backend/precision identity where material,
)
```

Do not hash every incidental presentation option into numerical caches. Identity should be complete enough to prevent unsafe reuse but scoped enough to avoid invalidation from irrelevant changes.

Store canonical serialized values before hashing. Avoid hashes of unordered or implementation-dependent object representations.

## Secrets and sensitive configuration

Credentials, tokens, private keys, and other secrets are configuration inputs but must not be persisted in ordinary resolved-configuration snapshots, logs, manifests, exception messages, cache identities, or documentation.

Instead:

- record only that a credential source/capability was configured when evidence requires it;
- redact secret values before serialization/logging;
- keep secret resolution at the narrowest layer that needs it;
- do not make a cache/checkpoint identity depend directly on raw secret bytes unless a specialized design explicitly requires and protects that behavior.

Read `security-and-trust-boundaries.md` for credential and external-service boundaries.

## API/CLI/config parity

When multiple front ends expose the same policy:

- route them through the same normalization/validation layer;
- keep defaults and enum choices synchronized;
- test equivalent CLI/API/config-file forms where compatibility matters;
- document one authoritative semantic definition rather than repeating divergent descriptions in each front end.

## Versioning and deprecation

Version a configuration schema when persisted configuration must survive software changes or be consumed independently.

For deprecations:

1. accept the legacy form for the supported transition period;
2. normalize it centrally;
3. emit one actionable warning at the appropriate user-facing boundary;
4. persist the normalized canonical form rather than propagating legacy aliases;
5. document the removal/version boundary.

Do not silently reinterpret an old key to mean something materially different.

## Verification

Add tests proportional to configuration risk:

- precedence and override behavior;
- omitted/default values;
- alias/deprecation normalization;
- incompatible combinations;
- dynamic resource-derived resolution;
- automatic-policy selection and explicit override;
- canonical serialization/digest stability;
- cache/checkpoint invalidation when a semantic field changes;
- no invalidation when an irrelevant presentation field changes;
- secret redaction from logs/manifests/errors;
- equivalent CLI/API/config-file behavior.

## Hard rules

- Do not let configuration semantics be distributed across unrelated callers without one canonical resolution layer.
- Do not allow hidden environment state to silently change scientific results.
- Do not persist only the user's partial input configuration when defaults/automatic policy materially determine the executed run.
- Do not reuse persisted state without checking the resolved semantic configuration that affects it.
- Do not log or serialize secrets as part of reproducibility evidence.
