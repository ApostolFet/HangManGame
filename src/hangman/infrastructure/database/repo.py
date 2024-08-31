from contextlib import closing
from sqlite3 import Connection

from hangman.application.interfaces.repo import HangManRepository
from hangman.domain.entity import HangManGame
from hangman.infrastructure.repo import GameNotFoundError


class SqliteHangManRepository(HangManRepository):
    def __init__(self, connection: Connection):
        self._connection = connection

    def get(self, user_id: int) -> HangManGame:
        with self._connection as conn, closing(conn.cursor()) as cur:
            result = cur.execute(
                """
                    SELECT word, max_error, used_letters 
                    FROM hangman WHERE user_id = ?
                """,
                (user_id,),
            )
            row_data = result.fetchone()

        if row_data is None:
            raise GameNotFoundError()

        word, max_error, used_letters = row_data
        return HangManGame(word, max_error, set(used_letters))

    def add(self, user_id: int, hangman_game: HangManGame):
        with self._connection as conn, closing(conn.cursor()) as cur:
            cur.execute(
                """
                    INSERT INTO hangman (word, max_error, used_letters, user_id) 
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        word = excluded.word,
                        max_error = excluded.max_error,
                        used_letters = excluded.used_letters;
                """,
                (
                    hangman_game.word,
                    hangman_game.max_error,
                    "".join(hangman_game.used_letters),
                    user_id,
                ),
            )
