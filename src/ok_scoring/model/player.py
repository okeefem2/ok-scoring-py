from dataclasses import dataclass


@dataclass(frozen=True)
class Player:
    key: str
    name: str
    favorite: bool

    def __eq__(self, other):
        return self.key == other.key
