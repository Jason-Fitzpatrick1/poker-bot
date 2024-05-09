from .deck import Deck
from .player import Player
from .player_actions import PlayerActions
from typing import List

import logging
logger = logging.getLogger(__name__)

class Game():
    def __init__(self, players: List[Player], starting_blind: int, blind_increase: float, max_rounds: int) -> None:
        self.players = players
        self.deck = Deck()
        self.blind = starting_blind
        self.blind_increase = blind_increase
        self.max_rounds = max_rounds
        self.pot_amount = self.blind + self.blind // 2
        self.first_turn = 0
        self.highest_bid = self.blind
        self.rounds_complete = 0
        self.last_bidder = None
        self.current_player = 0

    def simulate(self) -> None:
        """
        Simulates a complete game of poker until a winner is determined or the maximum number of rounds is reached.

        Performs rounds of dealing cards, showing next cards, player actions, pot settlement, elimination of losers,
        blind movement, and round resetting. The simulation continues until a winner is declared or the maximum number
        of rounds is reached.

        Returns:
            None
        """
        logger.info("Welcome to Texas Hold'Em!\n")
        while not self.check_winner() and self.rounds_complete < self.max_rounds:
            self.deck = Deck()
            self.deck.shuffle()
            self.deal()
            for i in range(4):
                self.round(i)
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
            logger.info("\nRound Complete!\n")
            self.rounds_complete += 1
    
    def round(self, round: int) -> None:
        """
        Conducts a round of betting in the game.

        Deducts blinds from the players, handles their actions, updates pot amount,
        highest bid, and current player position.

        Returns:
            None
        """
        round_names = ["PRE-FLOP", "FLOP", "TURN", "RIVER"]
        logger.info(f"{round_names[round]}\n")

        self.show_next_cards(round)
        self.current_player = self.first_turn
        self.last_bidder = None

        # Reset bets each round
        for i, p in enumerate(self.players):
            logger.info(f"Player {i+1} has a balance of ${p.balance}")
            p.round_bid = 0
            self.highest_bid = 0

        if round == 0:
            self.deduct_blinds()

        self.process_player_actions()

    def deduct_blinds(self) -> None:
        """
        Deducts blinds from the players.

        Returns:
            None
        """
        self.players[self.first_turn - 1].deduct_balance(self.blind)
        self.players[self.first_turn - 1].current_bid += self.blind
        self.players[self.first_turn - 1].round_bid += self.blind
        self.players[self.first_turn - 2].deduct_balance(self.blind // 2)
        self.players[self.first_turn - 2].current_bid += self.blind // 2
        self.players[self.first_turn - 2].round_bid += self.blind // 2
        self.highest_bid = self.blind

    def process_player_actions(self) -> None:
        """
        Processes actions of the players.

        Returns:
            None
        """
        while self.current_player != self.last_bidder:
            if self.last_bidder == None:
                self.last_bidder = self.current_player
            logging.info(f"Player {self.current_player + 1}'s turn (Balance: {self.players[self.current_player].balance}, Player's bet this hand: {self.players[self.current_player].current_bid}, Player's bet this round: {self.players[self.current_player].round_bid}, Amount to call: {self.highest_bid - self.players[self.current_player].round_bid}, Pot: {self.pot_amount}):\n")
            player = self.players[self.current_player]
            if self.is_valid_player(player):
                other_actions = [p.prev_action for p in self.players if p != self.players[self.current_player]]
                while len(other_actions) < 9:
                    other_actions.append(PlayerActions.FOLD)
                if player.player_type == "AI":
                    action, raise_amount = player.action(self.pot_amount, other_actions[0], other_actions[1], other_actions[2], other_actions[3],
                                                        other_actions[4], other_actions[5], other_actions[6], other_actions[7], other_actions[8])
                else:
                    action, raise_amount = player.get_action_from_user()
                self.perform_action(player, action, raise_amount)
            self.update_current_player()

    def is_valid_player(self, player: Player) -> bool:
        """
        Checks if the player is valid for taking action.

        Returns:
            bool: True if the player is valid, False otherwise.
        """
        return not player.folded and not player.is_all_in and not player.is_out

    def perform_action(self, player: Player, action: PlayerActions, raise_amount: int) -> None:
        """
        Performs the corresponding action based on the player's choice.

        Returns:
            None
        """
        if action == PlayerActions.CHECK:
            player.check(self.highest_bid)
            logger.info("Player checks\n")
        elif action == PlayerActions.CALL:
            self.pot_amount += player.call(self.highest_bid, self.pot_amount)
            logger.info(f"Player calls ${self.highest_bid}. Pot is ${self.pot_amount}\n")
        elif action == PlayerActions.RAISE:
            self.handle_raise(player, raise_amount)
            logger.info(f"Player raises ${raise_amount}. Pot is ${self.pot_amount}\n")
        elif action == PlayerActions.ALL_IN:
            self.handle_raise(player, player.balance)
            logger.info(f"Player goes all-in! Pot is ${self.pot_amount}\n")
        elif action == PlayerActions.FOLD:
            player.fold()
            logger.info(f"Player folds.\n")

    def handle_raise(self, player: Player, raise_amount: int) -> None:
        """
        Handles the raise action of the player.

        Returns:
            None
        """
        # raise_bid is save against overdrafts
        bet_amount = player.raise_bid(self.blind, self.highest_bid, raise_amount, self.pot_amount)
        self.pot_amount += bet_amount

        if player.round_bid > self.highest_bid:
            self.highest_bid = player.round_bid
            self.last_bidder = self.players.index(player)

    def update_current_player(self) -> None:
        """
        Updates the current player position.

        Returns:
            None
        """
        if self.current_player == len(self.players) - 1:
            self.current_player = 0
        else:
            self.current_player += 1

    
    def reset_round(self) -> None:
        """
        Resets the round for a new betting session.

        Resets the pot amount, highest bid, current player position, and clears
        the current bids and folded/all-in statuses of the players.

        Returns:
            None
        """
        self.pot_amount = self.blind + self.blind // 2
        self.highest_bid = self.blind
        self.current_player = self.first_turn
        self.last_bidder = None
        for p in self.players:
            p.current_bid = 0
            p.folded = False
            p.is_all_in = False
            p.prev_action = PlayerActions.NO_ACTION
            p.hand.clear()

    def check_winner(self) -> bool:
        """
        Checks if there is a winner in the game.

        Determines if there is only one player remaining with a non-zero balance.

        Returns:
            bool: True if there is a winner, False otherwise.
        """
        players_in = 0
        for p in self.players:
            if p.balance != 0:
                players_in += 1
        return players_in <= 1

    def check_hand_winner(self) -> bool:
        """
        Checks if there is a winner for the current hand.

        Determines if there is only one player remaining with a non-zero balance,
        and who has not folded or gone all-in.

        Returns:
            bool: True if there is a winner, False otherwise.
        """
        players_in = 0
        for p in self.players:
            if p.balance != 0 and not p.folded and not p.is_all_in:
                players_in += 1
        return players_in <= 1

    def deal(self) -> None:
        """
        Deals cards to the players.

        Deals two cards to each player by drawing cards from the deck.

        Returns:
            None
        """
        for i, p in enumerate(self.players):
            card1 = self.deck.draw_card()
            card2 = self.deck.draw_card()
            p.hand.add_card(card1)
            p.hand.add_card(card2)
            if p.player_type != "AI":
                logger.info(f"Player {i+1} hand: Card 1 is {card1}, Card 2 is {card2}")


    def show_next_cards(self, round: int) -> None:
        """
        Shows the next set of cards based on the given round.

        Draws cards from the deck and adds them to each player's hand.

        Args:
            round (int): The current round of the game.

        Returns:
            None
        """
        logger.info(f"Drawn Cards:")
        if round == 0:
            return
        elif round == 1:
            self.draw_common_cards(3)
        else:
            self.draw_common_cards(1)

    def draw_common_cards(self, num_cards: int) -> None:
        """
        Draws a specified number of cards from the deck and adds them to each player's hand.

        Args:
            num_cards (int): The number of cards to draw.

        Returns:
            None
        """
        for _ in range(num_cards):
            card = self.deck.draw_card()
            logger.info(card)
            for p in self.players:
                p.hand.add_card(card)


    def move_blinds(self) -> None:
        """
        Moves the blinds to the next player who is still in the game.

        Adjusts the blind amount and updates the first turn to the next eligible player.

        Returns:
            None
        """
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
    def settle_pot(self) -> None:
        """
        Settles the pot by distributing winnings to players with the best hands.

        Determines the winners among the unfolded players, settles side pots, and distributes
        the winnings proportionally among tied players.

        Returns:
            None
        """
        unfolded_players = self.get_unfolded_players_sorted()

        settled_players = []
        for i, p in enumerate(unfolded_players):
            if self.pot_amount <= 0:
                break
            if p in settled_players:
                continue
            tied_players = self.get_tied_players(p, unfolded_players, i)

            self.distribute_winnings(tied_players, settled_players)
        logger.info("Pot settled.\n")

    def get_unfolded_players_sorted(self) -> List[Player]:
        """
        Retrieves a list of unfolded players sorted by hand strength in descending order.

        Returns:
            List[Player]: The unfolded players sorted by hand strength.
        """
        unfolded_players = [p for p in self.players if not p.folded and not p.is_out]
        unfolded_players.sort(key=lambda p: p.hand, reverse=True)
        logging.info(f"Winning hand: {unfolded_players[0].hand}\n")
        return unfolded_players

    def get_tied_players(self, player: Player, unfolded_players: List[Player], index: int) -> List[Player]:
        """
        Retrieves a list of tied players with the same hand strength.

        Args:
            player (Player): The current player.
            unfolded_players (List[Player]): The unfolded players list.
            index (int): The index of the current player.

        Returns:
            List[Player]: The tied players with the same hand strength.
        """
        tied_players = [player]
        for j, p2 in enumerate(unfolded_players):
            if index != j and player.hand == p2.hand:
                tied_players.append(p2)
        tied_players.sort(key=lambda p: p.current_bid)
        return tied_players
    
    def distribute_winnings(self, tied_players: List[Player], settled_players: List[Player]) -> None:
        """
        Distributes the winnings among the tied players and settles their bids.

        Calculates the side pot for each tied player and distributes the winnings proportionally
        among the split winners. The settled players' current bids are reset, and they are marked as settled.

        Args:
            tied_players (List[Player]): The tied players with the same hand strength.
            settled_players (List[Player]): The players who have already settled.

        Returns:
            None
        """
        prev_bid = 0
        for tied_player in tied_players:
            side_pot = self.calculate_side_pot(tied_player, tied_players, settled_players, prev_bid)
            prev_bid = tied_player.current_bid

            split_winners = [p for p in tied_players if p not in settled_players]
            for tied_player2 in split_winners:
                tied_player2.increase_balance(side_pot / len(split_winners))
            tied_player.increase_balance(tied_player.current_bid)
            tied_player.current_bid = 0
            settled_players.append(tied_player)

    def calculate_side_pot(self, tied_player: Player, tied_players: List[Player], settled_players: List[Player], prev_bid: int) -> int:
        """
        Calculates the side pot amount for the tied player.

        Iterates over the players to calculate the contribution to the side pot from each player.
        Contributions are made by players who are not settled, not tied players, and are still in the game.

        Args:
            tied_player (Player): The tied player for whom the side pot is being calculated.
            tied_players (List[Player]): The tied players with the same hand strength.
            settled_players (List[Player]): The players who have already settled.
            prev_bid (int): The previous bid amount in the pot.

        Returns:
            int: The side pot amount for the tied player.
        """
        side_pot = 0
        for other in self.players:
            if not other in settled_players and not other in tied_players and not other.is_out:
                contribution = min(tied_player.current_bid - prev_bid, other.current_bid)
                side_pot += contribution
                self.pot_amount -= contribution
                other.current_bid -= contribution

        return side_pot

    def remove_losers(self) -> None:
        """
        Removes players with zero or negative balance from the game.

        Marks players with a balance less than or equal to zero as out of the game.

        Returns:
            None
        """
        for i, p in enumerate(self.players):
            if p.balance <= 0:
                p.is_out = True
                p.prev_action = PlayerActions.FOLD
                logging.info(f"Player {i+1} has been eliminated.")




