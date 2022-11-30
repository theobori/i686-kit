for i in range(256):
    print(f"extern void isr{i}();")
    
for i in range(16):
    print(f"extern void irq{i}();")
