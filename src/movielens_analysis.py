import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import UTC, datetime

from bs4 import BeautifulSoup

import config


def _parse_csv_line(line: str) -> list[str]:
    """Helper to parse CSV lines without the csv module."""
    return [
        m.group(1) if m.group(1) is not None else m.group(2)
        for m in config.REGEX["csv"].finditer(line)
    ]


class Ratings:
    def __init__(self, path: str | None = None, limit: int | None = None) -> None:
        self.path: str = path or config.PATHS["ratings"]
        self.limit: int = limit or config.LIMIT
        self.data: list[dict] = self._read_rows()

    def _read_rows(self) -> list[dict]:
        rows: list[dict] = []
        with open(self.path, encoding="utf-8") as f:
            next(f)
            for i, line in enumerate(f):
                if i >= self.limit:
                    break
                cols = _parse_csv_line(line.strip())
                if len(cols) == 4:
                    rows.append(
                        {
                            "userId": int(cols[0]),
                            "movieId": int(cols[1]),
                            "rating": float(cols[2]),
                            "timestamp": int(cols[3]),
                        }
                    )
        return rows

    def get_movies_by_rating(self) -> dict[int, list[float]]:
        result: dict[int, list[float]] = defaultdict(list)
        for row in self.data:
            result[row["movieId"]].append(row["rating"])
        return dict(result)

    def get_top_N_movies(self, N: int) -> list[tuple[int, float]]:
        movies_by_rating = self.get_movies_by_rating()
        averages: list[tuple[int, float]] = [
            (movie_id, round(sum(ratings) / len(ratings), 2))
            for movie_id, ratings in movies_by_rating.items()
        ]
        averages.sort(key=lambda x: (-x[1], x[0]))
        return averages[:N]

    def get_movies_by_year(self, year: int) -> list[tuple[int, float]]:
        movie_ratings: dict[int, list[float]] = defaultdict(list)
        for row in self.data:
            rating_year = datetime.fromtimestamp(row["timestamp"], tz=UTC).year
            if rating_year == year:
                movie_ratings[row["movieId"]].append(row["rating"])

        result: list[tuple[int, float]] = [
            (m_id, round(sum(ratings) / len(ratings), 2))
            for m_id, ratings in movie_ratings.items()
        ]
        result.sort(key=lambda x: (-x[1], x[0]))
        return result

    def get_average_rating_by_year(self) -> list[tuple[int, float]]:
        year_ratings: dict[int, list[float]] = defaultdict(list)
        for row in self.data:
            year = datetime.fromtimestamp(row["timestamp"], tz=UTC).year
            year_ratings[year].append(row["rating"])

        return [
            (year, round(sum(ratings) / len(ratings), 2))
            for year, ratings in sorted(year_ratings.items())
        ]


class Tags:
    def __init__(self, path: str | None = None, limit: int | None = None) -> None:
        self.path: str = path or config.PATHS["tags"]
        self.limit: int = limit or config.LIMIT
        self.data: list[dict] = self._read_rows()

    def _read_rows(self) -> list[dict]:
        rows: list[dict] = []
        with open(self.path, encoding="utf-8") as f:
            next(f)
            for i, line in enumerate(f):
                if i >= self.limit:
                    break
                cols = _parse_csv_line(line.strip())
                if len(cols) == 4:
                    rows.append(
                        {
                            "userId": int(cols[0]),
                            "movieId": int(cols[1]),
                            "tag": cols[2],
                            "timestamp": int(cols[3]),
                        }
                    )
        return rows

    def get_most_words_tags(self, N: int) -> list[tuple[str, int]]:
        tag_word_counts: dict[str, int] = {
            row["tag"]: len(config.REGEX["word"].findall(row["tag"]))
            for row in self.data
        }
        return sorted(tag_word_counts.items(), key=lambda x: (-x[1], x[0]))[:N]

    def get_longest_tag(self) -> str:
        if not self.data:
            return ""
        return max((row["tag"] for row in self.data), key=len)

    def get_tags_with_specific_word(self, word: str) -> list[str]:
        word = word.lower()
        return list({row["tag"] for row in self.data if word in row["tag"].lower()})


class Movies:
    def __init__(self, path: str | None = None, limit: int | None = None) -> None:
        self.path: str = path or config.PATHS["movies"]
        self.limit: int = limit or config.LIMIT
        self.data: list[dict] = self._read_rows()

    def _read_rows(self) -> list[dict]:
        rows: list[dict] = []
        with open(self.path, encoding="utf-8") as f:
            next(f)
            for i, line in enumerate(f):
                if i >= self.limit:
                    break
                cols = _parse_csv_line(line.strip())
                if len(cols) == 3:
                    title = cols[1]
                    year_match = config.REGEX["year"].search(title)
                    year = int(year_match.group(1)) if year_match else None

                    genres = (
                        cols[2].split("|") if cols[2] != "(no genres listed)" else []
                    )

                    rows.append(
                        {
                            "movieId": int(cols[0]),
                            "title": title,
                            "genres": genres,
                            "year": year,
                        }
                    )
        return rows

    def dist_by_release(self) -> dict[int, int]:
        year_counts: Counter = Counter(
            row["year"] for row in self.data if row["year"] is not None
        )
        return dict(sorted(year_counts.items()))

    def dist_by_genres(self) -> dict[str, int]:
        genre_counts: Counter = Counter(
            genre for row in self.data for genre in row["genres"]
        )
        return dict(genre_counts.most_common())

    def top_N_movies_by_rating(
        self, N: int, ratings: Ratings
    ) -> list[tuple[str, float]]:
        movies_by_rating = ratings.get_movies_by_rating()
        averages: list[tuple[int, float]] = sorted(
            ((m_id, round(sum(r) / len(r), 2)) for m_id, r in movies_by_rating.items()),
            key=lambda x: (-x[1], x[0]),
        )[:N]

        id_to_title: dict[int, str] = {
            row["movieId"]: row["title"] for row in self.data
        }
        return [
            (id_to_title.get(m_id, f"Unknown (ID: {m_id})"), avg)
            for m_id, avg in averages
        ]

    def get_movies_by_title(self, substring: str) -> list[str]:
        substring = substring.lower()
        return [row["title"] for row in self.data if substring in row["title"].lower()]


class Links:
    def __init__(self, path: str | None = None, limit: int | None = None) -> None:
        self.path: str = path or config.PATHS["links"]
        self.limit: int = limit or config.LIMIT
        self.data: list[dict] = self._read_rows()

    def _read_rows(self) -> list[dict]:
        rows: list[dict] = []
        with open(self.path, encoding="utf-8") as f:
            next(f)
            for i, line in enumerate(f):
                if i >= self.limit:
                    break
                cols = _parse_csv_line(line.strip())
                if len(cols) >= 2:
                    rows.append(
                        {
                            "movieId": int(cols[0]),
                            "imdbId": str(cols[1]).zfill(7),
                            "tmdbId": cols[2] if len(cols) > 2 and cols[2] else None,
                        }
                    )
        return rows

    def get_movie_id_by_imdb(self, imdb_id: str) -> int | None:
        imdb_id = str(imdb_id).zfill(7)
        return next(
            (row["movieId"] for row in self.data if row["imdbId"] == imdb_id), None
        )

    def get_imdb_id_by_movie(self, movie_id: int) -> str | None:
        return next(
            (row["imdbId"] for row in self.data if row["movieId"] == movie_id), None
        )

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

        # 1. Сетевые ошибки и ошибки HTTP (404, 403, таймауты)
        except urllib.error.HTTPError as e:
            return {"title": None, "url": url, "status": f"http_error: {e.code}"}
        except urllib.error.URLError as e:
            return {"title": None, "url": url, "status": f"url_error: {e.reason}"}

        # 2. Ошибки парсинга (если IMDb вернул капчу вместо HTML)
        except AttributeError as e:
            return {"title": None, "url": url, "status": f"parse_error: {e!s}"}

        # 3. Ошибки кодировки (если пришел не UTF-8)
        except UnicodeDecodeError as e:
            return {"title": None, "url": url, "status": f"encoding_error: {e!s}"}


class Tests:
    pass
