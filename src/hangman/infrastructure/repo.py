from hangman.application.interfaces.repo import HangManRepository
from hangman.domain.entity import HangManGame


class GameNotFoundError(Exception): ...


class InMemoryHangmanRepository(HangManRepository):
    def __init__(self) -> None:
        self._storage: dict[int, HangManGame] = {}

    def get(self, user_id: int) -> HangManGame:
        game = self._storage.get(user_id)
        if game is None:
            raise GameNotFoundError()
        return game

    def add(self, user_id: int, hangman_game: HangManGame) -> None:
        self._storage[user_id] = hangman_game
