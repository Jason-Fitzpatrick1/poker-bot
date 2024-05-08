from enum import Enum

'''
This class enumerates poker hand categories, 
where greater values are better hands
'''
class HandCategory(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    def __lt__(self, other):
        if isinstance(other, HandCategory):
            return self.value < other.value
        return NotImplemented
    
    def __gt__(self, other):
        if isinstance(other, HandCategory):
            return self.value > other.value
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, HandCategory):
            return self.value == other.value
        return NotImplemented