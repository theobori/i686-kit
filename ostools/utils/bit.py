"""Containing bit manipultion functions"""

from ..exceptions.exception import OtError

class BitUtils:
    """
        Containing static useful functions
    """
    
    def set_flag(value: int, flag: int) -> int:
        """
            Set a bit flag (`flag`) to `value`
        """
        
        return value | flag
    
    def unset_flag(value: int, flag: int) -> int:
        """
            Unset a bit flag (`flag`) to `value`
        """
        
        return value & ~flag
    
    def set_n_bit(value: int, n: int, state: bool) -> int:
        """
            Order: | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
        
            Set the bit at pos n to the state `state`
        """

        value_len = len(bin(value)[2:])
        value_len = int((value_len + 8) / 8) * 8
        
        if n >= value_len:
            raise OtError(
                "Bit position exceeds the value sizeof (bits)"
            )
        
        mask = 1 << n
        
        if not state:
            return BitUtils.unset_flag(value, mask)
        
        return BitUtils.set_flag(value, mask)
        