from database import DataBase
from utils import Tag

db = DataBase()
tag = Tag("test_name2", "if test2?")

db.increment_usage(tag)
print(str(db.get_tags()[1]))
db.disconnect()


