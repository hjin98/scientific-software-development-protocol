def rescale(values, low, high):
    if not values:
        raise ValueError("values must not be empty")
    minimum = min(values)
    maximum = max(values)
    if minimum == maximum:
        raise ValueError("values must not be constant")
    scale = (high - low) / (maximum - minimum)
    return [low + (v - minimum) * scale for v in values]
