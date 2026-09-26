"""Descriptive statistics for small in-memory samples."""


def mean(values):
    """Arithmetic mean of ``values``; raises ``ValueError`` for an empty sample."""
    if not values:
        raise ValueError("mean of an empty sample")
    return sum(values) / len(values)


def median(values):
    """Median of ``values``; raises ``ValueError`` for an empty sample."""
    if not values:
        raise ValueError("median of an empty sample")
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2
