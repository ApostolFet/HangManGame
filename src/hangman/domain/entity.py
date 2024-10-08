from collections.abc import Iterable
from enum import Enum, auto

from hangman.domain.exceptions import LetterAlredyGuessError


class GameState(Enum):
    COMING = auto()
    VICTORY = auto()
    DEFEAT = auto()


class HangManGame:
    def __init__(
        self,
        word: str,
        max_error: int,
        used_letters: Iterable[str] = "",
    ):
        self._word = word.lower()
        self._max_error = max_error

        self._used_letters = dict.fromkeys(used_letters)
        self._word_letters = set(self._word)

    @property
    def word(self) -> str:
        return self._word

    @property
    def max_error(self) -> int:
        return self._max_error

    @property
    def used_letters(self) -> list[str]:
        return list(self._used_letters)

    @property
    def indeces_guessed_letters(self) -> set[int]:
        all_indeces: set[int] = set()
        for index, letter in enumerate(self._word):
            if letter in self._used_letters:
                all_indeces.add(index)

        return all_indeces

    @property
    def count_error(self) -> int:
        count_err = 0
        for letter in self._used_letters:
            if letter not in self._word:
                count_err += 1
        return count_err

    @property
    def game_state(self) -> GameState:
        if self.count_error >= self._max_error:
            state = GameState.DEFEAT
        elif len(self._word) == len(self.indeces_guessed_letters):
            state = GameState.VICTORY
        else:
            state = GameState.COMING

        return state

    def guess(self, letter: str) -> bool:
        letter = letter.lower()
        if letter in self._used_letters:
            raise LetterAlredyGuessError(
                f"Character: '{letter}' has already been used before",
                letter=letter,
            )

        self._used_letters[letter] = None
        return letter in self._word_letters
