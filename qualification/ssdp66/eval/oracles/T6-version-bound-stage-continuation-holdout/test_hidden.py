import unittest

from sigproc.clip import clip_values


class HiddenClipTests(unittest.TestCase):
    def test_clip(self):
        self.assertEqual(clip_values([-5, 0, 3, 9], 0, 4), [0, 0, 3, 4])

    def test_bounds_error(self):
        with self.assertRaises(ValueError):
            clip_values([1], 2, 1)

    def test_input_unchanged(self):
        values = [-1, 7]
        clip_values(values, 0, 5)
        self.assertEqual(values, [-1, 7])


if __name__ == "__main__":
    unittest.main()
