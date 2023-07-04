from .deck import Deck
from .player import Player
from .player_actions import PlayerActions
from typing import List

'''
scale to have consistent starting amounts and raises
make players lose if balance == 0 after settle pot
handle blinds without players
'''

class Game():
    def __init__(self, players: List[Player], starting_blind: int, blind_increase: float, max_rounds: int) -> None:
        self.players = players
        self.deck = Deck()
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

            for i in range(4):
                self.show_next_cards(i)
                self.round()
                for p in self.players:
                    p.round_bid = 0
                if self.check_hand_winner():
                    rd = i
                    while len(self.players[0].hand.cards) < 7:
                        self.show_next_cards(rd)
                        rd += 1
                    break

            self.settle_pot()
            self.remove_losers()
            self.move_blinds()
            self.reset_round() 

            self.rounds_complete += 1
    
    def round(self) -> None:
        self.players[self.first_turn - 1].deduct_balance(self.blind)
        self.players[self.first_turn - 2].deduct_balance(self.blind // 2)
        while self.current_player != self.last_bidder:
            if not self.players[self.current_player].folded and not self.players[self.current_player].is_all_in and not self.players[self.current_player].is_out:
                action, raise_amount = self.players[self.current_player].action()
                if action == PlayerActions.CHECK:
                    self.players[self.current_player].check(self.highest_bid)
                elif action == PlayerActions.CALL:
                    self.pot_amount += self.players[self.current_player].call(self.highest_bid, self.pot_amount)
                elif action == PlayerActions.RAISE:
                    bet_amount = self.players[self.current_player].raise_bid(raise_amount)
                    if bet_amount < self.highest_bid:
                        self.pot_amount += bet_amount
                    else:
                        self.pot_amount += bet_amount
                        self.highest_bid = bet_amount - self.highest_bid
                        self.last_bidder = self.current_player
                elif action == PlayerActions.ALL_IN:
                    self.pot_amount += self.players[self.current_player].all_in(self.pot_amount)
                elif action == PlayerActions.FOLD:
                    self.players[self.current_player].fold()
            
            if self.current_player == len(self.players) - 1:
                self.current_player = 0
            else:
                self.current_player += 1
    
    def reset_round(self):
        self.pot_amount = self.blind + self.blind // 2
        self.highest_bid = self.blind
        self.current_player = self.first_turn
        for p in self.players:
            p.current_bid = 0
            p.folded = False
            p.is_all_in = False

    def check_winner(self) -> bool:
        players_in = 0
        for p in self.players:
            if p.balance != 0:
                players_in += 1
        return players_in <= 1
    
    def check_hand_winner(self) -> bool:
        players_in = 0
        for p in self.players:
            if p.balance != 0 and not p.folded and not p.is_all_in:
                players_in += 1
        return players_in <= 1

    def deal(self) -> None:
        for _ in range(2):
            for p in self.players:
                p.hand.add_card(self.deck.draw_card())

    def show_next_cards(self, round: int) -> None:
        if round == 0:
            return
        elif round == 1:
            for _ in range(3):
                card = self.deck.draw_card()
                for p in self.players:
                    p.hand.add_card(card)
        else:
            card = self.deck.draw_card()
            for p in self.players:
                p.hand.add_card(card)

    def move_blinds(self) -> None:
        next_player = self.first_turn
        while True:
            if next_player >= len(self.players) - 1:
                self.blind *= 1+self.blind_increase
                next_player = 0
            else:
                next_player += 1
            if not self.players[next_player].is_out:
                self.first_turn = next_player
                break
    
    def settle_pot(self):
        unfolded_players = [p for p in self.players if not p.folded]
        unfolded_players.sort(key=lambda p: p.hand, reverse=True)
        settled_players = []
        for i, p in enumerate(unfolded_players):
            if self.pot_amount <= 0:
                break
            if p in settled_players:
                continue
            tied_players = [p]
            for j, p2 in enumerate(unfolded_players):
                if i != j:
                    if p.hand == p2.hand:
                        tied_players.append(p2)
            tied_players.sort(key=lambda p: p.current_bid)
            prev_bid = 0
            for tied_player in tied_players:
                side_pot = 0
                for other in self.players:
                    if not other in settled_players and not other in tied_players:
                        side_pot += min(tied_player.current_bid - prev_bid, other.current_bid)
                        self.pot_amount -= min(tied_player.current_bid - prev_bid, other.current_bid)
                        other.current_bid -= min(tied_player.current_bid - prev_bid, other.current_bid)
                prev_bid = tied_player.current_bid
                split_winners = [p for p in tied_players if p not in settled_players]
                for tied_player2 in split_winners:
                    tied_player2.increase_balance(side_pot / len(split_winners))
                tied_player.increase_balance(tied_player.current_bid)
                tied_player.current_bid = 0
                settled_players.append(tied_player)

    def remove_losers(self):
        for p in self.players:
            if p.balance <= 0:
                p.is_out = True




