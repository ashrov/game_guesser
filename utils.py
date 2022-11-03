from typing import Iterable


class Tag:
    def __init__(self, name="", question="", tag_id=-1, usage_count=0):
        self.id= tag_id
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


class TagsList:
    def __init__(self, tags_list: Iterable[Tag]):
        self._list = list(tags_list)
        self._names_array = [tag.name for tag in self._list]

    @property
    def names_list(self):
        return self._names_array

    def __iter__(self):
        self.i = 0

    def __next__(self):
        if self.i < len(self._list):
            tag = self._list[self.i]
            self.i += 1
            return tag
        else:
            raise StopIteration

    def append(self, new_tag: Tag):
        self._list.append(new_tag)
        self._names_array.append(new_tag.name)


class Game:
    def __init__(self, name="", game_id=-1, tags=None, steam_url=""):
        self.id = game_id
        self._name = name
        self.tags = tags
        self.steam_url = steam_url

    @property
    def name(self):
        return self._name

    def from_db_row(self, row: Iterable, tags: Iterable[Tag]):
        self.id, self._name, self.steam_url = row
        self.tags = tags
        return self

    def __eq__(self, other) -> bool:
        return True if all(self.tags) == all(other.tags) else False

    def __str__(self) -> str:
        return f"Name: {self._name}; Tags: {self.tags}"


class User:
    def __init__(self):
        self.current_game = Game()

