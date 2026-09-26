import tempfile
import unittest
from pathlib import Path

from tabular.rows import count_rows


class RowsTests(unittest.TestCase):
    def test_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "a.csv")
            path.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
            self.assertEqual(count_rows(str(path)), 2)


if __name__ == "__main__":
    unittest.main()
