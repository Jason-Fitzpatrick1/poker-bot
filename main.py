import neat
import os
import pickle
import gzip
import threading
from flask import Flask, render_template

from .poker.suit import Suit
from .poker.card import Card
from .poker.hand import Hand
from .poker.deck import Deck
from .poker.game import Game
from .poker.player import Player

import logging

STARTING_BALANCE = 1000 # starting number of chips
STARTING_BLIND = 10 # starting big blind
BLIND_INCREASE = 0.2 # how much big blind increases
MAX_ROUNDS = 25 # max number of rounds in a game

app = Flask(__name__)

with gzip.open('neat-checkpoint-2') as f:
    generation, config, population, species_set, rndstate = pickle.load(f)
    bot1 = population[124]
    bot2 = population[99]
    bot3 = population[139]
    bot4 = population[140]
    bot5 = population[141]

players = [
    #Player(STARTING_BALANCE, "USER"),
    Player(STARTING_BALANCE, "AI", genome=bot1, config=config),
    Player(STARTING_BALANCE, "AI", genome=bot1, config=config),
    Player(STARTING_BALANCE, "AI", genome=bot2, config=config),
    Player(STARTING_BALANCE, "AI", genome=bot2, config=config),
    Player(STARTING_BALANCE, "AI", genome=bot3, config=config),
    Player(STARTING_BALANCE, "AI", genome=bot3, config=config),
    Player(STARTING_BALANCE, "AI", genome=bot4, config=config),
    Player(STARTING_BALANCE, "AI", genome=bot4, config=config),
    Player(STARTING_BALANCE, "AI", genome=bot5, config=config),
]

game = Game(players, STARTING_BLIND, BLIND_INCREASE, MAX_ROUNDS)

def get_updated_players_data():
    data = []
    for i, player in enumerate(game.players):
        data.append({
            "num": i+1,
            "balance": player.balance,
            "bet": player.current_bid,
            "action": player.prev_action.name,
            "card1": "poker_images/cards/face_down.png",
            "card2": "poker_images/cards/face_down.png"
        })
    return data

def get_updated_community_data():
    # player hands are their two community cards, then the community cards
    community_cards = [card for card in game.players[0].hand.cards[2:]]
    logging.error([f"{card.value}_OF_{card.suit.name}S" for card in game.players[0].hand.cards])
    data = {}
    for i, card in enumerate(community_cards):
        data[f"card{i}"] = f"poker_images/cards/{card.value}_OF_{card.suit.name}S.png"
    return data

def get_updated_pot_amount():
    return game.pot_amount

@app.route('/update_data')
def update_data():
    # Get updated data from your game backend
    # Update the following lines with your actual logic
    players = get_updated_players_data()
    community = get_updated_community_data()
    pot_amount = get_updated_pot_amount()

    updated_data = {
        'players': players,
        'community': community,
        'pot_amount': pot_amount
    }

    return updated_data

@app.route('/')
def index():
    #return render_template('index.html')
    players = get_updated_players_data()
    community = get_updated_community_data()
    pot_amount = get_updated_pot_amount()
    return render_template('index.html', players=players, community=community, pot_amount=pot_amount)

if __name__ == '__main__':
    t1 = threading.Thread(target=app.run, kwargs={'debug':False})
    t2 = threading.Thread(target=game.simulate)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    

