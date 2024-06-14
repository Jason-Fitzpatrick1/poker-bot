import csv
from itertools import combinations_with_replacement
from .suit import Suit
from .card import Card
from .hand import Hand

NUM_SIMS = 100

# Generate all unique starting value combinations
values = range(2,15)
value_combinations = combinations_with_replacement(values, 2)

results = []

for v1, v2 in value_combinations:
    card1_diamond = Card(value=v1, suit=Suit.DIAMOND)
    card1_heart = Card(value=v1, suit=Suit.HEART)
    card2_heart = Card(value=v2, suit=Suit.HEART)

    unsuited_hand = Hand(cards=[card1_diamond, card2_heart])
    unsuited_strength = unsuited_hand.hand_strength(num_decks=NUM_SIMS)

    suited_hand = Hand(cards=[card1_heart, card2_heart])
    suited_strength = suited_hand.hand_strength(num_decks=NUM_SIMS)
    print([f"{v1},{v2}", unsuited_strength, suited_strength])
    results.append([f"{v1},{v2}", unsuited_strength, suited_strength])

with open('starting_hand_strengths.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['hand', 'unsuited', 'suited'])
    for row in results:
        csvwriter.writerow(row)


print("Hand strengths have been calculated and exported to hand_strengths.csv.")