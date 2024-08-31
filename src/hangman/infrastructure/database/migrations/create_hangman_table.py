from sqlite3 import Connection, connect

from hangman.config import Config


def up():
    config = Config.load_config()
    if config.db_path is None:
        raise ValueError("db_path must be set for ")
    connection = connect(config.db_path)
    try:
        upgrade(connection)
    finally:
        connection.close()


def down():
    config = Config.load_config()
    if config.db_path is None:
        raise ValueError("db_path must be set for ")
    connection = connect(config.db_path)
    try:
        downgrade(connection)
    finally:
        connection.close()


def upgrade(connection: Connection):
    with connection as conn:
        conn.execute(
            """
        CREATE TABLE IF NOT EXISTS hangman (
            id INTEGER PRIMARY KEY, 
            word VARCHAR(255),
            max_error INTEGER,
            used_letters VARCHAR(255),
            user_id INTEGER UNIQUE 
        );
        """
        )


def downgrade(connection: Connection):
    with connection as conn:
        conn.execute(
            """
        DROP TABLE IF EXISTS hangman;
        """
        )
