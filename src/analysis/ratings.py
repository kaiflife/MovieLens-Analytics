from collections import defaultdict
from datetime import UTC, datetime

from logger import log_method
from .base import BaseDataLoader


class Ratings(BaseDataLoader):
    def _parse_row(self, cols: list[str]) -> dict | None:
        if len(cols) == 4:
            return {
                "userId": int(cols[0]),
                "movieId": int(cols[1]),
                "rating": float(cols[2]),
                "timestamp": int(cols[3]),
            }
        return None

    @log_method
    def get_movies_by_rating(self) -> dict[int, list[float]]:
        result: dict[int, list[float]] = defaultdict(list)
        for row in self.data:
            result[row["movieId"]].append(row["rating"])
        return dict(result)

    @log_method
    def get_top_N_movies(self, N: int) -> list[tuple[int, float]]:
        movies_by_rating = self.get_movies_by_rating()
        averages: list[tuple[int, float]] = [
            (movie_id, round(sum(ratings) / len(ratings), 2))
            for movie_id, ratings in movies_by_rating.items()
        ]
        averages.sort(key=lambda x: (-x[1], x[0]))
        return averages[:N]

    @log_method
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

    @log_method
    def get_average_rating_by_year(self) -> list[tuple[int, float]]:
        year_ratings: dict[int, list[float]] = defaultdict(list)
        for row in self.data:
            year = datetime.fromtimestamp(row["timestamp"], tz=UTC).year
            year_ratings[year].append(row["rating"])

        return [
            (year, round(sum(ratings) / len(ratings), 2))
            for year, ratings in sorted(year_ratings.items())
        ]
