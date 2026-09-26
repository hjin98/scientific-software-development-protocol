import tempfile
import unittest
from pathlib import Path

from tabular.header import read_header


class HeaderTests(unittest.TestCase):
    def test_normal_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "a.csv")
            path.write_text("a,b,c\n1,2,3\n", encoding="utf-8")
            self.assertEqual(read_header(str(path)), ["a", "b", "c"])

    def test_whitespace_stripped(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "a.csv")
            path.write_text(" a , b ,c\n1,2,3\n", encoding="utf-8")
            self.assertEqual(read_header(str(path)), ["a", "b", "c"])

    def test_empty_file_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "a.csv")
            path.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_header(str(path))

    def test_duplicate_columns_raise(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "a.csv")
            path.write_text("a,b,a\n1,2,3\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_header(str(path))


if __name__ == "__main__":
    unittest.main()
