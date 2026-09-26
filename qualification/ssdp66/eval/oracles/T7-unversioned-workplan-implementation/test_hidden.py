import unittest

from sigproc.rescale import rescale


class HiddenRescaleTests(unittest.TestCase):
    def test_rescale(self):
        self.assertEqual(rescale([2, 4, 6], 0, 1), [0.0, 0.5, 1.0])

    def test_negative_range(self):
        self.assertEqual(rescale([0, 10], -1, 1), [-1.0, 1.0])

    def test_constant_and_empty(self):
        for values in ([3, 3], []):
            with self.assertRaises(ValueError):
                rescale(values, 0, 1)

    def test_input_unchanged(self):
        values = [5, 1]
        rescale(values, 0, 1)
        self.assertEqual(values, [5, 1])


if __name__ == "__main__":
    unittest.main()
