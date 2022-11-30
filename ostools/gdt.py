"""global descriptor table module"""

import uuid

from enum import Enum
from typing import Self
from typing import Any
from typing import Union

from .asm.asm import Assembly
from .asm.label import Label
from .asm.types import TypeByte
from .asm.types import TypeWord
from .asm.types import TypeDouble
from .asm.types import TypeValue
from .asm.types import TypeFormat

from .utils.bit import BitUtils

GDT_START = "gdt_start"
GDT_END = "gdt_end"
GDT_DESCRIPTOR = "gdt_descriptor"

class CpuPrivilevel(Enum):
    """
        Available CPU Privilege Level flags.
        
        bit 6-5 in the access byte
    """
    
    RING0 = ~0x60
    RING1 = 0x20
    RING2 = 0x40
    RING3 = 0x60
    
class GdtAccessByte:
    """
        Representing the access byte of a GDT entry
    """
    
    def __init__(self, value: int=0):
        self.__value = value
        
    def __call__(self, *args: Any, **kwds) -> Any:
        return self.__value
    
    def set_p(self, state: bool) -> Self:
        """
            Set the Present Bit at pos 7 in the access byte
            
            Allows an entry to refer to a valid segment.
            Must be set (1) for any valid segment.
        """
        
        self.__value = BitUtils.set_n_bit(
            self.__value,
            7,
            state
        )
        
        return self
    
    def set_dpl(self, permission: CpuPrivilevel) -> Self:
        """
            Set the Descriptor Privilege Level
            at pos 6-5 in the access byte
            
            Contains the CPU Privilege level of the segment.
            0 = highest privilege (kernel),
            3 = lowest privilege (user applications).
        """
        
        self.__value | permission.value
        
        return self
    
    def set_s(self, state: bool) -> Self:
        """
            Set the Descriptor type bit at pos 4
            in the access byte
            
            If clear (0) the descriptor defines a system segment
            (eg. a Task State Segment).
            If set (1) it defines a code or data segment.
        """
        
        self.__value = BitUtils.set_n_bit(
            self.__value,
            4,
            state
        )
        
        return self
        
    def set_e(self, state: bool) -> Self:
        """
            Set the Direction bit/Conforming bit at pos 3
            in the access byte
            
            Executable bit. If clear (0) the descriptor defines
            a data segment. If set (1) it defines a code segment
            which can be executed from.

        """
        
        self.__value = BitUtils.set_n_bit(
            self.__value,
            3,
            state
        )
        
        return self
        
    def set_dc(self, state: bool) -> Self:
        """
            Set the Direction bit / Conforming bit at pos 2
            in the access byte
            
            - For data selectors: Direction bit.
            If clear (0) the segment grows up.
            If set (1) the segment grows down, ie. the Offset has to
            be greater than the Limit.
            
            - For code selectors: Conforming bit.
                - If clear (0) code in this segment can only be executed
                from the ring set in DPL.
                
                - If set (1) code in this segment can be executed from
                an equal or lower privilege level. For example,
                code in ring 3 can far-jump to conforming code in a ring 2
                segment. The DPL field represent the highest privilege level
                that is allowed to execute the segment.
                For example, code in ring 0 cannot far-jump to a conforming
                code segment where DPL is 2, while code in ring 2 and 3 can.
                Note that the privilege level remains the same, ie. a far-jump
                from ring 3 to a segment with a DPL of 2 remains in ring 3
                after the jump.
        """
        
        self.__value = BitUtils.set_n_bit(
            self.__value,
            2,
            state
        )
        
        return self
        
    def set_rw(self, state: bool) -> Self:
        """
            Set the Readable bit / Writable bit in the access byte
            at pos 1

            - For code segments: Readable bit. If clear (0),
            read access for this segment is not allowed.
            If set (1) read access is allowed.
            Write access is never allowed for code segments.
            
            - For data segments: Writeable bit.
            If clear (0), write access for this segment is not allowed.
            If set (1) write access is allowed.
            Read access is always allowed for data segments.
        """
        
        self.__value = BitUtils.set_n_bit(
            self.__value,
            1,
            state
        )
        
        return self
        
    def set_a(self, state: bool) -> Self:
        """
            Set the Accessed bit at the pos 0 in the access byte
            
            Best left clear (0),
            the CPU will set it when the segment is accessed.
        """
        
        self.__value = BitUtils.set_n_bit(
            self.__value,
            0,
            state
        )
        
        return self

class GdtFlags:
    """
        Represents the GDT entry flags
    """
    
    def __init__(self):
        self.__value = 15 # 3-0 are set by default and unused
        
        self.set_g(True)
        self.set_db(True)
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.__value
    
    def set_g(self, state: bool) -> Self:
        """
            Granularity flag at the pos 3
            
            It indicates the size the Limit value is scaled by.
            If clear (0), the Limit is in 1 Byte blocks (byte granularity).
            If set (1), the Limit is in 4 KiB blocks (page granularity).
        """
        
        self.__value = BitUtils.set_n_bit(
            self.__value,
            7,
            state
        )
        
        return self
    
    def set_db(self, state: bool) -> Self:
        """
            Size flag at the pos 2
            
            If clear (0), the descriptor defines a 16-bit protected mode segment.
            If set (1) it defines a 32-bit protected mode segment.
            A GDT can have both 16-bit and 32-bit selectors at once.
        """
        
        self.__value = BitUtils.set_n_bit(
            self.__value,
            6,
            state
        )
        
        return self
    
    def set_l(self, state: bool) -> Self:
        """
            Long mode code flat at the pos 1
            
            If set (1), the descriptor defines a 64-bit code segment.
            When set, DB should always be clear.
            For any other type of segment (other code types or any data segment),
            it should be clear (0).
        """
        
        self.__value = BitUtils.set_n_bit(
            self.__value,
            5,
            state
        )
        
        return self

class GdtEntry(Label):
    """
        Represents an entry (aka a segment descriptor)
        for the GDT
    """
    
    def __init__(self, name: Union[str, None] = None):
        self.__segment_limit = 0xffff
        self.__base_0_15 = 0
        self.__base_16_23 = 0
        self.__access_byte = 0
        self.__flags = 0xcf
        self.__base_24_31 = 0
        
        if not name:
            name = str(uuid.uuid4())

        super().__init__(name)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.add(
            TypeWord(
                TypeValue(self.__segment_limit, TypeFormat.HEX)
                )
            )
        self.add(
            TypeWord(
                TypeValue(self.__base_0_15, TypeFormat.DEFAULT)
                )
            )
        self.add(
            TypeByte(
                TypeValue(self.__base_16_23, TypeFormat.DEFAULT)
                )
            )
        self.add(
            TypeByte(
                TypeValue(self.__access_byte, TypeFormat.HEX)
                )
            )
        self.add(
            TypeByte(
                TypeValue(self.__flags, TypeFormat.BIN)
                )
            )
        self.add(
            TypeByte(
                TypeValue(self.__base_24_31, TypeFormat.DEFAULT)
                )
            )

    def set_base(self, value: int):
        """
            Set the 32 bits linear address,
            where the segment begins
        """
        
        self.__base_0_15 = value & 0xffff
        self.__base_16_23 = (value >> 8) & 0xff
        self.__base_24_31 = (value >> 16) & 0xff
    
    def set_access_byte(self, value: GdtAccessByte) -> Self:
        """
            Apply the access byte
        """
        
        self.__access_byte = value()
        
        return self

    def set_flags(self, value: Union[GdtFlags, int]) -> Self:
        """
            Set the flags configuration
        """
        
        if type(value) == int:
            self.__flags = value
        else:
            self.__flags = value()
        
        return self

class Gdt(Assembly):
    """
        Representing the Global Descriptor Table
    """
    
    def __init__(self):
        super().__init__()
        
        self.add_label(Label(GDT_START))
        self.__add_null_entry()
        
    def __add_null_entry(self) -> Self:
        """
            Adding the first null entry
        """
        
        self.add_label(
            Label("gdt_null")
                .add(TypeDouble(
                    TypeValue(0, TypeFormat.HEX))
                )
                .add(TypeDouble(
                    TypeValue(0, TypeFormat.HEX))
                )
        )
        
        return self
    
    def add_entry(self, entry: GdtEntry) -> Self:
        """
            Add an entry toe the GDT
        """

        entry()
        self.add(entry)
        
        return self
    
    def add_end(self) -> Self:
        """
            Just adding a end label, it makes everything easier
        """
        
        self.add_label(Label(GDT_END))
        
        return self
    
    def add_descriptor(self) -> Self:
        """
            Add the GDT descriptor automatically
        """

        self.add_label(
            Label(GDT_DESCRIPTOR)
            .add(
                TypeWord(
                    TypeValue(f"{GDT_END} - {GDT_START} - 1", TypeFormat.DEFAULT)
                )
            )
            .add(
                TypeWord(
                    TypeValue(GDT_START, TypeFormat.DEFAULT)
                )
            )
        )
        
        return self
