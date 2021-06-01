from dataclasses import dataclass


@dataclass()
class Player:
    key: str
    name: str
    favorite: bool = False

    def __eq__(self, other):
        return self.key == other.key
