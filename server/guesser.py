from database import DataBase
from utils import Game, Tag, User

import random


class Guesser:
    def __init__(self):
        self.db = DataBase()

    def close(self):
        self.db.disconnect()

    def guess_game(self, user: User, selection_size=-1) -> list[Game]:
        ans = self.selection(user)
        while len(ans) < selection_size:
            user.delete_useless_tag()
            ans = self.selection(user)

        if selection_size == -1:
            selection_size = len(ans)

        ans = sorted(list(ans), reverse=True)
        return ans[0:selection_size]

    def selection(self, user: User):
        good_games = self.select_good_games(user.good_tags)
        bad_games = self.select_bad_games(user.bad_tags)
        return good_games - bad_games

    def select_good_games(self, tags: list[Tag]) -> set[Game]:
        ans = set(self.db.get_all_games())
        for tag in tags:
            temp = self.db.get_games_with_tag(tag)
            ans = set(temp) & ans
            if not ans:
                break

        return ans

    def select_bad_games(self, tags: list[Tag]) -> set[Game]:
        ans = set()
        for tag in tags:
            temp = self.db.get_games_with_tag(tag)
            ans = set(temp) | ans

        return ans

    def get_new_tag(self, user: User) -> Tag:
        remaining_tags = set(self.db.get_all_tags()) - set(user.used_tags)

        remaining_tags = sorted(list(remaining_tags))
        chances = []
        for i in range(len(remaining_tags)):
            chances += [i] * (i+1)

        n = random.choice(chances)
        return remaining_tags[n]
