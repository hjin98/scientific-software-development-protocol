"""SDP Orchestrator Core: configuration, observation, workplan/profile resolution, prompt rendering.

Public surfaces are ``sdp_orchestrator.core.api.v1`` and ``sdp_orchestrator.core.spi.v1``.
Other modules are implementation detail under the API policy; their descriptive
names do not create compatibility paths.
"""

__all__ = ["CORE_DISTRIBUTION", "CORE_API_MAJOR", "CORE_SPI_MAJOR"]

CORE_DISTRIBUTION = "sdp-orchestrator-core"
CORE_API_MAJOR = 1
CORE_SPI_MAJOR = 1
