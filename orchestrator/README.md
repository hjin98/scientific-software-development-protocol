# sdp-orchestrator-core

The Core / Prompt module of the SDP Orchestrator: it renders one complete,
copy/paste-ready, profile-correct Scientific Software Development Protocol prompt
for a configured target repository.

Core-only installation is a finished operating mode. It needs no database, agent
process, model catalog, quota meter, or scheduler.

The current default profile is Protocol 6.2 (`ssdp-protocol-6.2`, workflow
profile schema v2). Frozen Protocol 6.1 and 6.0 profiles remain packaged under
schema v2, and the frozen Protocol 5.16 profile remains packaged under schema v1;
workplan version binding prevents silent reinterpretation across versions.

See [the Core user guide](docs/core-user-guide.md) for installation,
configuration, Protocol 6 stages, 5.16 compatibility, and the full command
reference.

```bash
pip install sdp-orchestrator-core
sdp doctor
sdp software-implementation --workplan workplans/active/MY-WORKPLAN.md

# Common software-stage alias, valid for Protocol 6 and Protocol 5.16
sdp implementation --workplan workplans/active/MY-WORKPLAN.md

# checkout development, without installing this package
python3 orchestrator/sdp.py --help
```

Both invocation forms delegate to the single `sdp_orchestrator.core.cli:main`
implementation. The versioned consumer and provider contracts are
`sdp_orchestrator.core.api.v1` and `sdp_orchestrator.core.spi.v1`; other Core
modules are implementation detail under that API policy.
