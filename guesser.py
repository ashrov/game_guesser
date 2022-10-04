from database import DataBase


db = DataBase()
db.connect()


def get_question(tag: str) -> str:
    return "...question..."


def close():
    db.disconnect()


get_question([])
close()
