import math
import unittest

from quad.trapezoid import integrate


class TrapezoidTests(unittest.TestCase):
    def test_linear_is_exact(self):
        self.assertAlmostEqual(integrate(lambda x: 2 * x + 1, 0.0, 2.0, 7), 6.0, places=12)

    def test_sin_integral(self):
        a, b, n = 0.0, math.pi, 100
        # Error bound from docs/numerical-method.md (accepted D2 authority):
        # |E| <= (b - a) * h**2 * max|f''| / 12, with a safety factor of 2.
        # max|sin''| = max|sin| = 1 on [0, pi].
        h = (b - a) / n
        tolerance = 2 * (b - a) * h**2 * 1 / 12
        value = integrate(math.sin, a, b, n)
        self.assertLess(abs(value - 2.0), tolerance)


if __name__ == "__main__":
    unittest.main()
