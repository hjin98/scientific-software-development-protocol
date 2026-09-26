def read_header(path: str) -> list[str]:
    with open(path, encoding="utf-8") as handle:
        line = handle.readline()

    if not line:
        raise ValueError(f"empty file: {path}")

    names = [name.strip() for name in line.rstrip("\n").split(",")]

    seen = set()
    for name in names:
        if name in seen:
            raise ValueError(f"duplicate column name: {name}")
        seen.add(name)

    return names
