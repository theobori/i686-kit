"""mnemonic module"""

class BaseMnemonic:
    """
        Representing an assembly mnemonic
    """
    
    def __init__(self, dest: str, src: str):
        self.name = "base"
        self.dest = dest
        self.src = src
        
    def __str__(self) -> str:
        return f"{self.name} {self.dest}, {self.src}"
