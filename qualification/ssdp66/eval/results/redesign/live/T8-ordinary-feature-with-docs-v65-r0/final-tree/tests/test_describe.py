import unittest

from stats.describe import mean, median


class MeanTests(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3, 6]), 3.0)

    def test_empty(self):
        with self.assertRaises(ValueError):
            mean([])


class MedianTests(unittest.TestCase):
    def test_odd(self):
        self.assertEqual(median([1, 3, 2]), 2)

    def test_even(self):
        self.assertEqual(median([1, 2, 3, 6]), 2.5)

    def test_unsorted(self):
        self.assertEqual(median([5, 1, 4, 2, 3]), 3)

    def test_empty(self):
        with self.assertRaises(ValueError):
            median([])


if __name__ == "__main__":
    unittest.main()
