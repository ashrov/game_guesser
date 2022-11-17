from json import JSONEncoder, dumps
from typing import Iterable


class Tag:
    def __init__(self, name="", question="", tag_id=-1, usage_count=0):
        self.id = tag_id
        self.name = name
        self.question = question
        self.usage_count = usage_count

    def from_db_row(self, row: Iterable):
        self.id, self.name, self.question, self.usage_count = row
        return self

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            if self.id != -1 and other.id != -1:
                return True if self.id == other.id else False
            else:
                return True if self.name == other.name else False
        else:
            raise TypeError

    def __str__(self) -> str:
        return f"Tag: {self.name}; Question: {self.question}"

    def __lt__(self, other) -> bool:
        return self.usage_count < other.usage_count

    def __hash__(self) -> int:
        return self.id

    def get_all_data(self) -> dict:
        data = {
            'tag_name': self.name,
            'id': self.id,
            'question': self.question,
            'usage_count': self.usage_count
        }
        return data

    def to_json(self) -> str:
        return dumps(self.get_all_data())


class TagsList:
    def __init__(self, tags_list: Iterable[Tag] = []):
        self._list = list(tags_list)
        self._names_list = [tag.name for tag in self._list]

    @property
    def names_list(self):
        return self._names_list

    def from_names_list(self, names_list: Iterable[str] = []):
        self._names_list = list(names_list)
        self._list = [Tag(name=name) for name in names_list]
        return self

    def __str__(self):
        return str(self._names_list)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self._list):
            tag = self._list[self.i]
            self.i += 1
            return tag
        else:
            raise StopIteration

    def append(self, new_tag: Tag):
        self._list.append(new_tag)
        self._names_list.append(new_tag.name)


class Game:
    def __init__(self, name="", game_id=-1, tags=[], steam_url="", reviews_count=0):
        self.id = game_id
        self.name = name
        self.tags = tags
        self.steam_url = steam_url
        self.reviews_count = reviews_count

    def from_db_row(self, row: Iterable, tags: Iterable):
        self.id, self.name, self.steam_url, self.reviews_count = row
        self.tags = tags
        return self

    def __eq__(self, other) -> bool:
        return True if all(self.tags) == all(other.tags) else False

    def __str__(self) -> str:
        return f"Name: {self.name}; Tags: {self.tags}"

    def to_socket_message(self) -> bytes:
        data = f"({self.id}, {self.name}, {self.steam_url}, {self.reviews_count})"
        return data.encode('utf-8')

    def __hash__(self) -> int:
        return self.id

    def __lt__(self, other):
        return self.reviews_count < other.reviews_count

    def get_all_data(self) -> dict:
        data = {
            'game_name': self.name,
            'id': self.id,
            'steam_url': self.steam_url,
            'reviews_count': self.reviews_count
        }
        return data

    def to_json(self):
        return dumps(self.get_all_data())


class User:
    current_tag: Tag
    current_games: list[Game]

    def __init__(self, connection, address):
        self.good_tags: list[Tag] = []
        self.bad_tags: list[Tag] = []
        self.used_tags: list[Tag] = []
        self.connection = connection
        self.address = address
        self.current_games = list()
        self.current_tag = None

    def reset_tags(self):
        self.good_tags.clear()
        self.bad_tags.clear()
        self.used_tags.clear()

    def add_good_tag(self, tag: Tag):
        self.good_tags.append(tag)
        self.used_tags.append(tag)

    def add_bad_tag(self, tag: Tag):
        self.bad_tags.append(tag)
        self.used_tags.append(tag)

    def sort_all(self):
        self.good_tags.sort(reverse=True)
        self.bad_tags.sort(reverse=True)
        self.used_tags.sort(reverse=True)

    def delete_useless_tag(self):
        tag = self.used_tags.pop(-1)
        if tag in self.bad_tags:
            self.bad_tags.remove(tag)
        elif tag in self.good_tags:
            self.good_tags.remove(tag)


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Game):
            return o.get_all_data()
        elif isinstance(o, Tag):
            return o.get_all_data()
        else:
            return o
