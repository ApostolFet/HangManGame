import random
from pathlib import Path


class FileWordProvider:
    def __init__(self, file_path_words: Path):
        self._file_path_words = file_path_words

    def get_random_word(self) -> str:
        words = self._get_words()
        random_word = random.choice(words)
        return random_word

    def _get_words(self) -> list[str]:
        words = []
        with open(self._file_path_words) as file:
            for word in file:
                words.append(word.strip())

        return words
