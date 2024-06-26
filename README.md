# i686 toolkit

## How to build and run ?

1. Install the dependencies 
   - Python >=3.11.0
2. You can just run the scripts in `scripts/`.
3. You can use install the Python module.

```bash
python setup.py install
```

## Usage example

#### Build and dump/save a GDT
```python
from ostools.gdt import Gdt
from ostools.gdt import GdtEntry
from ostools.gdt import GdtAccessByte
from ostools.gdt import GdtFlags
from ostools.gdt import CpuPrivilevel

a = Gdt() \
.add_entry(
    GdtEntry("gdt_code")
    .set_access_byte(
        GdtAccessByte(0x9a)
    )
    .set_flags(GdtFlags())
) \
.add_entry( 
    GdtEntry("gdt_data")
    .set_access_byte(
        GdtAccessByte()
            .set_p(True)
            .set_dpl(CpuPrivilevel.RING0)
            .set_s(True)
            .set_rw(True)
    )
    .set_flags(0xcf)
) \
.add_end() \
.add_descriptor() \
.dump_asm() # or .save_asm("test.asm")
```

#### Convert a Linux PC Screen Font to x86 assembly data

```python
from ostools.psf import Psf

a = Psf("ter-v32n.psf") \
.parse() \
.save_asm("test.asm")
```

## Scripts

The directory `scripts/` contains scripts intended to do metaprogramming. Most of them concern the 32 bits interrupts.
