from sqlite3 import Connection

import pytest
from hangman.domain.entity import HangManGame
from hangman.infrastructure.database.repo import SqliteHangManRepository


def test_get_hangman(connection_in_memory_db: Connection) -> None:
    game = HangManGame(word="test", max_error=5, used_letters=["s", "d", "g"])
    user_id = 1

    repo = SqliteHangManRepository(connection_in_memory_db)
    repo.add(user_id, game)
    result = repo.get(user_id)

    assert (
        result.word,
        result.max_error,
        result.used_letters,
    ) == (
        game.word,
        game.max_error,
        game.used_letters,
    )


@pytest.mark.repeat(3)
def test_get_latest_hangman(connection_in_memory_db: Connection) -> None:
    game_first = HangManGame(word="first", max_error=5, used_letters="firsd")
    game_second = HangManGame(word="second", max_error=7, used_letters=list("secont"))
    game_latest = HangManGame(word="latest", max_error=10, used_letters=tuple("latesd"))
    user_id = 1

    repo = SqliteHangManRepository(connection_in_memory_db)
    repo.add(user_id, game_first)
    repo.add(user_id, game_second)
    repo.add(user_id, game_latest)
    result = repo.get(user_id)

    assert (
        result.word,
        result.max_error,
        result.used_letters,
    ) == (
        game_latest.word,
        game_latest.max_error,
        game_latest.used_letters,
    )
