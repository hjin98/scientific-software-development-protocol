import math
import unittest

from quad.trapezoid import integrate


class TrapezoidTests(unittest.TestCase):
    def test_linear_is_exact(self):
        self.assertAlmostEqual(integrate(lambda x: 2 * x + 1, 0.0, 2.0, 7), 6.0, places=12)

    def test_sin_integral(self):
        value = integrate(math.sin, 0.0, math.pi, 100)
        self.assertLess(abs(value - 2.0), 1e-12)


if __name__ == "__main__":
    unittest.main()
