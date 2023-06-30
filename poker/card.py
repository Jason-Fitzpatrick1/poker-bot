from .suit import Suit

'''
This class represents a playing card with value between 1 and 14,
where Ace is a high 14, excpet in a low straight, in which an ace
can be a 1. Each card is assigned a Suit
'''
class Card():
    def __init__(self, value: int, suit: Suit) -> None:
        self.value = self._is_valid_value(value)
        self.suit = suit
    
    def _is_valid_value(self, value: int) -> int:
        if (value < 1 or value >14):
            raise ValueError("Card value must be between 1 and 14")
        return value
    