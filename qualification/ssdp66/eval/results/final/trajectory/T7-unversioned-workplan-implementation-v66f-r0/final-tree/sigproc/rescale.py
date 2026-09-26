def rescale(values, low, high):
    if not values:
        raise ValueError("values must not be empty")
    minimum = min(values)
    maximum = max(values)
    if minimum == maximum:
        raise ValueError("values must not be constant")
    scale = (high - low) / (maximum - minimum)
    return [low + (value - minimum) * scale for value in values]
