import pickle
import gzip

from packages.poker.game import Game
from packages.poker.player import Player

import logging

'''
TODO:
- Replace print with logs
- Fix issue where players can infinitely go all-in and create test
- 
'''

STARTING_BALANCE = 1000 # starting number of chips
STARTING_BLIND = 10 # starting big blind
BLIND_INCREASE = 0.2 # how much big blind increases
MAX_ROUNDS = 25 # max number of rounds in a game
VERBOSE = True

# with gzip.open('neat-checkpoint-2') as f:
#     generation, config, population, species_set, rndstate = pickle.load(f)
#     bot1 = population[124]
#     bot2 = population[99]
#     bot3 = population[139]
#     bot4 = population[140]
#     bot5 = population[141]

players = [
    Player(STARTING_BALANCE, "USER"),
    Player(STARTING_BALANCE, "USER"),
    # Player(STARTING_BALANCE, "AI", genome=bot1, config=config),
    # Player(STARTING_BALANCE, "AI", genome=bot1, config=config),
    # Player(STARTING_BALANCE, "AI", genome=bot2, config=config),
    # Player(STARTING_BALANCE, "AI", genome=bot2, config=config),
    # Player(STARTING_BALANCE, "AI", genome=bot3, config=config),
    # Player(STARTING_BALANCE, "AI", genome=bot3, config=config),
    # Player(STARTING_BALANCE, "AI", genome=bot4, config=config),
    # Player(STARTING_BALANCE, "AI", genome=bot4, config=config),
    # Player(STARTING_BALANCE, "AI", genome=bot5, config=config),
]

game = Game(players, STARTING_BLIND, BLIND_INCREASE, MAX_ROUNDS)

if __name__ == '__main__':
    if VERBOSE:
        logging.basicConfig(
            level=logging.INFO,
            format='%(levelname)s - %(message)s'
        )
    game.simulate()
    

