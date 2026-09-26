import math
import unittest

from quad.trapezoid import integrate


class TrapezoidTests(unittest.TestCase):
    def test_linear_is_exact(self):
        self.assertAlmostEqual(integrate(lambda x: 2 * x + 1, 0.0, 2.0, 7), 6.0, places=12)

    def test_sin_integral(self):
        a, b, n = 0.0, math.pi, 100
        value = integrate(math.sin, a, b, n)
        # Tolerance derived from the accepted D2 error bound in
        # docs/numerical-method.md: |E| <= (b - a) * h**2 * max|f''| / 12,
        # with max|sin''| = 1 on [0, pi], and a safety factor of 2.
        h = (b - a) / n
        error_bound = (b - a) * h**2 * 1.0 / 12
        self.assertLess(abs(value - 2.0), 2 * error_bound)


if __name__ == "__main__":
    unittest.main()
