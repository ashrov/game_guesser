class Tag:
    def __init__(self, *args):
        """ :param: takes (name, question) or (id, name, question, usage_count) """

        match args:
            case name, question:
                self._tag_id = -1
                self._name = name
                self._question = question
                self.usage_count = -1
            case tag_id, name, question, usage_count:
                self._tag_id = tag_id
                self._name = name
                self._question = question
                self.usage_count = usage_count
            case _:
                raise ValueError

    @property
    def tag_id(self):
        return self._tag_id

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


class Game:
    def __init__(self, name="", game_id=-1, tags=[], bad_tags=[]):
        self._id = game_id
        self._name = name
        self.tags = tags
        self.bad_tags = bad_tags

    @property
    def name(self):
        return self._name

    def __eq__(self, other) -> bool:
        return True if all(self.tags) == all(other.tags) else False

    def __str__(self) -> str:
        return f"Name: {self._name}; Tags: {self.tags}"


class User:
    def __init__(self):
        self.current_game = Game()

