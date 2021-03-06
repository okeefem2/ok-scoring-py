from dataclasses import dataclass


@dataclass(frozen=True)
class FavoriteGame:
    key: str
    description: str

    def __eq__(self, other):
        return self.description == other.description
