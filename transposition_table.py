from bitboard import Bitboard
from typing import Optional, Union
from collections import OrderedDict

class TranspositionTable:
    """
    ### Parameters
        - size: `int` - The size of the cache. Defaults to 2^32.

    ### Explanation
    This is my implementation of a transpotion table to store previously explored Connect 4 positions. \n
    
    In initialisation, it takes in a size, which if left out, defaults to 2^32 or 4,294,967,296 spaces, which seems more than reasonable enough. \n
    
    It leverages the built-in `OrderedDict` found in the `collections` library to emulate LRU cache
    which ensures all of our inputs are removed when they're not needed, meaning the memory doesn't
    get bloated with old unaccessed positions. \n
    
    Given that a depth 5 search went through about 135,000 boards, a depth 10 search would be
    (as a crude guess) probably 324,135,000 board positions. This means the cache size of 2^32
    could store 13 separate searches at depth 10.


    ### Source:
        - [Solving LRU cache using OrderedDict](https://medium.com/@ireneziwang/solving-lru-cache-with-pythons-built-in-ordereddict-class-d76e0c82d3b6)
    """
    
    def __init__(self, size: int = 2**32):
        self.size = size 
        self.interal_cache = OrderedDict()
    
    def __len__(self) -> int:
        return len(self.interal_cache)

    def insert(self, bitboard: Bitboard, evaluation: Union[int, float]) -> None:
        """
        ### Explanation
        Inserts a key established from a Bitboard instance into the internal cache.

        ### Parameters
        - bitboard: `Bitboard` - the `Bitboard` instance.
        - evaluation: `Union[int, float]` - The evaluation from the given `Bitboard` instance.
        """

        key = bitboard.generate_key()

        if key in self.interal_cache:
            self.interal_cache[key] = evaluation
            self.interal_cache.move_to_end(key)
        else:
            if len(self.interal_cache) == self.size:
                self.interal_cache.popitem(last = False)
            
            self.interal_cache[key] = evaluation
    
    def get(self, bitboard: Bitboard) -> Optional[int]:
        """
        ### Explanation
        Gets the evaluation based on a given `Bitboard` instance.

        ### Parameters
        - bitboard: `Bitboard` - the `Bitboard` instance.

        ### Returns
        - `Optional[int]` - Either an `int` which represents the evaluation score or `None` if the value isn't found.
        """

        key = bitboard.generate_key()

        if key not in self.interal_cache:
            return
        
        self.interal_cache.move_to_end(key)
        return self.interal_cache[key]