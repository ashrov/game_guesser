from database import DataBase
from utils import Game, Tag


class Guesser:
    def __init__(self):
        self.db = DataBase()
        self.all_games = set(self.db.get_all_games())

    def close(self):
        self.db.disconnect()

    def guess_game(self, string):
        tags_names = string.split('_')
        tag_list = [self.db.get_tag_by_name(tag_name) for tag_name in tags_names]
        tag_list.sort(reverse=True)

        return self.selection(tag_list)

    def selection(self, tags: list[Tag]):
        ans = self.sort_games(tags)

        while not ans:
            tags.pop(-1)
            ans = self.sort_games(tags)

        return ans[0]

    def sort_games(self, tags) -> list[Game]:
        ans = self.all_games
        for tag in tags:
            temp = self.db.get_games_with_tag(tag)
            ans = set(temp) & ans
            if not ans:
                break

        ans = list(ans)
        ans.sort(reverse=True)

        return ans
