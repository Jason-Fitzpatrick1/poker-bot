import multiprocessing
import os
import pickle
import random
import neat

from ..poker.player import Player
from ..poker.hand import Hand
from ..poker.game import Game

GAME_SIZE = 10 # number of players in a game
STARTING_BALANCE = 1000 # starting number of chips
STARTING_BLIND = 10 # starting big blind
BLIND_INCREASE = 0.2 # how much big blind increases
MAX_ROUNDS = 25 # max number of rounds in a game
NUM_GENERATIONS = 100 # number of generations to train
NUM_HAND_SIMS = 50 # number of randomized decks in Monte Carlo

def eval_genomes(genomes, config) -> None:
    random.shuffle(genomes)
    for i in range(0, len(genomes), GAME_SIZE):
        if i+GAME_SIZE >= len(genomes):
            genome_sublist = genomes[i:]
        else:
            genome_sublist = genomes[i:i+GAME_SIZE]
        players = []
        for (genome_id, genome) in genome_sublist:
            player = Player(STARTING_BALANCE, Hand(), NUM_HAND_SIMS, genome, config)
            players.append(player)
        game = Game(players, STARTING_BLIND, BLIND_INCREASE, MAX_ROUNDS)
        game.simulate()
        for player in players:
            player.update_fitness()


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(neat.Checkpointer(10))
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    #pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genomes)
    #winner = pop.run(pe.evaluate, NUM_GENERATIONS)
    winner = pop.run(eval_genomes, NUM_GENERATIONS)

    # Save the winner.
    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)

if __name__ == '__main__':
    run()