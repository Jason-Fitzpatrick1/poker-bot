import time
from .poker.suit import Suit
from .poker.card import Card
from .poker.hand import Hand
from .poker.deck import Deck

def eval_duration(hand: Hand, num_decks: int) -> float:
    start_time = time.time()
    hand_str = hand.hand_strength(num_decks)
    print(hand_str)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken for {len(hand.cards)}-card hand with {num_decks} decks: {duration} seconds")
    return hand_str

if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()

    hand1 = Hand([Card(14, Suit.CLUB), Card(14, Suit.HEART)]) # should be ~86.4%
    vals = []
    for _ in range(50):
        vals.append(eval_duration(hand1, 50))
    print("######")
    print(f"Range: {min(vals)}-{max(vals)}")
    #eval_duration(hand1, 1000)
    #eval_duration(hand1, 10000)

