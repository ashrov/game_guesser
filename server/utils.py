import json
from typing import Iterable


class Tag:
    def __init__(self, name="", question="", tag_id=-1, usage_count=0):
        self.id = tag_id
        self._name = name
        self._question = question
        self.usage_count = usage_count

    def from_db_row(self, row: Iterable):
        self.id, self._name, self._question, self.usage_count = row
        return self

    @property
    def name(self) -> str:
        return self._name

    @property
    def question(self) -> str:
        return self._question

    def __eq__(self, other):
        return True if self._name == other.name else False

    def __str__(self) -> str:
        return f"Tag: {self._name}; Question: {self._question}"

    def __lt__(self, other):
        return self.usage_count < other.usage_count


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

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class User:
    def __init__(self):
        self.current_game = Game()