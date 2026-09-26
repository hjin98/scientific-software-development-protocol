import unittest

from sigproc.rescale import rescale


class RescaleTests(unittest.TestCase):
    def test_normal_range(self):
        self.assertEqual(rescale([1, 2, 3], 0, 10), [0.0, 5.0, 10.0])

    def test_negative_range(self):
        self.assertEqual(rescale([-10, 0, 10], -1, 1), [-1.0, 0.0, 1.0])

    def test_constant_input_raises(self):
        with self.assertRaises(ValueError):
            rescale([5, 5, 5], 0, 1)

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            rescale([], 0, 1)

    def test_input_list_unchanged(self):
        values = [1, 2, 3]
        rescale(values, 0, 10)
        self.assertEqual(values, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
