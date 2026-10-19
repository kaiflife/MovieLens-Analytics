import re

LIMIT = 1000

DATA_DIR = "data"

PATHS = {
    "ratings": f"{DATA_DIR}/ratings.csv",
    "tags": f"{DATA_DIR}/tags.csv",
    "movies": f"{DATA_DIR}/movies.csv",
    "links": f"{DATA_DIR}/links.csv",
}

REGEX = {
    "year": re.compile(r"\((\d{4})\)"),
    "word": re.compile(r"\b\w+\b"),
    "csv": re.compile(r'(?:"([^"]*)"|([^,]+))(?:,|$)'),
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
