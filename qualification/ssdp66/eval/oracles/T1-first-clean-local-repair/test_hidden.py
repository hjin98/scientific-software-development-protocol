import unittest

from gridtools.io import cell_widths, parse_grid


class HiddenParseGridTests(unittest.TestCase):
    def test_all_sizes(self):
        for n in range(2, 12):
            edges = [float(i) for i in range(n)]
            cells = parse_grid(" ".join(str(e) for e in edges))
            self.assertEqual(len(cells), n - 1, n)
            self.assertEqual(cells[-1], (float(n - 2), float(n - 1)))

    def test_two_edges(self):
        self.assertEqual(parse_grid("1 2"), [(1.0, 2.0)])

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            parse_grid("")

    def test_widths_unchanged_semantics(self):
        self.assertEqual(cell_widths("0 1 3 6"), [1.0, 2.0, 3.0])


if __name__ == "__main__":
    unittest.main()
