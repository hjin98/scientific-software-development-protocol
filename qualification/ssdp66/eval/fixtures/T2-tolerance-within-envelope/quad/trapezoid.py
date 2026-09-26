"""Composite trapezoidal quadrature (see docs/numerical-method.md)."""
from collections.abc import Callable


def integrate(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    if n < 1:
        raise ValueError("n must be positive")
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return total * h
