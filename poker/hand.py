from multiprocessing import Pool
from .card import Card
from .deck import Deck
from .suit import Suit
from .hand_category import HandCategory
from typing import Tuple, List
from itertools import combinations
import random
'''
This class represents a hand in a poker game,
which includes community cards. The evalate_hand
method attempts to find the best {hand_size} cards
in the hand and categorize into a category defined by
the HandCategory enum. The Hand class has a built-in
comparator using the evaluate_hand method.
'''
class Hand():
    def __init__(self, cards: List[Card]=None) -> None:
        if cards:
            self.cards = cards
        else:
            self.cards = []


    '''
    Adds card to cards in hand
    '''
    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    '''
    Performs a Monte Carlo simulation. Takes in 
    a hand and a number of decks to randomly generate with the
    remaining cards. 
    Randomizes the deck and checks how many times the hand loses 
    against every possible opponent. This happens num_decks times.
    Uses multiprocessing to speed up simulation
    '''
    def hand_strength(self, num_decks: int) -> float:
        num_processes = 8
        iterations_per_process = num_decks // num_processes

        with Pool(num_processes) as pool:
            results = pool.map(self._run_simulation, [iterations_per_process] * num_processes)
        
        won_hands = sum(result[0] for result in results)
        tot_hands = sum(result[1] for result in results)

        return won_hands / tot_hands

    def _run_simulation(self, iterations: int) -> Tuple[int, int]:
        won_hands = 0
        tot_hands = 0

        for _ in range(iterations):
            starting_deck = Deck()
            for card in self.cards:
                starting_deck.remove_card(card)
            starting_deck.shuffle()

            temp_hand = Hand(self.cards[:])

            while len(temp_hand.cards) < 7:
                temp_hand.add_card(starting_deck.draw_card())

            opponent_hands = list(combinations(starting_deck.cards, 2))
            for opponent_hand in opponent_hands:
                temp_opponent_hand = Hand([opponent_hand[0], opponent_hand[1]])
                if temp_hand > temp_opponent_hand:
                    won_hands += 1
                tot_hands += 1

        return won_hands, tot_hands

    '''
    Classifies hand and returns highest value within category for 
    comparison purposes
    '''
    def evaluate_hand(self) -> Tuple[HandCategory, int]:
        hand_categories = [
            self._check_royal_flush,
            self._check_straight_flush,
            self._check_four_of_a_kind,
            self._check_full_house,
            self._check_flush,
            self._check_straight,
            self._check_three_of_a_kind,
            self._check_two_pair,
            self._check_one_pair,
            self._check_high_card
        ]
        
        for category in hand_categories:
            result, values = category()
            if result:
                return result, values

    def __gt__(self, other: 'Hand') -> bool:
        self_category, self_values = self.evaluate_hand()
        other_category, other_values = other.evaluate_hand()

        if self_category == other_category:
            for i in range(len(self_values)):
                if self_values[i] != other_values[i]:
                    return self_values[i] > other_values[i]
        else:
            return self_category > other_category
    
    def __lt__(self, other: 'Hand') -> bool:
        self_category, self_values = self.evaluate_hand()
        other_category, other_values = other.evaluate_hand()

        if self_category == other_category:
            for i in range(len(self_values)):
                if self_values[i] != other_values[i]:
                    return self_values[i] < other_values[i]
        else:
            return self_category < other_category
    
    def __eq__(self, other: 'Hand') -> bool:
        self_category, self_values = self.evaluate_hand()
        other_category, other_values = other.evaluate_hand()

        return self_category == other_category and self_values == other_values
    
    def __ge__(self, other: 'Hand') -> bool:
        return not self < other
    
    def __le__(self, other: 'Hand') -> bool:
        return not self > other
    
    def __ne__(self, other: 'Hand') -> bool:
        return not self == other
    
    def _check_royal_flush(self) -> Tuple[str, List[int]]:
        royal_values = [14, 13, 12, 11, 10]
        suits = [Suit.CLUB, Suit.DIAMOND, Suit.HEART, Suit.SPADE]
        for suit in suits:
            suit_cards = [card for card in self.cards if card.suit == suit]
            if len(suit_cards) >= 5:
                values = sorted([card.value for card in suit_cards], reverse=True)
                if values[:5] == royal_values:
                    return HandCategory.ROYAL_FLUSH, royal_values
        return None, None
    
    def _check_straight_flush(self) -> Tuple[str, List[int]]:
        suits = [Suit.CLUB, Suit.DIAMOND, Suit.HEART, Suit.SPADE]
        for suit in suits:
            suit_cards = [card for card in self.cards if card.suit == suit]
            if len(suit_cards) >= 5:
                values = sorted([card.value for card in suit_cards], reverse=True) 
                for i in range(len(values) - 5):
                    if self._is_consecutive(values[i:5+i]):
                        return HandCategory.STRAIGHT_FLUSH, values[:5]
                    elif values[0] == 14 and self._is_low_straight(values):
                        return HandCategory.STRAIGHT_FLUSH, [5, 4, 3, 2, 1]
        return None, None
    
    def _check_four_of_a_kind(self) -> Tuple[str, List[int]]:
        for value in range(2, 15):
            value_cards = [card for card in self.cards if card.value == value]
            non_value_cards = sorted([card for card in self.cards if card.value != value], key=lambda c: c.value, reverse=True)
            if len(value_cards) >= 4:
                return HandCategory.FOUR_OF_A_KIND, [value, non_value_cards[0]]
        return None, None
    
    def _check_full_house(self) -> Tuple[str, List[int]]:
        three_of_a_kind = self._check_three_of_a_kind()
        if three_of_a_kind[0]:
            remaining_cards = [card for card in self.cards if card.value != three_of_a_kind[0]]
            temp_cards = self.cards
            self.cards = remaining_cards
            pair = self._check_one_pair()
            self.cards = temp_cards
            if pair[0]:
                return HandCategory.FULL_HOUSE, [three_of_a_kind[0], pair[0]]
        return None, None
    
    def _check_flush(self) -> Tuple[str, List[int]]:
        suits = [Suit.CLUB, Suit.DIAMOND, Suit.HEART, Suit.SPADE]
        for suit in suits:
            suit_cards = [card for card in self.cards if card.suit == suit]
            if len(suit_cards) >= 5:
                values = sorted([card.value for card in suit_cards], reverse=True)
                return HandCategory.FLUSH, values[:5]
        return None, None
    
    def _check_straight(self) -> Tuple[str, List[int]]:
        values = sorted([card.value for card in self.cards], reverse=True)
        for i in range(len(self.cards) - 5):
            if self._is_consecutive(values[i:5+i]):
                return HandCategory.STRAIGHT, values[:5]
            elif values[0] == 14 and self._is_low_straight(values):
                return HandCategory.STRAIGHT, [5, 4, 3, 2, 1]
        return None, None
    
    def _check_three_of_a_kind(self) -> Tuple[str, List[int]]:
        for value in range(2, 15):
            value_cards = [card for card in self.cards if card.value == value]
            remaining_cards = [card for card in self.cards if card.value != value]
            if len(value_cards) >= 3:
                return HandCategory.THREE_OF_A_KIND, [value, remaining_cards[0], remaining_cards[1]]
        return None, None
    
    def _check_two_pair(self) -> Tuple[str, List[int]]:
        pair1 = self._check_one_pair()
        if pair1[0]:
            remaining_cards = [card for card in self.cards if card.value != pair1[1][0]]
            temp_cards = self.cards
            self.cards = remaining_cards
            pair2 = self._check_one_pair()
            self.cards = temp_cards
            if pair2[0] and pair2[1] != pair1[1]:
                self.cards = temp_cards
                return HandCategory.TWO_PAIR, [max(pair1[1][0], pair2[1][0]), min(pair1[1][0], pair2[1][0]), pair2[1][1]]
            self.cards = temp_cards
        return None, None
    
    def _check_one_pair(self) -> Tuple[str, List[int]]:
        for value in range(2, 15):
            value_cards = [card for card in self.cards if card.value == value]
            remaining_cards = sorted([card for card in self.cards if card.value != value], key=lambda c: c.value, reverse=True)
            if len(value_cards) >= 2:
                return HandCategory.ONE_PAIR, remaining_cards[:3]
        return None, None
    
    def _check_high_card(self) -> Tuple[str, List[int]]:
        values = sorted([card.value for card in self.cards], reverse=True)
        return HandCategory.HIGH_CARD, values[:5]
    
    def _is_low_straight(self, values: List[int]) -> bool:
        low_straight = [14, 2, 3, 4, 5]
        if set(low_straight).issubset(values):
            return True
        return False
    
    def _is_consecutive(self, values) -> List[int]:
        return all(values[i] == values[i+1] + 1 for i in range(len(values)-1))
