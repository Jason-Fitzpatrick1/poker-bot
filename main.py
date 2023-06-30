import time
from poker.suit import Suit
from poker.card import Card
from poker.hand import Hand
from poker.deck import Deck

def eval_duration(hand: Hand, num_decks: int):
    start_time = time.time()
    print(hand.hand_strength(num_decks))
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken for {len(hand.cards)}-card hand with {num_decks} decks: {duration} seconds")

if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()

    hand1 = Hand([Card(14, Suit.CLUB), Card(14, Suit.HEART)])
    #eval_duration(hand1, 100)
    eval_duration(hand1, 1000)
    #eval_duration(hand1, 10000)

