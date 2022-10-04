class Game:
    def __init__(self, name: str, tags: list | tuple | None):
        self._name = name
        self._tags = tags

    @property
    def name(self):
        return self._name

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags: list | tuple):
        self._tags = tags

    def __eq__(self, other) -> bool:
        if all(self._tags) == all(self.tags):
            return True
        else:
            return False

    def __str__(self) -> str:
        s = f"Name: {self._name}; Tags: {self._tags}"
        return s

