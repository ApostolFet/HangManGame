from typing import Protocol


class WordProvider(Protocol):
    def get_random_word(self) -> str: ...
