"""x86 assembly module"""

from typing import Self
from typing import List

from .label import Label
from ..utils.store import BaseStore

from ..exceptions.exception import OtError

class Assembly(BaseStore):
    """
        Managing asm dumping
    """
    
    def __init__(self):
        super().__init__()
        
        self.__labels = []
        
    def label_exists(self, obj: Label) -> bool:
        """
            Returns if a label already exists
        """
    
        return obj.name in self.__labels

    def add_label(self, obj: Label) -> Self:
        """
            Add a label to `self.__store` and `self.__labels`
        """
        
        if self.label_exists(obj) == True:
            raise OtError("Label has to be unique")

        self.__labels.append(obj.name)

        return self.add(obj)
    
    def __get_asm(self) -> List[str]:
        """
            Returns the formatted asm
        """
        
        return list(map(str, self.get_store()))
    
    def dump_asm(self):
        """
            Dumping the assembly lines
        """
        
        print("\n".join(self.__get_asm()))
    
    def save_asm(self, path: str):
        """
            Dump the asm into `path`
        """
        
        with open(path, "w") as f:
            data = "\n".join(self.__get_asm())

            f.write(data)
