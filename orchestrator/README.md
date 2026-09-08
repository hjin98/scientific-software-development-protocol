# sdp-orchestrator-core

The Core / Prompt module of the SDP Orchestrator: it renders one complete,
copy/paste-ready, stage-correct Software Development Protocol prompt for a
configured target repository.

Core-only installation is a finished operating mode. It needs no database, agent
process, model catalog, quota meter, or scheduler.

See [the Core user guide](docs/core-user-guide.md) for installation,
configuration, and the full command reference.

```bash
pip install sdp-orchestrator-core
sdp doctor
sdp implementation

# checkout development, without installing this package
python3 orchestrator/sdp.py --help
```

Both invocation forms delegate to the single `sdp_orchestrator.core.cli:main`
implementation. The versioned consumer and provider contracts are
`sdp_orchestrator.core.api.v1` and `sdp_orchestrator.core.spi.v1`; other Core
modules are implementation detail under that API policy.
