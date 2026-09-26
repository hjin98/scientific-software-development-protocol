import unittest

from units.length import to_metre


class LengthTests(unittest.TestCase):
    def test_km(self):
        self.assertEqual(to_metre(2.0, "km"), 2000.0)


if __name__ == "__main__":
    unittest.main()
