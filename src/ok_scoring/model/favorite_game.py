from dataclasses import dataclass


@dataclass()
class FavoriteGame:
    key: str
    description: str

    def __eq__(self, other):
        return self.description == other.description
