import unittest

from sph.kernel import neighbour_radius, smoothing_length


class KernelTests(unittest.TestCase):
    def test_default_eta(self):
        self.assertAlmostEqual(smoothing_length(0.5), 0.6)

    def test_radius(self):
        self.assertAlmostEqual(neighbour_radius(1.0), 2.4)


if __name__ == "__main__":
    unittest.main()
