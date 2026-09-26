def rescale(values, low, high):
    if not values:
        raise ValueError("values must be non-empty")
    lo = min(values)
    hi = max(values)
    if lo == hi:
        raise ValueError("values must not be constant")
    scale = (high - low) / (hi - lo)
    return [low + (v - lo) * scale for v in values]
