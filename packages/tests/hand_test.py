import unittest
from ..poker.hand import Hand
from ..poker.card import Card
from ..poker.suit import Suit
from ..poker.hand_category import HandCategory

class HandTestCase(unittest.TestCase):
    def test_add_card(self):
        hand = Hand()
        card = Card(value=2, suit=Suit.HEART)
        hand.add_card(card)
        self.assertIn(card, hand.cards)

    def test_evaluate_hand_royal_flush(self):
        cards = [
            Card(value=14, suit=Suit.HEART),
            Card(value=13, suit=Suit.HEART),
            Card(value=12, suit=Suit.HEART),
            Card(value=11, suit=Suit.HEART),
            Card(value=10, suit=Suit.HEART),
            Card(value=9, suit=Suit.DIAMOND),
            Card(value=8, suit=Suit.DIAMOND)
        ]
        hand = Hand(cards)
        category, values = hand.evaluate_hand()
        self.assertEqual(category, HandCategory.ROYAL_FLUSH)
        self.assertEqual(values, [14, 13, 12, 11, 10])
    
    def test_evaluate_hand_straight_flush(self):
        cards = [
            Card(value=9, suit=Suit.SPADE),
            Card(value=8, suit=Suit.SPADE),
            Card(value=7, suit=Suit.SPADE),
            Card(value=6, suit=Suit.SPADE),
            Card(value=5, suit=Suit.SPADE),
            Card(value=3, suit=Suit.HEART),
            Card(value=2, suit=Suit.HEART)
        ]
        hand = Hand(cards)
        category, values = hand.evaluate_hand()
        self.assertEqual(category, HandCategory.STRAIGHT_FLUSH)
        self.assertEqual(values, [9, 8, 7, 6, 5])
    
    def test_evaluate_hand_four_of_a_kind(self):
        cards = [
            Card(value=10, suit=Suit.CLUB),
            Card(value=10, suit=Suit.DIAMOND),
            Card(value=10, suit=Suit.HEART),
            Card(value=10, suit=Suit.SPADE),
            Card(value=6, suit=Suit.CLUB),
            Card(value=3, suit=Suit.SPADE),
            Card(value=2, suit=Suit.HEART)
        ]
        hand = Hand(cards)
        category, values = hand.evaluate_hand()
        self.assertEqual(category, HandCategory.FOUR_OF_A_KIND)
        self.assertEqual(values, [10, 6])

    def test_evaluate_hand_full_house(self):
        cards = [
            Card(value=7, suit=Suit.CLUB),
            Card(value=7, suit=Suit.DIAMOND),
            Card(value=7, suit=Suit.SPADE),
            Card(value=4, suit=Suit.HEART),
            Card(value=4, suit=Suit.SPADE),
            Card(value=4, suit=Suit.CLUB),
            Card(value=2, suit=Suit.CLUB)
        ]
        hand = Hand(cards)
        category, values = hand.evaluate_hand()
        self.assertEqual(category, HandCategory.FULL_HOUSE)
        self.assertEqual(values, [7, 4])
    
    def test_evaluate_hand_flush(self):
        cards = [
            Card(value=11, suit=Suit.DIAMOND),
            Card(value=9, suit=Suit.DIAMOND),
            Card(value=7, suit=Suit.DIAMOND),
            Card(value=6, suit=Suit.DIAMOND),
            Card(value=4, suit=Suit.DIAMOND),
            Card(value=3, suit=Suit.HEART),
            Card(value=2, suit=Suit.HEART)
        ]
        hand = Hand(cards)
        category, values = hand.evaluate_hand()
        self.assertEqual(category, HandCategory.FLUSH)
        self.assertEqual(values, [11, 9, 7, 6, 4])
    
    def test_evaluate_hand_straight(self):
        cards = [
            Card(value=9, suit=Suit.CLUB),
            Card(value=8, suit=Suit.DIAMOND),
            Card(value=7, suit=Suit.HEART),
            Card(value=6, suit=Suit.SPADE),
            Card(value=5, suit=Suit.CLUB),
            Card(value=3, suit=Suit.HEART),
            Card(value=2, suit=Suit.HEART)
        ]
        hand = Hand(cards)
        category, values = hand.evaluate_hand()
        self.assertEqual(category, HandCategory.STRAIGHT)
        self.assertEqual(values, [9, 8, 7, 6, 5])

    def test_evaluate_hand_three_of_a_kind(self):
        cards = [
            Card(value=7, suit=Suit.CLUB),
            Card(value=7, suit=Suit.DIAMOND),
            Card(value=7, suit=Suit.HEART),
            Card(value=5, suit=Suit.SPADE),
            Card(value=4, suit=Suit.CLUB),
            Card(value=3, suit=Suit.HEART),
            Card(value=2, suit=Suit.HEART)
        ]
        hand = Hand(cards)
        category, values = hand.evaluate_hand()
        self.assertEqual(category, HandCategory.THREE_OF_A_KIND)
        self.assertEqual(values, [7, 5, 4])

    def test_evaluate_hand_two_pair(self):
        cards = [
            Card(value=9, suit=Suit.CLUB),
            Card(value=9, suit=Suit.DIAMOND),
            Card(value=6, suit=Suit.HEART),
            Card(value=6, suit=Suit.SPADE),
            Card(value=4, suit=Suit.CLUB),
            Card(value=3, suit=Suit.HEART),
            Card(value=2, suit=Suit.HEART)
        ]
        hand = Hand(cards)
        category, values = hand.evaluate_hand()
        self.assertEqual(category, HandCategory.TWO_PAIR)
        self.assertEqual(values, [9, 6, 4])

    def test_evaluate_hand_one_pair(self):
        cards = [
            Card(value=8, suit=Suit.CLUB),
            Card(value=8, suit=Suit.DIAMOND),
            Card(value=7, suit=Suit.HEART),
            Card(value=5, suit=Suit.SPADE),
            Card(value=4, suit=Suit.CLUB),
            Card(value=3, suit=Suit.HEART),
            Card(value=2, suit=Suit.HEART)
        ]
        hand = Hand(cards)
        category, values = hand.evaluate_hand()
        self.assertEqual(category, HandCategory.ONE_PAIR)
        self.assertEqual(values, [8, 7, 5, 4])

    def test_evaluate_hand_high_card(self):
        cards = [
            Card(value=11, suit=Suit.CLUB),
            Card(value=9, suit=Suit.DIAMOND),
            Card(value=7, suit=Suit.HEART),
            Card(value=5, suit=Suit.SPADE),
            Card(value=3, suit=Suit.CLUB),
            Card(value=2, suit=Suit.HEART),
            Card(value=1, suit=Suit.HEART)
        ]
        hand = Hand(cards)
        category, values = hand.evaluate_hand()
        self.assertEqual(category, HandCategory.HIGH_CARD)
        self.assertEqual(values, [11, 9, 7, 5, 3])
    
    def test_hand_comparison(self):
        hand1 = Hand([
            Card(value=14, suit=Suit.HEART),
            Card(value=13, suit=Suit.HEART),
            Card(value=12, suit=Suit.HEART),
            Card(value=11, suit=Suit.HEART),
            Card(value=10, suit=Suit.HEART)
        ])
        hand2 = Hand([
            Card(value=10, suit=Suit.SPADE),
            Card(value=9, suit=Suit.SPADE),
            Card(value=8, suit=Suit.SPADE),
            Card(value=7, suit=Suit.SPADE),
            Card(value=6, suit=Suit.SPADE)
        ])
        self.assertGreater(hand1, hand2)

if __name__ == '__main__':
    unittest.main()
