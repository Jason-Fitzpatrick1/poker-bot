from multiprocessing import Pool
import multiprocessing
from .card import Card
from .deck import Deck
from .suit import Suit
from .hand_category import HandCategory
from typing import Tuple, List
from itertools import combinations
import copy
import random

class Hand():
    def __init__(self, cards: List[Card]=None) -> None:
        if cards:
            self.cards = cards
        else:
            self.cards = []

    def __str__(self) -> str:
        if not self.cards:
            return "Empty hand"
        else:
            return "Cards in hand:\n" + "\n".join(str(card) for card in self.cards)

    def add_card(self, card: Card) -> None:
        '''
        Adds card to cards in hand

        Args:
            card (Card): A playing card object to go into a hand of cards

        Returns:
            None
        '''
        self.cards.append(card)
    
    def clear(self) -> None:
        '''
        Resets hand to empty list of Cards

        Returns:
            None
        '''
        self.cards = []

    def hand_strength(self, num_decks: int) -> float:
        '''
        Performs a Monte Carlo simulation to calculate the hand strength.

        Args:
            num_decks (int): The number of decks to randomly generate with the remaining cards.
            
        Returns:
            float: The calculated hand strength.
        '''
        num_processes = multiprocessing.cpu_count()

        with Pool(num_processes) as pool:
            results = pool.map(self._run_simulation, [num_decks] * num_processes)
        
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

            temp_hand = Hand(copy.deepcopy(self.cards))

            while len(temp_hand.cards) < 7:
                temp_hand.add_card(starting_deck.draw_card())

            opponent_hands = list(combinations(starting_deck.cards, 2))
            for opponent_hand in opponent_hands:
                temp_opponent_hand = Hand([opponent_hand[0], opponent_hand[1]])
                for c in temp_hand.cards[2:]:
                    temp_opponent_hand.add_card(c)
                counter = 0
                while len(temp_hand.cards) < 7:
                    if starting_deck.cards[counter] not in temp_hand.cards:
                        temp_hand.add_card(starting_deck.cards[counter])
                    counter += 1
                if temp_hand > temp_opponent_hand:
                    won_hands += 1
                tot_hands += 1
        return won_hands, tot_hands

    def evaluate_hand(self) -> Tuple[HandCategory, int]:
        '''
        Classifies the hand and returns the highest value within the category for comparison purposes.

        Returns:
            Tuple[HandCategory, int]: The hand category and the highest value within that category.
        '''
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
        """
        Compares if this hand is greater than the other hand.
        
        Args:
            other (Hand): The other hand to compare with.
            
        Returns:
            bool: True if this hand is greater than the other hand, False otherwise.
        """
        self_category, self_values = self.evaluate_hand()
        other_category, other_values = other.evaluate_hand()

        if self_category == other_category:
            for i in range(len(self_values)):
                if self_values[i] != other_values[i]:
                    return self_values[i] > other_values[i]
        else:
            return self_category > other_category
    
    def __lt__(self, other: 'Hand') -> bool:
        """
        Compares if this hand is less than the other hand.
        
        Args:
            other (Hand): The other hand to compare with.
            
        Returns:
            bool: True if this hand is less than the other hand, False otherwise.
        """
        self_category, self_values = self.evaluate_hand()
        other_category, other_values = other.evaluate_hand()

        if self_category == other_category:
            for i in range(len(self_values)):
                if self_values[i] != other_values[i]:
                    return self_values[i] < other_values[i]
        else:
            return self_category < other_category
    
    def __eq__(self, other: 'Hand') -> bool:
        """
        Compares if this hand is equal to the other hand.
        
        Args:
            other (Hand): The other hand to compare with.
            
        Returns:
            bool: True if this hand is equal to the other hand, False otherwise.
        """
        self_category, self_values = self.evaluate_hand()
        other_category, other_values = other.evaluate_hand()

        return self_category == other_category and self_values == other_values
    
    def __ge__(self, other: 'Hand') -> bool:
        """
        Compares if this hand is greater than or equal to the other hand.
        
        Args:
            other (Hand): The other hand to compare with.
            
        Returns:
            bool: True if this hand is greater than or equal to the other hand, False otherwise.
        """
        return not self < other
    
    def __le__(self, other: 'Hand') -> bool:
        """
        Compares if this hand is less than or equal to the other hand.
        
        Args:
            other (Hand): The other hand to compare with.
            
        Returns:
            bool: True if this hand is less than or equal to the other hand, False otherwise.
        """
        return not self > other
    
    def __ne__(self, other: 'Hand') -> bool:
        """
        Compares if this hand is not equal to the other hand.
        
        Args:
            other (Hand): The other hand to compare with.
            
        Returns:
            bool: True if this hand is not equal to the other hand, False otherwise.
        """
        return not self == other
    
    def _check_royal_flush(self) -> Tuple[HandCategory, List[int]]:
        royal_values = [14, 13, 12, 11, 10]
        suits = [Suit.CLUB, Suit.DIAMOND, Suit.HEART, Suit.SPADE]
        for suit in suits:
            suit_cards = [card for card in self.cards if card.suit == suit]
            if len(suit_cards) >= 5:
                values = sorted([card.value for card in suit_cards], reverse=True)
                if values[:5] == royal_values:
                    return HandCategory.ROYAL_FLUSH, royal_values
        return None, None
    
    def _check_straight_flush(self) -> Tuple[HandCategory, List[int]]:
        suits = [Suit.CLUB, Suit.DIAMOND, Suit.HEART, Suit.SPADE]
        for suit in suits:
            suit_cards = [card for card in self.cards if card.suit == suit]
            if len(suit_cards) >= 5:
                temp_cards = self.cards
                self.cards = suit_cards
                straight = self._check_straight()
                self.cards = temp_cards
                if straight[0]:
                    return HandCategory.STRAIGHT_FLUSH, straight[1]

        return None, None
    
    def _check_four_of_a_kind(self) -> Tuple[HandCategory, List[int]]:
        for value in range(2, 15):
            value_cards = [card for card in self.cards if card.value == value]
            non_value_cards = sorted([card.value for card in self.cards if card.value != value], reverse=True)
            if len(value_cards) >= 4:
                return HandCategory.FOUR_OF_A_KIND, [value, non_value_cards[0]]
        return None, None
    
    def _check_full_house(self) -> Tuple[HandCategory, List[int]]:
        three_of_a_kind = self._check_three_of_a_kind()
        if three_of_a_kind[0]:
            remaining_cards = [card for card in self.cards if card.value != three_of_a_kind[1][0]]
            temp_cards = self.cards
            self.cards = remaining_cards
            other_three_of_a_kind = self._check_three_of_a_kind() # there could be a higher 3 of a kind
            pair = self._check_one_pair()
            self.cards = temp_cards
            if other_three_of_a_kind[0]:
                return HandCategory.FULL_HOUSE, [max(three_of_a_kind[1][0], other_three_of_a_kind[1][0]), min(three_of_a_kind[1][0], other_three_of_a_kind[1][0])]
            elif pair[0]:
                return HandCategory.FULL_HOUSE, [three_of_a_kind[1][0], pair[1][0]]
        return None, None
    
    def _check_flush(self) -> Tuple[HandCategory, List[int]]:
        suits = [Suit.CLUB, Suit.DIAMOND, Suit.HEART, Suit.SPADE]
        for suit in suits:
            suit_cards = [card for card in self.cards if card.suit == suit]
            if len(suit_cards) >= 5:
                values = sorted([card.value for card in suit_cards], reverse=True)
                return HandCategory.FLUSH, values[:5]
        return None, None
    
    def _check_straight(self) -> Tuple[HandCategory, List[int]]:
        values = sorted([card.value for card in self.cards], reverse=True)
        if len(values) == 5:
            if self._is_consecutive(values):
                return HandCategory.STRAIGHT, values
            elif values[0] == 14 and self._is_low_straight(values):
                return HandCategory.STRAIGHT, [5, 4, 3, 2, 1]
        else:
            for i in range(len(values) - 5):
                if self._is_consecutive(values[i:5+i]):
                    return HandCategory.STRAIGHT, values[:5]
                elif values[0] == 14 and self._is_low_straight(values):
                    return HandCategory.STRAIGHT, [5, 4, 3, 2, 1]
        return None, None
    
    def _check_three_of_a_kind(self) -> Tuple[HandCategory, List[int]]:
        for value in range(2, 15):
            value_cards = [card for card in self.cards if card.value == value]
            remaining_cards = sorted([card.value for card in self.cards if card.value != value], reverse=True)
            if len(value_cards) >= 3:
                if len(remaining_cards) < 2:
                    remaining_cards.extend([0] * (2 - len(remaining_cards)))
                return HandCategory.THREE_OF_A_KIND, [value, remaining_cards[0], remaining_cards[1]]
        return None, None
    
    def _check_two_pair(self) -> Tuple[HandCategory, List[int]]:
        pair1 = self._check_one_pair()
        if pair1[0]:
            remaining_cards = [card for card in self.cards if card.value != pair1[1][0]]
            temp_cards = self.cards
            self.cards = remaining_cards
            pair2 = self._check_one_pair()
            self.cards = temp_cards
            if pair2[0]:
                self.cards = temp_cards
                return HandCategory.TWO_PAIR, [max(pair1[1][0], pair2[1][0]), min(pair1[1][0], pair2[1][0]), pair2[1][1]]
            self.cards = temp_cards
        return None, None
    
    def _check_one_pair(self) -> Tuple[HandCategory, List[int]]:
        for value in range(2, 15):
            value_cards = [card for card in self.cards if card.value == value]
            remaining_cards = sorted([card.value for card in self.cards if card.value != value], reverse=True)
            if len(value_cards) >= 2:
                if len(remaining_cards) < 3:
                    remaining_cards.extend([0] * (3 - len(remaining_cards)))
                return HandCategory.ONE_PAIR, [value, remaining_cards[0], remaining_cards[1], remaining_cards[2]]
        return None, None
    
    def _check_high_card(self) -> Tuple[HandCategory, List[int]]:
        values = sorted([card.value for card in self.cards], reverse=True)
        if len(values) < 5:
            values.extend([0] * (5 - len(values)))
        return HandCategory.HIGH_CARD, values[:5]
    
    def _is_low_straight(self, values: List[int]) -> bool:
        low_straight = [14, 2, 3, 4, 5]
        if set(low_straight).issubset(values):
            return True
        return False
    
    def _is_consecutive(self, values) -> List[int]:
        return all(values[i] == values[i+1] + 1 for i in range(len(values)-1))
