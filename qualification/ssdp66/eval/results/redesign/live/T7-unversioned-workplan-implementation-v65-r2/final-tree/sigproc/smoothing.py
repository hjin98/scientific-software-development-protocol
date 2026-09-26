def moving_average(values, window):
    if window < 1:
        raise ValueError("window must be positive")
    if window > len(values):
        return []
    return [sum(values[i:i + window]) / window for i in range(len(values) - window + 1)]
