DATABASE_NAME = "database.db"

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


