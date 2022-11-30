"""psf module"""

from typing import List
from typing import Tuple
from typing import Self
from dataclasses import dataclass
from struct import unpack

from .exceptions.exception import OtError
from .asm.asm import Assembly
from .asm.label import Label
from .asm.types import TypeValue
from .asm.types import TypeByte
from .asm.types import TypeFormat

FONT_START = "font_start"

class PsfHeader:
    """
        Interface for the header classes
    """
    
    def __init__(self):
        raise OtError("Not implemented")
    
    def get_dimensions(self) -> Tuple[int, int]:
        """
            Return (w, h)
        """
        
        raise OtError("Not implemented")

    def get_length(self) -> int:
        """
            Returns glyphs amount        
        """
        
        raise OtError("Not implemented")

########
# PSF1 #
########

PSF1_MAGIC0     = 0x36
PSF1_MAGIC1     = 0x04
PSF1_MAGIC      = [
    PSF1_MAGIC0,
    PSF1_MAGIC1
]
PSF1_MAGIC_BYTES = bytes(PSF1_MAGIC)

PSF1_MODE512    = 0x01
PSF1_MODEHASTAB = 0x02
PSF1_MODEHASSEQ = 0x04
PSF1_MAXMODE    = 0x05

PSF1_SEPARATOR  = 0xFFFF
PSF1_STARTSEQ   = 0xFFFE

@dataclass
class Psf1Header(PsfHeader):
    """
        Representing a PSF1 header
    """
    
    # u8[2]
    magic: List[int]
    # u8
    mode: int
    # u8
    char_size: int
    
    def __str__(self) -> str:
        return "psf v1\nMode: {}: Character size: {}".format(
            self.mode,
            self.char_size
        )
    
    def __sizeof__(self) -> int:
        return 4
    
    def get_dimensions(self) -> Tuple[int, int]:        
        return (8, self.char_size)

    def get_length(self) -> int:
        return 256

########
# PSF2 #
########

PSF2_MAGIC0     = 0x72
PSF2_MAGIC1     = 0xb5
PSF2_MAGIC2     = 0x4a
PSF2_MAGIC3     = 0x86

PSF2_MAGIC      = [
    PSF2_MAGIC0,
    PSF2_MAGIC1,
    PSF2_MAGIC2,
    PSF2_MAGIC3
]

PSF2_MAGIC_BYTES = bytes(PSF2_MAGIC)

# Bits used in flags
PSF2_HAS_UNICODE_TABLE = 0x01

# Max version recognized so far
PSF2_MAXVERSION = 0

# UTF8 separators
PSF2_SEPARATOR  = 0xFF
PSF2_STARTSEQ   = 0xFE

@dataclass
class Psf2Header(PsfHeader):
    """
        Representing a PSF2 header
    """
    
    # u8[4]
    magic: List[int]
    # u32
    version: int
    # u32
    header_size: int
    # u32
    flags: int
    # u32
    length: int
    # u32
    char_size: int
    # u32
    height: int
    # u32
    width: int

    def __str__(self) -> str:
        return "psf v2\nCharacter size: {}\nDimensions: {}x{}".format(
            self.char_size,
            self.width,
            self.height
        )
    
    def __sizeof__(self) -> int:
        return 32

    def get_dimensions(self) -> Tuple[int, int]:
        """
            Return (w, h)
        """
        
        return (self.width, self.height)
    
    def get_length(self) -> int:
        return self.length

class Psf(Assembly):
    """
        Managing a Linux PC Screen Font
    """
    
    def __init__(self, filepath: str):
        super().__init__()
        
        with open(filepath, "rb") as f:
            self.__buffer = f.read()
        
        if len(self.__buffer) < 2:
            raise OtError("File content isnt enough long")
        
        if (magic := self.__buffer[:2]) == PSF1_MAGIC_BYTES:        
            self.header = Psf1Header(
                magic,
                self.__buffer[2],
                *list(unpack("BB", self.__buffer[2:4]))
            )
        elif (magic := self.__buffer[:4]) == PSF2_MAGIC_BYTES:
            self.header = Psf2Header(
                magic,
                *list(unpack("<iiiiiii", self.__buffer[4:32]))
            )
        else:
            raise OtError("Invalid file")

        self.offset = self.header.__sizeof__()
        self.glyphs_size = self.header.get_length() * self.header.char_size
    
    def dump_metadata(self):
        """
            Dump the file metadata
        """
        
        print(str(self.header))
    
    def get_char(self, index: int) -> bytes:
        """
            Unsafe

            Get char with an `index`
        """
        
        if index >= self.offset + self.glyphs_size:
            raise OtError("Index out of range")
        
        index += self.offset

        end = index + self.header.char_size

        return self.__buffer[index:end]
    
    def get_chars(self) -> bytes:
        """
            Get every chars as bytes
        """
        
        return self.__buffer[self.offset:self.offset + self.glyphs_size]

    def parse(self) -> Self:
        """
            Filling the assembly storage
        """

        # Avoid duplicates if multiples calls
        self.clear_store()
        self.add_label(Label(FONT_START))
        
        w, _ = self.header.get_dimensions()
        
        for i in range(0, self.glyphs_size, self.header.char_size):
            char = self.get_char(i)
            
            for ii in range(0, len(char), w // 8):
                line = char[ii:ii + (w // 8)]
                tv = lambda x: TypeValue(x, TypeFormat.BIN_FILL)

                line = list(map(tv, line))
                
                self.add(TypeByte(*line))
        
        return self