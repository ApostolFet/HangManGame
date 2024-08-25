from hangman.application.dto import CreateHangMan, GameStep
from hangman.application.interfaces.repo import HangManRepository


class GuessLaterInteractor:
    def __init__(self, hangman_repo: HangManRepository):
        self._hangman_repo = hangman_repo

    def __call__(self, user_id: int, letter: str) -> GameStep:
        hangman_game = self._hangman_repo.get(user_id)
        guessed = hangman_game.guess(letter)
        self._hangman_repo.add(user_id, hangman_game)
        return GameStep.from_hangman(hangman_game, guessed)


class CreateGameInteractor:
    def __init__(self, hangman_repo: HangManRepository):
        self._hangman_repo = hangman_repo

    def __call__(self, user_id: int, create_hangman: CreateHangMan) -> GameStep:
        hangman_game = create_hangman.to_hangman()
        self._hangman_repo.add(user_id, hangman_game)
        return GameStep.from_hangman(hangman_game)
