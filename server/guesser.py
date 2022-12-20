from gamesdb import GuesserDataBase, Game, Tag, User

import random


class Guesser:
    def __init__(self):
        self.db = GuesserDataBase()

    def close(self):
        self.db.disconnect()

    def get_new_tag(self, user: User) -> Tag:
        remaining_tags = tuple(self._get_possible_tags(user))

        weights = [tag.usage_count for tag in remaining_tags]
        return random.choices(remaining_tags, weights=weights)[0]

    def guess_game(self, user: User, selection_size=-1) -> list[Game]:
        ans = self._get_selection(user)
        while len(ans) < selection_size:
            user.delete_useless_tag()
            ans = self._get_selection(user)

        if selection_size == -1:
            selection_size = len(ans)

        ans = sorted(list(ans), reverse=True)
        return ans[0:selection_size]

    def _get_selection(self, user: User):
        good_games = self._select_good_games(user.good_tags)
        bad_games = self._select_bad_games(user.bad_tags)
        return good_games - bad_games

    def _select_good_games(self, tags: list[Tag]) -> set[Game]:
        ans = set(self.db.all_games)
        for tag in tags:
            ans &= self.db.get_games_with_tag(tag)

            if not ans:
                break

        return ans

    def _select_bad_games(self, tags: list[Tag]) -> set[Game]:
        ans = set()
        for tag in tags:
            ans |= self.db.get_games_with_tag(tag)

        return ans

    def _get_possible_tags(self, user: User, games_threshold=50) -> set[Tag]:
        if not (1 < len(user.current_games) <= games_threshold):
            return self.db.all_tags - set(user.used_tags)

        possible_tags = set()
        for game in user.current_games:
            possible_tags |= self.db.get_game_tags(game.id)

        return possible_tags - set(user.used_tags)
