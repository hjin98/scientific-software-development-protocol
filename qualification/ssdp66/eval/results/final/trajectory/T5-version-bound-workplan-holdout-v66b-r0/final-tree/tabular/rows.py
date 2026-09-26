def count_rows(path: str) -> int:
    with open(path, encoding="utf-8") as handle:
        return max(sum(1 for _ in handle) - 1, 0)
