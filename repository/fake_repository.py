# class FakeRepository(AbstractRepository):
#
#     def __init__(self, data):
#         self._data = set(data)
#
#     def add(self, batch):
#         self._data.add(batch)
#
#     def get(self, reference):
#         return next(b for b in self._data if b.reference == reference)
#
#     def list(self):
#         return list(self._data)