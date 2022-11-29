"""x86 assembly module"""

from typing import Self

from .label import Label
from ..utils.store import BaseStore

from ..exceptions.exception import I686Error

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
            raise I686Error("Label has to be unique")

        self.__labels.append(obj.name)

        return self.add(obj)
    
    def dump_asm(self):
        """
            Dumping the assembly lines
        """
        
        formatted = list(map(str, self.get_store()))
        
        print("\n".join(formatted))
