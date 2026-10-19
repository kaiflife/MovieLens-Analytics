import config
from logger import log_method
from .base import BaseDataLoader


class Tags(BaseDataLoader):
    def _parse_row(self, cols: list[str]) -> dict | None:
        if len(cols) == 4:
            return {
                "userId": int(cols[0]),
                "movieId": int(cols[1]),
                "tag": cols[2],
                "timestamp": int(cols[3]),
            }
        return None

    @log_method
    def get_most_words_tags(self, N: int) -> list[tuple[str, int]]:
        tag_word_counts: dict[str, int] = {
            row["tag"]: len(config.REGEX["word"].findall(row["tag"]))
            for row in self.data
        }
        return sorted(tag_word_counts.items(), key=lambda x: (-x[1], x[0]))[:N]

    @log_method
    def get_longest_tag(self) -> str:
        if not self.data:
            return ""
        return max((row["tag"] for row in self.data), key=len)

    @log_method
    def get_tags_with_specific_word(self, word: str) -> list[str]:
        word = word.lower()
        return list({row["tag"] for row in self.data if word in row["tag"].lower()})
