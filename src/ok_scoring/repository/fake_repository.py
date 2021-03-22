from ok_scoring.repository.abstract_repository import AbstractRepository


class FakeRepository(AbstractRepository):

    def __init__(self, entities):
        self._entities = set(entities)

    def add(self, batch):
        self._entities.add(batch)

    def get(self, key):
        return next(b for b in self._entities if b.key == key)

    def list(self):
        return list(self._entities)

    def delete(self, key):
        self._entities.remove(self.get(key))

    def update(self, entity):
        self.delete(entity.key)
        self.add(entity)
