"""label module"""

from ..utils.store import BaseStore

class Label(BaseStore):
    """
        Represents an assembly label
    """

    def __init__(self, name: str):
        super().__init__()

        self.name = name

    def __str__(self) -> str:
        ret = [self.name + ":"]

        for obj in self.get_store():
            ret.append("    " + str(obj))

        return "\n".join(ret) + "\n"
