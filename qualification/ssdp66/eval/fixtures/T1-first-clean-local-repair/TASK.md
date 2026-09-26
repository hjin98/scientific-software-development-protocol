`parse_grid()` in `gridtools/io.py` drops the last cell when the number of values is odd. Fix it. `python -m unittest discover -s tests` shows the failure.
