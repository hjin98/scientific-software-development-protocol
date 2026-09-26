import tempfile
import unittest
from pathlib import Path

from tabular.header import read_header


class HiddenHeaderTests(unittest.TestCase):
    def write(self, text):
        tmp = tempfile.mkdtemp()
        path = Path(tmp, "h.csv")
        path.write_text(text, encoding="utf-8")
        return str(path)

    def test_header(self):
        self.assertEqual(read_header(self.write(" a , b,c \n1,2,3\n")), ["a", "b", "c"])

    def test_empty(self):
        with self.assertRaises(ValueError):
            read_header(self.write(""))

    def test_duplicates(self):
        with self.assertRaises(ValueError):
            read_header(self.write("a,b,a\n"))


if __name__ == "__main__":
    unittest.main()
