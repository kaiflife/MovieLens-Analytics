from .links import Links
from .movies import Movies
from .ratings import Ratings
from .tags import Tags
from .tests import Tests

# Этот файл нужен, чтобы папка считалась Python-пакетом. Мы можем сразу импортировать в него классы
# для удобства (чтобы в ноутбуке писать from analysis import Ratings, а не from analysis.ratings import Ratings).

__all__ = ["Links", "Movies", "Ratings", "Tags", "Tests"]
