import neat
from neat import DefaultGenome, Config
from .hand import Hand
from .player_actions import PlayerActions
from typing import Tuple

class Player():
    def __init__(self, starting_balance: int, player_type: str, hand: Hand=Hand(), num_hand_sims: int=5, genome: DefaultGenome=None, config: Config=None) -> None:
        self.balance = starting_balance
        self.player_type = player_type.upper()
        self.hand = hand
        self.num_hand_sims = num_hand_sims
        self.genome = genome
        if genome and config:
            self.net = neat.nn.RecurrentNetwork.create(genome, config)
        self.config = config
        self.folded = False
        self.round_bid = 0
        self.current_bid = 0
        self.is_all_in = False
        self.is_out = False
        self.prev_action = PlayerActions.NO_ACTION

        if self.player_type not in  ["AI", "USER"]:
            raise Exception("Invalid Player Type")
        elif self.player_type == "AI" and (self.genome == None or self.config == None):
            raise Exception("AI player type requires genome and config inputs")
    
    def action(self, pot_amount: int, opp1: PlayerActions, opp2: PlayerActions, opp3: PlayerActions, opp4: PlayerActions, opp5: PlayerActions, opp6: PlayerActions, opp7: PlayerActions, opp8: PlayerActions, opp9: PlayerActions) -> Tuple[PlayerActions, int]:
        '''
        Returns a PlayerAction and a raise amount based on the output of 
        the neural network. Raise amount is returned every time.
        '''
        decision = self.net.activate((self.hand.hand_strength(self.num_hand_sims), self.balance, self.round_bid, self.prev_action.value,
                                    pot_amount, opp1.value, opp2.value, opp3.value, opp4.value, opp5.value, opp6.value, opp7.value,
                                    opp8.value, opp9.value))
        self.prev_action = PlayerActions(decision.index(max(decision[1:])))
        return self.prev_action, decision[-1]
    
    def get_action_from_user(self) -> Tuple[PlayerActions, int]:
        action = int(input("Do you want to check (1), call (2), raise (3), go all-in (4), or fold (5)? (int): "))
        raise_amount = 0
        if action == 3:
            raise_amount = int(input("How much do you want to raise? (int): "))
        return PlayerActions(action), raise_amount
    
    def deduct_balance(self, amount: int):
        self.balance -= amount

    def increase_balance(self, amount: int):
        self.balance += amount

    def fold(self):
        self.folded = True

    def check(self, highest_bid: int):
        if highest_bid > self.round_bid:
            self.fold()

    def call(self, highest_bid: int, pot_size: int) -> int:
        amount_to_call = highest_bid - self.round_bid
        if amount_to_call > self.balance:
            return self.all_in(pot_size)
        else:
            self.balance -= amount_to_call
            self.current_bid += amount_to_call
            self.round_bid += amount_to_call
            return amount_to_call
    def raise_bid(self, blind: int, highest_bid: int, raise_amount:int, pot_size: int) -> int:
        if blind > raise_amount:
            raise_amount = blind
        if raise_amount > self.balance or (highest_bid - self.round_bid) > self.balance:
            return self.all_in(pot_size)
        else:
            bet = highest_bid - self.round_bid + raise_amount
            self.balance -= bet
            self.current_bid += bet
            self.round_bid += bet
            return raise_amount
        
    def all_in(self, pot_size: int) -> int:
        temp_balance = self.balance
        self.balance = 0
        self.all_in_amount = pot_size + temp_balance
        self.current_bid += temp_balance
        self.round_bid += temp_balance
        return temp_balance

    def update_fitness(self) -> None:
        self.genome.fitness = self.balance