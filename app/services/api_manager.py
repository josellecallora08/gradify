import itertools
import os
from typing import List


class APIManager:
    def __init__(self, keys: List[str]) -> None:
        self.keys = itertools.cycle(keys)

    def get_next_key(self):
        return next(self.keys)

    def __repr__(self):
        return f"APIManager(keys={self.keys})"
