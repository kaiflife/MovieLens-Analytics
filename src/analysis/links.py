import urllib.error
import urllib.request

from bs4 import BeautifulSoup

import config
from logger import log_method
from .base import BaseDataLoader


class Links(BaseDataLoader):
    def _parse_row(self, cols: list[str]) -> dict | None:
        if len(cols) >= 2:
            return {
                "movieId": int(cols[0]),
                "imdbId": str(cols[1]).zfill(7),
                "tmdbId": cols[2] if len(cols) > 2 and cols[2] else None,
            }
        return None

    @log_method
    def get_movie_id_by_imdb(self, imdb_id: str) -> int | None:
        imdb_id = str(imdb_id).zfill(7)
        return next(
            (row["movieId"] for row in self.data if row["imdbId"] == imdb_id), None
        )

    @log_method
    def get_imdb_id_by_movie(self, movie_id: int) -> str | None:
        return next(
            (row["imdbId"] for row in self.data if row["movieId"] == movie_id), None
        )

    @log_method
    def get_movie_info_by_imdb(self, imdb_id: str) -> dict:
        imdb_id = str(imdb_id).zfill(7)
        url = f"https://www.imdb.com/title/tt{imdb_id}/"
        req = urllib.request.Request(url, headers={"User-Agent": config.USER_AGENT})

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                soup = BeautifulSoup(response.read().decode("utf-8"), "html.parser")
                title_tag = soup.find("h1")
                title = title_tag.text.strip() if title_tag else "Unknown"
                return {"title": title, "url": url, "status": "success"}

        except urllib.error.HTTPError as e:
            return {"title": None, "url": url, "status": f"http_error: {e.code}"}
        except urllib.error.URLError as e:
            return {"title": None, "url": url, "status": f"url_error: {e.reason}"}
        except AttributeError as e:
            return {"title": None, "url": url, "status": f"parse_error: {e!s}"}
        except UnicodeDecodeError as e:
            return {"title": None, "url": url, "status": f"encoding_error: {e!s}"}
