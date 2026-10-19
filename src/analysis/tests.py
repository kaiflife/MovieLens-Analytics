import pytest

from .links import Links
from .movies import Movies
from .ratings import Ratings
from .tags import Tags


class Tests:
    """PyTest test class for the above classes."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Инициализация объектов перед каждым тестом."""
        self.ratings = Ratings()
        self.tags = Tags()
        self.movies = Movies()
        self.links = Links()

    # --- TESTS FOR RATINGS ---

    def test_get_movies_by_rating(self):
        result = self.ratings.get_movies_by_rating()
        # 1. Проверка типа возвращаемого значения
        assert isinstance(result, dict)
        # 2. Проверка типов элементов
        for key, value in result.items():
            assert isinstance(key, int)
            assert isinstance(value, list)
            for rating in value:
                assert isinstance(rating, float)

    def test_get_top_N_movies(self):
        result = self.ratings.get_top_N_movies(5)
        # 1. Проверка типа
        assert isinstance(result, list)
        # 2. Проверка типов элементов
        for item in result:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)  # movieId
            assert isinstance(item[1], float)  # avg rating
        # 3. Проверка сортировки (по убыванию рейтинга)
        ratings = [item[1] for item in result]
        assert ratings == sorted(ratings, reverse=True)

    def test_get_movies_by_year(self):
        result = self.ratings.get_movies_by_year(2015)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], float)
        # Проверка сортировки
        ratings = [item[1] for item in result]
        assert ratings == sorted(ratings, reverse=True)

    def test_get_average_rating_by_year(self):
        result = self.ratings.get_average_rating_by_year()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)  # year
            assert isinstance(item[1], float)  # avg rating
        # Проверка сортировки (по возрастанию года)
        years = [item[0] for item in result]
        assert years == sorted(years)

    # --- TESTS FOR TAGS ---

    def test_get_most_words_tags(self):
        result = self.tags.get_most_words_tags(5)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert isinstance(item[0], str)  # tag
            assert isinstance(item[1], int)  # word count
        # Проверка сортировки (по убыванию количества слов)
        counts = [item[1] for item in result]
        assert counts == sorted(counts, reverse=True)

    def test_get_longest_tag(self):
        result = self.tags.get_longest_tag()
        assert isinstance(result, str)
        # Проверка, что это действительно самый длинный тег (опционально)
        all_tags = [row["tag"] for row in self.tags.data]
        if all_tags:
            assert len(result) == max(len(tag) for tag in all_tags)

    def test_get_tags_with_specific_word(self):
        result = self.tags.get_tags_with_specific_word("love")
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, str)
            assert "love" in item.lower()

    # --- TESTS FOR MOVIES ---

    def test_dist_by_release(self):
        result = self.movies.dist_by_release()
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, int)  # year
            assert isinstance(value, int)  # count

    def test_dist_by_genres(self):
        result = self.movies.dist_by_genres()
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)  # genre
            assert isinstance(value, int)  # count

    def test_top_N_movies_by_rating(self):
        result = self.movies.top_N_movies_by_rating(5, self.ratings)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert isinstance(item[0], str)  # title
            assert isinstance(item[1], float)  # avg rating
        # Проверка сортировки
        ratings = [item[1] for item in result]
        assert ratings == sorted(ratings, reverse=True)

    def test_get_movies_by_title(self):
        result = self.movies.get_movies_by_title("Star")
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, str)
            assert "star" in item.lower()

    # --- TESTS FOR LINKS ---

    def test_get_movie_id_by_imdb(self):
        # Берем первый попавшийся ID из данных
        if self.links.data:
            imdb_id = self.links.data[0]["imdbId"]
            result = self.links.get_movie_id_by_imdb(imdb_id)
            assert isinstance(result, int)

    def test_get_imdb_id_by_movie(self):
        if self.links.data:
            movie_id = self.links.data[0]["movieId"]
            result = self.links.get_imdb_id_by_movie(movie_id)
            assert isinstance(result, str)
            assert len(result) == 7  # Проверяем, что zfill сработал

    def test_get_movie_info_by_imdb(self):
        if self.links.data:
            imdb_id = self.links.data[0]["imdbId"]
            result = self.links.get_movie_info_by_imdb(imdb_id)
            assert isinstance(result, dict)
            assert "title" in result
            assert "url" in result
            assert "status" in result
