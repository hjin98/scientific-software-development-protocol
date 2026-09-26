import unittest

from sigproc.smoothing import moving_average


class SmoothingTests(unittest.TestCase):
    def test_window_two(self):
        self.assertEqual(moving_average([1, 3, 5], 2), [2.0, 4.0])


if __name__ == "__main__":
    unittest.main()
