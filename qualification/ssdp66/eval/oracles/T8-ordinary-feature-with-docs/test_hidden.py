import unittest

from stats.describe import median


class HiddenMedianTests(unittest.TestCase):
    def test_odd(self):
        self.assertEqual(median([3, 1, 2]), 2)

    def test_even(self):
        self.assertEqual(median([4, 1, 3, 2]), 2.5)

    def test_empty(self):
        with self.assertRaises(ValueError):
            median([])

    def test_input_unchanged(self):
        values = [3, 1, 2]
        median(values)
        self.assertEqual(values, [3, 1, 2])


if __name__ == "__main__":
    unittest.main()
