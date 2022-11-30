"""assembly types modules"""

from enum import Enum
from typing import List, Union

from ..exceptions.exception import OtError

class TypeFormat(Enum):
    """
        Availables format for the assembly types
    """

    DEFAULT = 0
    HEX = 1
    BIN = 2
    BIN_FILL = 3
    CHAR = 4

class TypeValue:
    """
        Representing a type value with a linked format
    """
    
    def __init__(self, value: Union[int, str], __format: TypeFormat):
        self.value = value
        self.__format = __format
        
    def __int_to_str(self) -> str:
        """
            If `self.value` has type int
        """
        
        match self.__format:
            case TypeFormat.DEFAULT:
                return str(self.value)
            case TypeFormat.HEX:
                return hex(self.value)
            case TypeFormat.BIN:
                return bin(self.value)[2:] + "b"
            case TypeFormat.BIN_FILL:
                binary = bin(self.value)[2:]
                fill = "0" * (8 - len(binary))
                
                return fill + binary + "b"
            case TypeFormat.CHAR:
                if self.value <= 0xff:
                    return chr(self.value)
                else:
                    raise OtError("Overflow")
            case _:
                raise OtError("Invalid format")
    
    def __str__(self) -> str:
        if type(self.value) == str:
            return self.value

        return self.__int_to_str()

class BaseType:
    """
        Representing an assembly type (db, dw, etc..)
    """
    
    def __init__(self, _type: str, *args: List[TypeValue]):
        self.args = args
        self.type = _type
    
    def __str__(self) -> str:
        values = ",".join(str(value) for value in self.args)

        return f"{self.type} {values}"

class TypeByte(BaseType):
    """
        Represents a byte
    """

    def __init__(self, *args: List[TypeValue]):
        super().__init__("db", *args)

class TypeWord(BaseType):
    """
        Represents a word
    """

    def __init__(self, *args: List[TypeValue]):
        super().__init__("dw", *args)

class TypeDouble(BaseType):
    """
        Represents a double
    """

    def __init__(self, *args: List[TypeValue]):
        super().__init__("dd", *args)
