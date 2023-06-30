from .deck import Deck
from .player import Player
from .player_actions import PlayerActions
from typing import List

class Game():
    def __init__(self, players: List[Player], starting_balance: int, starting_blind: int, blind_increase: float, max_rounds: int) -> None:
        self.players = players
        self.deck = Deck()
        self.starting_balance = starting_balance
        self.blind = starting_blind
        self.blind_increase = blind_increase
        self.max_rounds = max_rounds
        self.pot_amount = 0
        self.first_turn = 0
        self.highest_bid = self.blind
        self.rounds_complete = 0
        self.last_bidder = len(self.players) -1
        self.current_player = 0

    def simulate(self) -> None:
        while not self.check_winner() and self.rounds_complete < self.max_rounds:
            self.deck = Deck()
            self.deck.shuffle()
            self.deal()

            for i in range(3):
                if self.check_hand_winner():
                    break
                self.round()
                self.show_next_cards(i)
            
            self.reset_round() # reset pot, folded players, highest bid, current player
            self.move_blinds()
            self.check_blinds_raise()

            self.rounds_complete += 1
    
    def round(self) -> None:
        self.current_player = self.first_turn
        self.highest_bid = self.blind
        self.players[self.first_turn - 1].deduct_balance(self.blind)
        self.players[self.first_turn - 2].deduct_balance(self.blind // 2)
        self.pot_amount = self.blind + self.blind // 2
        while self.current_player != self.last_bidder:
            if not self.players[self.current_player].folded:
                action, raise_amount = self.players[self.current_player].action()
                if action == PlayerActions.CHECK:
                    if self.highest_bid != 0:
                        self.players[self.current_player].fold()
                elif action == PlayerActions.CALL:
                    amount_called = self.highest_bid - self.players[self.current_player].current_bid
                    self.players[self.current_player].deduct_balance(amount_called)
                    if self.players[self.current_player].balance == 0:
                        self.players[self.current_player].all_in(self.pot_amount)
                    self.pot_amount += amount_called
                elif action == PlayerActions.RAISE:
                    amount_raised = max(self.highest_bid + raise_amount, self.starting_blind)
                    self.pot_amount += amount_raised
                    self.players[self.current_player].deduct_balance(amount_raised)
                    self.highest_bid = amount_raised
                    self.last_bidder = self.current_player
                elif action == PlayerActions.ALL_IN:
                    self.players[self.current_player].all_in(self.pot_amount)
                    self.pot_amount += self.players[self.current_player].balance
                elif action == PlayerActions.FOLD:
                    self.players[self.current_player].fold()
            
            if self.current_player == len(self.players) - 1:
                self.current_player = 0
            else:
                self.current_player += 1

    def check_winner(self) -> bool:
        players_in = 0
        for p in self.players:
            if p.balance != 0:
                players_in += 1
        return players_in <= 1
    
    def check_hand_winner(self) -> bool:
        players_in = 0
        for p in self.players:
            if p.balance != 0 and not p.folded:
                players_in += 1
        return players_in <= 1

    def deal(self) -> None:
        for _ in range(2):
            for p in self.players:
                p.hand.add(self.deck.draw_card())

    def show_next_cards(self, round: int) -> None:
        if round == 0:
            for _ in range(3):
                card = self.deck.draw_card()
                for p in self.players:
                    p.hand.add(card)
        else:
            card = self.deck.draw_card()
            for p in self.players:
                p.hand.add(card)

    def move_blinds(self) -> None:
        next_player = self.first_player + 1
        while True:
            if not self.players[next_player].folded:
                self.first_turn += next_player
                break

            if self.first_player + next_player == len(self.players) - 1:
                next_player = 0
            else:
                next_player += 1


    def check_blinds_raise(self) -> None:
        if self.first_turn == 0:
            self.blind *= 1+self.blind_increase

