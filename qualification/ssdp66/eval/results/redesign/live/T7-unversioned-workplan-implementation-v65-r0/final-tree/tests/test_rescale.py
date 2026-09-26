import unittest

from sigproc.rescale import rescale


class RescaleTests(unittest.TestCase):
    def test_normal_range(self):
        self.assertEqual(rescale([0, 5, 10], 0, 1), [0.0, 0.5, 1.0])

    def test_negative_range(self):
        self.assertEqual(rescale([0, 5, 10], -1, 1), [-1.0, 0.0, 1.0])

    def test_constant_input_raises(self):
        with self.assertRaises(ValueError):
            rescale([3, 3, 3], 0, 1)

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            rescale([], 0, 1)

    def test_input_list_unchanged(self):
        values = [0, 5, 10]
        rescale(values, 0, 1)
        self.assertEqual(values, [0, 5, 10])


if __name__ == "__main__":
    unittest.main()
