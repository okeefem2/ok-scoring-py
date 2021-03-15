import time
from uuid import uuid4


def unique_id() -> str:
    return str(uuid4())


def now() -> int:
    return int(time.time() * 1000)
