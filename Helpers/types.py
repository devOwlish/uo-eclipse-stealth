from .config import Config
from py_stealth import *


class Types():
    """
        Class for tile manipulation
    """
    def __init__(self):
        self._types = Config("Common/types.yaml").get()

    def get_category(self, category: str) -> int:
        """
            Get types by category
        """
        if category in self._types:
            return self._types.get(category)

        raise KeyError(f"Category {category} is not found in the types.yaml")

    def find_by_name(self, name: str) -> int:
        """
            Get type by name
        """
        for category in self._types:
            if name in self._types.get(category):
                return self._types.get(category).get(name)

        raise KeyError(f"Type {name} is not found in the types.yaml")
