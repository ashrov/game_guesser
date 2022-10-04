from database import DataBase


db = DataBase()
db.connect()


def get_question(tag: str) -> str:
    return "...question..."


def get_tag(current_tags: tuple | list) -> str:
    return "...tag..."


def close():
    db.disconnect()


get_question([])
close()
