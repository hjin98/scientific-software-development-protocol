def rescale(values, low, high):
    if not values:
        raise ValueError("values must not be empty")
    minimum = min(values)
    maximum = max(values)
    if minimum == maximum:
        raise ValueError("values must not be constant")
    span = maximum - minimum
    target_span = high - low
    return [low + (value - minimum) * target_span / span for value in values]
