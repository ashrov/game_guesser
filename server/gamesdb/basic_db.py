from logging import getLogger
import os
from sqlite3 import Connection, Cursor, connect


DB_NAME = "/database.db"
DB_TABLES = {
    "games": ("id INTEGER PRIMARY KEY",
              "game_name TEXT UNIQUE",
              "steam_url TEXT",
              "reviews_count INT"),
    "tags": ("id INTEGER PRIMARY KEY",
             "tag_name TEXT UNIQUE",
             "question TEXT",
             "usage_count INTEGER DEFAULT 0"),
    "game_to_tag": ("game_id INT",
                    "tag_id INT")
}


logger = getLogger(__name__)


class BasicDataBase:
    _connection: Connection
    _cursor: Cursor

    def __init__(self):
        self._path = os.path.abspath(os.path.dirname(__file__) + DB_NAME)
        self._connect()
        self._create_tables()

    def delete_tables(self):
        for table_name in DB_TABLES.keys():
            sql = f"DROP TABLE {table_name}"
            self._cursor.execute(sql)

    def set_savepoint(self, name):
        self._connection.execute(f"savepoint {name}")

    def release_savepoint(self, name):
        self._connection.execute(f"release savepoint {name}")

    def rollback_to_savepoint(self, name):
        self._connection.execute(f"rollback to savepoint {name}")

    def disconnect(self):
        self._cursor.close()
        self._connection.close()
        logger.debug(f"{DB_NAME} disconnected")

    def _connect(self):
        try:
            self._connection = connect(self._path)
            logger.debug(f"{DB_NAME} connected")
            self._cursor = self._connection.cursor()
        except Exception as er:
            logger.error(f"unable to connect to {self._path}. {er}")

    def _create_tables(self):
        for table_name, columns in DB_TABLES.items():
            columns_sql = ", ".join(columns)
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
            self._cursor.execute(sql)
