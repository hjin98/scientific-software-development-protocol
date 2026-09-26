def clip_values(values, low, high):
    if low > high:
        raise ValueError("low must not exceed high")
    return [min(max(v, low), high) for v in values]
