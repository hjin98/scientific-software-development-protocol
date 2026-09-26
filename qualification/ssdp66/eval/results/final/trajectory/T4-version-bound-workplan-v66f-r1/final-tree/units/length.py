_FACTORS = {"m": 1.0, "km": 1000.0, "cm": 0.01}


def to_metre(value: float, unit: str) -> float:
    try:
        return value * _FACTORS[unit]
    except KeyError:
        raise ValueError(f"unknown length unit: {unit}") from None
