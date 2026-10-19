import functools
import logging
from pathlib import Path

# Создаем папку для логов, если её нет
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def get_class_logger(instance) -> logging.Logger:
    """Возвращает логгер, привязанный к имени класса."""
    class_name = instance.__class__.__name__
    logger = logging.getLogger(class_name)

    # Если логгер еще не настроен, настраиваем его
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Формат: [Время] - [Уровень] - [Сообщение]
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Пишем лог в файл. Пример: logs/Ratings.log
        file_handler = logging.FileHandler(
            LOG_DIR / f"{class_name}.log", encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def log_method(func):
    """Декоратор, который логирует вызов метода в файл класса."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        logger = get_class_logger(self)

        # Логируем вход
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")

        try:
            result = func(self, *args, **kwargs)
            # Логируем успешный выход (можно залогировать тип результата, чтобы не писать огромные списки в файл)
            logger.info(
                f"Finished {func.__name__} | Return type: {type(result).__name__}"
            )
            return result
        except Exception as e:
            # Логируем ошибку с трейсбеком
            logger.error(f"Error in {func.__name__}: {e!s}", exc_info=True)
            raise

    return wrapper
