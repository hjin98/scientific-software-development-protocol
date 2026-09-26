import unittest

from sigproc.clip import clip_values


class ClipTests(unittest.TestCase):
    def test_values_below_inside_and_above_interval(self):
        self.assertEqual(clip_values([-5, 0, 3, 10, 20], 0, 10), [0, 0, 3, 10, 10])

    def test_low_greater_than_high_raises(self):
        with self.assertRaises(ValueError):
            clip_values([1, 2, 3], 5, 1)

    def test_input_list_not_modified(self):
        values = [-5, 0, 3, 10, 20]
        original = list(values)
        clip_values(values, 0, 10)
        self.assertEqual(values, original)


if __name__ == "__main__":
    unittest.main()
