from collections import Counter

import config
from logger import log_method
from .base import BaseDataLoader
from .ratings import Ratings


class Movies(BaseDataLoader):
    def _parse_row(self, cols: list[str]) -> dict | None:
        if len(cols) == 3:
            title = cols[1]
            year_match = config.REGEX["year"].search(title)
            year = int(year_match.group(1)) if year_match else None
            genres = cols[2].split("|") if cols[2] != "(no genres listed)" else []
            return {
                "movieId": int(cols[0]),
                "title": title,
                "genres": genres,
                "year": year,
            }
        return None

    @log_method
    def dist_by_release(self) -> dict[int, int]:
        year_counts: Counter = Counter(
            row["year"] for row in self.data if row["year"] is not None
        )
        return dict(sorted(year_counts.items()))

    @log_method
    def dist_by_genres(self) -> dict[str, int]:
        genre_counts: Counter = Counter(
            genre for row in self.data for genre in row["genres"]
        )
        return dict(genre_counts.most_common())

    @log_method
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

    @log_method
    def get_movies_by_title(self, substring: str) -> list[str]:
        substring = substring.lower()
        return [row["title"] for row in self.data if substring in row["title"].lower()]
