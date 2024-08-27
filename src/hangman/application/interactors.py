from hangman.application.dto import GameStep
from hangman.application.interfaces.letter_validator import LetterValidator
from hangman.application.interfaces.word_provider import WordProvider
from hangman.application.interfaces.repo import HangManRepository
from hangman.domain.entity import HangManGame


class GuessLeterInteractor:
    def __init__(
        self,
        hangman_repo: HangManRepository,
        letter_validator: LetterValidator,
    ):
        self._hangman_repo = hangman_repo
        self._letter_validator = letter_validator

    def __call__(self, user_id: int, letter: str) -> GameStep:
        self._letter_validator.validate(letter)

        hangman_game = self._hangman_repo.get(user_id)
        guessed = hangman_game.guess(letter)

        self._hangman_repo.add(user_id, hangman_game)
        return GameStep.from_hangman(hangman_game, guessed)


class CreateGameInteractor:
    def __init__(
        self,
        hangman_repo: HangManRepository,
        word_provider: WordProvider,
        max_error: int,
    ):
        self._hangman_repo = hangman_repo
        self._word_provider = word_provider
        self._max_error = max_error

    def __call__(self, user_id: int) -> GameStep:
        word = self._word_provider.get_random_word()
        hangman_game = HangManGame(word, self._max_error)
        self._hangman_repo.add(user_id, hangman_game)
        return GameStep.from_hangman(hangman_game)
