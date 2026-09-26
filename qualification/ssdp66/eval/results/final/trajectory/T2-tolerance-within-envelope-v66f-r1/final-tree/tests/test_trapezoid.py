import math
import unittest

from quad.trapezoid import integrate


class TrapezoidTests(unittest.TestCase):
    def test_linear_is_exact(self):
        self.assertAlmostEqual(integrate(lambda x: 2 * x + 1, 0.0, 2.0, 7), 6.0, places=12)

    def test_sin_integral(self):
        a, b, n = 0.0, math.pi, 100
        h = (b - a) / n
        max_abs_f_second_derivative = 1.0  # |sin''(x)| = |sin(x)| <= 1 on [0, pi]
        # Error bound and safety factor per docs/numerical-method.md.
        tolerance = 2 * (b - a) * h**2 * max_abs_f_second_derivative / 12

        value = integrate(math.sin, a, b, n)
        self.assertLess(abs(value - 2.0), tolerance)


if __name__ == "__main__":
    unittest.main()
