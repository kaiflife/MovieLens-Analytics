import re

# --- CONFIGURATION ---
LIMIT = 1000

PATHS = {
    "ratings": "data/ratings.csv",
    "tags": "data/tags.csv",
    "movies": "data/movies.csv",
    "links": "data/links.csv",
}

REGEX = {
    "year": re.compile(r"\((\d{4})\)"),
    "word": re.compile(r"\b\w+\b"),
    "csv": re.compile(r'(?:"([^"]*)"|([^,]+))(?:,|$)'),
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
