from sqlite3 import Connection, connect
from typing import Iterator

import pytest

from hangman.infrastructure.database.migrations.create_hangman_table import upgrade


@pytest.fixture
def connection_in_memory_db() -> Iterator[Connection]:
    connection = connect(":memory:")

    upgrade(connection)
    try:
        yield connection
    finally:
        connection.close()
