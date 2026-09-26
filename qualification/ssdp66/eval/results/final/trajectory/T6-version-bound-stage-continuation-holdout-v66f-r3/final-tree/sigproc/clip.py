def clip_values(values, low, high):
    if low > high:
        raise ValueError("low must not exceed high")
    return [min(max(value, low), high) for value in values]
