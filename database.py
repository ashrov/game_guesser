from sqlite3 import Connection, Cursor, connect

from utils import Game, Tag
import config


DB_TABLES = {
    "games": ("id INTEGER PRIMARY KEY",
              "game_name TEXT",
              "steam_url TEXT"),
    "tags": ("id INTEGER PRIMARY KEY",
             "tag_name TEXT",
             "question TEXT",
             "usage_count INTEGER DEFAULT 0"),
    "links": ("game_id INT",
              "tag_id INT")
}


class DataBase:
    _connection: Connection
    _cursor: Cursor

    def __init__(self):
        self.connect()
        self._create_tables()

    def _create_tables(self):
        for table_name, columns in DB_TABLES.items():
            columns_sql = ""
            for column in columns:
                columns_sql += f"{column}{', ' if column != columns[-1] else ''}"

            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
            self._cursor.execute(sql)

    def connect(self):
        try:
            self._connection = connect(config.DATABASE_NAME)
        except ConnectionError as er:
            print(f"unable to connect to {config.DATABASE_NAME}. {er}")
        else:
            print(f"{config.DATABASE_NAME} connected")
            self._connection.isolation_level = None
            self._cursor = self._connection.cursor()

    def disconnect(self):
        self._cursor.close()
        self._connection.close()
        print(f"{config.DATABASE_NAME} disconnected")

    def add_game(self, game: Game):
        sql = "INSERT INTO games (game_name) VALUES (?)"
        self._cursor.execute(sql, (game.name, ))

    def add_tag_to_game(self, game: Game, tag: Tag):
        sql = "INSERT INTO links VALUES (?, ?)"
        self._cursor.execute(sql, (game, tag))

    def get_all_tags(self) -> list[Tag]:
        sql = "SELECT * from tags"
        self._cursor.execute(sql)
        tags = [Tag(*line) for line in self._cursor.fetchall()]
        return tags

    def add_tag(self, tag: Tag):
        sql = f"INSERT INTO tags (tag_name, question) VALUES (?, ?)"
        self._cursor.execute(sql, (tag.name, tag.question))

    def increment_usage(self, tag: Tag):
        sql = f"UPDATE tags SET usage_count = usage_count + 1 WHERE tag_name = '{tag.name}'"
        self._cursor.execute(sql)

