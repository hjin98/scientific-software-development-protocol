"""Smoothing-length helpers for the cubic-spline SPH kernel."""


def smoothing_length(dx: float, eta: float = 1.2) -> float:
    """Return the smoothing length for particle spacing ``dx`` (docs/numerical-method.md)."""
    if dx <= 0:
        raise ValueError("dx must be positive")
    return eta * dx


def neighbour_radius(dx: float, eta: float = 1.2) -> float:
    return 2.0 * smoothing_length(dx, eta)
