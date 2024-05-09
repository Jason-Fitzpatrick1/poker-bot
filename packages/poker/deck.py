import random
from .card import Card
from .suit import Suit

'''
Class that represents a deck of cards. When initialized,
creates an ordered list of 52 unique cards
'''
class Deck():
    def __init__(self) -> None:
        self.cards = [Card(value, suit) for suit in Suit for value in range(2, 15)]
    def shuffle(self) -> None:
        random.shuffle(self.cards)
    def draw_card(self) -> Card:
        return self.cards.pop()
    def remove_card(self, card: Card) -> None:
        for deck_card in self.cards:
            if card.value == deck_card.value and card.suit == deck_card.suit:
                self.cards.remove(deck_card)
                return