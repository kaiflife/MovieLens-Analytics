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

    # ==========================================
    # --- TESTS FOR RATINGS ---
    # ==========================================

    def test_get_movies_by_rating(self):
        result = self.ratings.get_movies_by_rating()
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, int)
            assert isinstance(value, list)
            for rating in value:
                assert isinstance(rating, float)

    def test_get_top_N_movies(self):
        result = self.ratings.get_top_N_movies(5)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], float)

        # Проверка сортировки
        ratings = [item[1] for item in result]
        assert ratings == sorted(ratings, reverse=True)

    def test_get_movies_by_year(self):
        result = self.ratings.get_movies_by_year(2015)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], float)

        ratings = [item[1] for item in result]
        assert ratings == sorted(ratings, reverse=True)

    def test_get_average_rating_by_year(self):
        result = self.ratings.get_average_rating_by_year()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], float)

        years = [item[0] for item in result]
        assert years == sorted(years)

    def test_get_top_N_movies_correctness(self):
        movies_by_rating = self.ratings.get_movies_by_rating()
        target_movie = None
        for m_id, ratings in movies_by_rating.items():
            if len(ratings) > 1:
                target_movie = m_id
                expected_avg = round(sum(ratings) / len(ratings), 2)
                break

        if target_movie:
            top_movies = self.ratings.get_top_N_movies(len(movies_by_rating))
            found = False
            for m_id, avg in top_movies:
                if m_id == target_movie:
                    assert avg == expected_avg
                    found = True
                    break
            assert found, "Фильм с несколькими оценками не найден в топе"

    # ==========================================
    # --- TESTS FOR TAGS ---
    # ==========================================

    def test_get_most_words_tags(self):
        result = self.tags.get_most_words_tags(5)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert isinstance(item[0], str)
            assert isinstance(item[1], int)

        counts = [item[1] for item in result]
        assert counts == sorted(counts, reverse=True)

    def test_get_longest_tag(self):
        result = self.tags.get_longest_tag()
        assert isinstance(result, str)
        all_tags = [row["tag"] for row in self.tags.data]
        if all_tags:
            assert len(result) == max(len(tag) for tag in all_tags)

    def test_get_tags_with_specific_word(self):
        result = self.tags.get_tags_with_specific_word("love")
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, str)
            assert "love" in item.lower()

    # ==========================================
    # --- TESTS FOR MOVIES ---
    # ==========================================

    def test_dist_by_release(self):
        result = self.movies.dist_by_release()
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, int)
            assert isinstance(value, int)

    def test_dist_by_genres(self):
        result = self.movies.dist_by_genres()
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, int)

    def test_top_N_movies_by_rating(self):
        result = self.movies.top_N_movies_by_rating(5, self.ratings)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert isinstance(item[0], str)
            assert isinstance(item[1], float)

        ratings = [item[1] for item in result]
        assert ratings == sorted(ratings, reverse=True)

    def test_get_movies_by_title(self):
        result = self.movies.get_movies_by_title("Star")
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, str)
            assert "star" in item.lower()

    # ==========================================
    # --- TESTS FOR LINKS ---
    # ==========================================

    def test_get_movie_id_by_imdb(self):
        if self.links.data:
            imdb_id = self.links.data[0]["imdbId"]
            result = self.links.get_movie_id_by_imdb(imdb_id)
            assert isinstance(result, int)

    def test_get_imdb_id_by_movie(self):
        if self.links.data:
            movie_id = self.links.data[0]["movieId"]
            result = self.links.get_imdb_id_by_movie(movie_id)
            assert isinstance(result, str)
            assert len(result) == 7

    def test_get_movie_info_by_imdb(self):
        if self.links.data:
            imdb_id = self.links.data[0]["imdbId"]
            result = self.links.get_movie_info_by_imdb(imdb_id)
            assert isinstance(result, dict)
            assert "title" in result
            assert "url" in result
            assert "status" in result
