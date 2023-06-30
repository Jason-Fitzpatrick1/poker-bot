import neat
from neat import DefaultGenome, Config
from .hand import Hand
from .player_actions import PlayerActions
class Player():
    def __init__(self, starting_balance: int, hand: Hand, genome: DefaultGenome, config: Config) -> None:
        self.balance = starting_balance
        self.hand = hand
        self.genome = genome
        self.config = config
        self.folded = False
        self.round_bid = 0
        self.current_bid = 0
        self.is_all_in = False
    
    '''
    Returns a PlayerAction and a raise amount based on the output of 
    the neural network. Raise amount is returned every time as a percentage of the
    total stack of the player.
    '''
    def action(self) -> tuple[PlayerActions, int]:
        network = neat.nn.FeedForwardNetwork.create(self.genome, self.config)
        decision = network.activate()        
        return PlayerActions(decision.index(max(decision[:-1]))), decision[-1]
    
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
