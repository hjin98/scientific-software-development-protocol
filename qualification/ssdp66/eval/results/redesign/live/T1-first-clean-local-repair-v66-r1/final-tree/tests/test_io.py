import unittest

from gridtools.io import cell_widths, parse_grid


class ParseGridTests(unittest.TestCase):
    def test_three_edges_make_two_cells(self):
        self.assertEqual(parse_grid("0 1 3"), [(0.0, 1.0), (1.0, 3.0)])

    def test_widths(self):
        self.assertEqual(cell_widths("0 0.5 2 2.5"), [0.5, 1.5, 0.5])

    def test_rejects_single_edge(self):
        with self.assertRaises(ValueError):
            parse_grid("4")


if __name__ == "__main__":
    unittest.main()
