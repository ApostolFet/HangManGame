from dataclasses import dataclass

from hangman.domain.entity import GameState, HangManGame


@dataclass
class GameStep:
    word: str
    indeces_guessed_letters: set[int]
    try_letters: list[str]
    count_error: int
    game_state: GameState
    guess: bool | None = None

    @classmethod
    def from_hangman(
        cls,
        hangman_game: HangManGame,
        guess: bool | None = None,
    ) -> "GameStep":
        return cls(
            word=hangman_game.word,
            indeces_guessed_letters=hangman_game.indeces_guessed_letters,
            try_letters=hangman_game.used_letters,
            count_error=hangman_game.count_error,
            game_state=hangman_game.game_state,
            guess=guess,
        )
