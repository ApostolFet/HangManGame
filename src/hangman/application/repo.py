from typing import Protocol

from hangman.domain.entity import HangManGame


class HangManRepository(Protocol):
    def get(self, user_id: int) -> HangManGame: ...

    def add(self, user_id: int, hangman_game: HangManGame) -> None: ...
