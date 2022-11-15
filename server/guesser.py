from database import DataBase
from utils import Game, Tag

from typing import Iterable
import random


class Guesser:
    def __init__(self):
        self._db = DataBase()
        self.all_games = set(self._db.get_all_games())
        self.all_tags = set(self._db.get_all_tags())

    def close(self):
        self._db.disconnect()

    def guess_game(self, tags, selection_size) -> list[Game]:
        tags.sort(reverse=True)

        return self.selection(tags, selection_size)

    def selection(self, tags: list[Tag], selection_size):
        ans = self.select_games_by_tags(tags)

        while len(ans) < selection_size:
            tags.pop(-1)
            ans = self.select_games_by_tags(tags)

        return ans[0:selection_size]

    def select_games_by_tags(self, tags: list[Tag]) -> list[Game]:
        ans = self.all_games
        for tag in tags:
            temp = self._db.get_games_with_tag(tag)
            ans = set(temp) & ans
            if not ans:
                break

        ans = list(ans)
        ans.sort(reverse=True)

        return ans

    def get_new_tag(self, current_tags: Iterable[Tag]) -> Tag:
        cur = set(current_tags)
        remaining_tags = self.all_tags - cur
        return random.choice(tuple(remaining_tags))

