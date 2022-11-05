from sqlite3 import Connection, Cursor, connect

from utils import Game, Tag, TagsList
import config


DB_TABLES = {
    "games": ("id INTEGER PRIMARY KEY",
              "game_name TEXT",
              "steam_url TEXT",
              "reviews_count INT"),
    "tags": ("id INTEGER PRIMARY KEY",
             "tag_name TEXT",
             "question TEXT",
             "usage_count INTEGER DEFAULT 0"),
    "game_to_tag": ("game_id INT",
                    "tag_id INT")
}


class DataBase:
    _connection: Connection
    _cursor: Cursor
    _tags_list: TagsList

    def __init__(self):
        self.connect()
        self._create_tables()
        self._tags_list = TagsList(self.get_all_tags())

    def _create_tables(self):
        for table_name, columns in DB_TABLES.items():
            columns_sql = ", ".join(columns)
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
            self._cursor.execute(sql)

    def connect(self):
        try:
            self._connection = connect(config.DATABASE_NAME, isolation_level=None)
        except ConnectionError as er:
            print(f"unable to connect to {config.DATABASE_NAME}. {er}")
        else:
            print(f"{config.DATABASE_NAME} connected")
            self._cursor = self._connection.cursor()

    def disconnect(self):
        self._cursor.close()
        self._connection.close()
        print(f"{config.DATABASE_NAME} disconnected")

    def drop_games(self):
        sql = "DROP TABLE games;" \
              "DROP TABLE game_to_tag;" \
              "UPDATE tags SET usage_count = 0"
        self._cursor.executescript(sql)
        self._create_tables()

    def add_game(self, game: Game):
        sql = "INSERT INTO games (game_name, steam_url, reviews_count) VALUES (?, ?, ?)"
        self._cursor.execute(sql, (game.name, game.steam_url, game.reviews_count))
        print("game row added")
        for tag in game.tags:
            self._link_tag_to_game(game, tag)
            print(f"({tag}) linked")

    def _link_tag_to_game(self, game: Game, tag: Tag):
        if tag.name not in self._tags_list.names_list:
            self._add_tag(tag)

        self.increment_usage(tag)
        sql = "INSERT INTO game_to_tag (game_id, tag_id) " \
              "SELECT games.id, tags.id FROM games, tags WHERE games.game_name = ? AND tags.tag_name = ?"
        self._cursor.execute(sql, (game.name, tag.name))

    def get_all_games(self) -> list[Game]:
        sql = "SELECT * from games"
        self._cursor.execute(sql)
        return [Game().from_db_row(line, self._get_game_tags(line[0])) for line in self._cursor.fetchall()]

    def _get_game_tags(self, game_id: int) -> list[Tag]:
        sql = "SELECT tag_id FROM game_to_tag WHERE game_id = ?"
        self._cursor.execute(sql, (game_id, ))
        return [Tag().from_db_row(tag_id[0]) for tag_id in self._cursor.fetchall()]

    def _get_tag_by_id(self, tag_id: int) -> Tag:
        sql = "SELECT * from tags WHERE id = ?"
        self._cursor.execute(sql, (tag_id, ))
        return Tag().from_db_row(self._cursor.fetchone())

    def get_all_tags(self) -> list[Tag]:
        sql = "SELECT * from tags"
        self._cursor.execute(sql)
        return [Tag().from_db_row(line) for line in self._cursor.fetchall()]

    def _add_tag(self, tag: Tag):
        sql = f"INSERT INTO tags (tag_name, question) VALUES (?, ?)"
        self._cursor.execute(sql, (tag.name, tag.question))
        sql = f"SELECT id FROM tags WHERE tag_name = ?"
        self._cursor.execute(sql, (tag.name, ))
        tag.id = self._cursor.fetchone()[0]
        self._tags_list.append(tag)

    def increment_usage(self, tag: Tag):
        sql = f"UPDATE tags SET usage_count = usage_count + 1 WHERE tag_name = ?"
        self._cursor.execute(sql, (tag.name, ))
        tag.usage_count += 1

