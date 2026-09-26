import unittest

from units.pressure import to_pascal


class HiddenPressureTests(unittest.TestCase):
    def test_units(self):
        self.assertEqual(to_pascal(1.0, "Pa"), 1.0)
        self.assertEqual(to_pascal(2.0, "kPa"), 2000.0)
        self.assertEqual(to_pascal(1.0, "bar"), 100000.0)
        self.assertEqual(to_pascal(1.0, "atm"), 101325.0)

    def test_unknown(self):
        with self.assertRaises(ValueError):
            to_pascal(1.0, "psi")


if __name__ == "__main__":
    unittest.main()
