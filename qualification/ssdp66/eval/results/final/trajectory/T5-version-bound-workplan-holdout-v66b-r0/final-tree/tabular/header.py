def read_header(path: str) -> list[str]:
    with open(path, encoding="utf-8") as handle:
        first_line = handle.readline()

    if first_line == "":
        raise ValueError(f"empty file: {path}")

    names = [name.strip() for name in first_line.rstrip("\r\n").split(",")]

    seen = set()
    for name in names:
        if name in seen:
            raise ValueError(f"duplicate column name: {name}")
        seen.add(name)

    return names
