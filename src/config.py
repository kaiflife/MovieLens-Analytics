import os
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
