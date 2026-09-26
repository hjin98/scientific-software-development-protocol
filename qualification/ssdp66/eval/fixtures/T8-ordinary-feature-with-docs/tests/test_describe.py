import unittest

from stats.describe import mean


class MeanTests(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3, 6]), 3.0)

    def test_empty(self):
        with self.assertRaises(ValueError):
            mean([])


if __name__ == "__main__":
    unittest.main()
