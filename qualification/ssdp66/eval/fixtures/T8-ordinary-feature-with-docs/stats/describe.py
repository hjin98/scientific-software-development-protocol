"""Descriptive statistics for small in-memory samples."""


def mean(values):
    """Arithmetic mean of ``values``; raises ``ValueError`` for an empty sample."""
    if not values:
        raise ValueError("mean of an empty sample")
    return sum(values) / len(values)
