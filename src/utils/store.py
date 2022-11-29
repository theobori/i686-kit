"""store lines module"""

from typing import Any
from typing import Self
from typing import List

from ..exceptions.exception import I686Error

class BaseStore:
    """
        Storing objs that implements `__str__`
    """
    
    def __init__(self):
        self.__store = []
        
    def get_store(self) -> List[Any]:
        """
            Getter for `self.__store`
        """
        
        return self.__store
    
    def add(self, obj: Any) -> Self:
        """
            Add an element to `self.__store`
        """
        
        if hasattr(obj, "__str__"):
            self.__store.append(obj)
        else:
            raise I686Error("Not implementing __str__")
        
        return self
