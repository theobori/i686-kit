"""
%macro ISR 1
  global isr%1

  isr%1:
    cli
    push 0
    push %1
    jmp isr_common_stub
%endmacro

%macro ISR_ERROR 1
  global isr%1

  isr%1:
    cli
    push %1
    jmp isr_common_stub
%endmacro

%macro IRQ 2
  global irq%1

  irq%1:
    cli
    push %1; dummy error
    push %2 ; interrupt number
    jmp irq_common_stub
%endmacro
"""

ISR_ERRORs = (
    8,
    10,
    11,
    12,
    13,
    14,
    17,
    18,
    21
)

print("; Default ISR handlers")

for i in range(256):
    if i in ISR_ERRORs:
        print("ISR_ERROR", i)
    else:
        print("ISR", i)

print("; Default IRQ handlers")

for i in range(16):
    print("IRQ", i, i + 32)
