SETTER = "set_idt_gate(%d, %s, KERNEL_CODE_SEG, IDT_FLAG_RING0 | IDT_FLAG_GATE_32BIT_INT);"
IRQ_NUMBERS = tuple(range(32, 47 + 1))

for i in range(256):
    if i in IRQ_NUMBERS:
        print(SETTER % (i, f"irq{i % 32}"))
    else:
        print(SETTER % (i, f"isr{i}"))
