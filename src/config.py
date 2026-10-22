import os
import re
from pathlib import Path

# Определяем корень проекта (папка src, где лежит config.py)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

LIMIT = 1000

PATHS = {
    "ratings": str(DATA_DIR / "ratings.csv"),
    "tags": str(DATA_DIR / "tags.csv"),
    "movies": str(DATA_DIR / "movies.csv"),
    "links": str(DATA_DIR / "links.csv"),
}

REGEX = {
    "year": re.compile(r"\((\d{4})\)"),
    "word": re.compile(r"\b\w+\b"),
    "csv": re.compile(r'(?:"([^"]*)"|([^,]+))(?:,|$)'),
}

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def load_env() -> None:
    # Проверяем файлы .env в текущей папке и папкой выше
    possible_paths = [".env", "../.env", "../../.env"]
    env_path = ""

    for path in possible_paths:
        if os.path.exists(path):
            env_path = path
            break

    if env_path:
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    cleaned_line = line.strip()
                    if not cleaned_line or cleaned_line.startswith("#"):
                        continue
                    if "=" in cleaned_line:
                        key, value = cleaned_line.split("=", 1)
                        # Очищаем от возможных пробелов и кавычек
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")
        except (FileNotFoundError, PermissionError):
            pass


load_env()


telegram_token = os.environ.get("TELEGRAM_TOKEN", "")
telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
