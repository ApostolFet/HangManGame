import random
from pathlib import Path

from hangman.application.interfaces.word_provider import WordProvider


class FileWordProvider(WordProvider):
    def __init__(self, file_path_words: Path):
        self._file_path_words = file_path_words

    def get_random_word(self) -> str:
        words = self._get_words()
        random_word = random.choice(words)
        return random_word

    def _get_words(self) -> list[str]:
        with self._file_path_words.open() as file:
            words = [word.strip() for word in file]

        return words
