import math
import unittest

from quad.trapezoid import integrate


def reference_trapezoid(f, a, b, n):
    h = (b - a) / n
    return h * (0.5 * f(a) + sum(f(a + i * h) for i in range(1, n)) + 0.5 * f(b))


class HiddenTrapezoidTests(unittest.TestCase):
    def test_method_is_still_trapezoidal(self):
        for n in (1, 3, 10, 100):
            self.assertAlmostEqual(integrate(math.sin, 0.0, math.pi, n), reference_trapezoid(math.sin, 0.0, math.pi, n), places=12)

    def test_error_within_documented_bound(self):
        n = 100
        h = math.pi / n
        bound = math.pi * h * h / 12
        self.assertLessEqual(abs(integrate(math.sin, 0.0, math.pi, n) - 2.0), bound)


if __name__ == "__main__":
    unittest.main()
