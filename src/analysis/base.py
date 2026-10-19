import config


def _parse_csv_line(line: str) -> list[str]:
    """Helper to parse CSV lines without the csv module."""
    return [
        m.group(1) if m.group(1) is not None else m.group(2)
        for m in config.REGEX["csv"].finditer(line)
    ]


class BaseDataLoader:
    """Base class for loading and parsing CSV data."""

    def __init__(self, path: str | None = None, limit: int | None = None) -> None:
        self.path: str = path or config.PATHS[self.__class__.__name__.lower()]
        self.limit: int = limit or config.LIMIT
        self.data: list[dict] = self._read_rows()

    def _read_rows(self) -> list[dict]:
        """Reads rows from the file and delegates parsing to _parse_row."""
        rows: list[dict] = []
        with open(self.path, encoding="utf-8") as f:
            next(f)  # skip header
            for i, line in enumerate(f):
                if i >= self.limit:
                    break
                cols = _parse_csv_line(line.strip())
                parsed = self._parse_row(cols)
                if parsed is not None:
                    rows.append(parsed)
        return rows

    def _parse_row(self, cols: list[str]) -> dict | None:
        """Abstract method to be implemented by subclasses."""
        raise NotImplementedError
