import unittest
from ..poker.game import Game
from ..poker.player import Player
from ..poker.hand import Hand
from ..poker.card import Card
from ..poker.suit import Suit


class GameTestCase(unittest.TestCase):
    def setUp(self):
        # Create a sample game setup for testing
        self.player1 = Player(1000, Hand(), None, None)
        self.player2 = Player(1000, Hand(), None, None)
        self.player3 = Player(1000, Hand(), None, None)
        self.player4 = Player(1000, Hand(), None, None)
        self.players = [self.player1, self.player2, self.player3, self.player4]
        self.game = Game(self.players, 10, 0.1, 10)

    def test_deal(self):
        # Verify that the players' hands are populated after dealing
        self.game.deal()
        for player in self.players:
            self.assertEqual(len(player.hand.cards), 2)

    def test_show_next_cards(self):
        # Verify that the correct number of cards is added to players' hands
        self.game.deal()
        self.game.show_next_cards(1)
        for player in self.players:
            self.assertEqual(len(player.hand.cards), 5)

    def test_move_blinds(self):
        # Verify that the blinds are moved to the next player correctly
        self.assertEqual(self.game.first_turn, 0)
        self.game.move_blinds()
        self.assertEqual(self.game.first_turn, 1)
        self.game.move_blinds()
        self.assertEqual(self.game.first_turn, 2)
        self.game.players[1].is_out = True  # Player 1 is out, so blinds should skip them
        self.game.move_blinds()
        self.assertEqual(self.game.first_turn, 3)
        self.game.move_blinds()
        self.assertEqual(self.game.first_turn, 0)
        self.game.move_blinds()
        self.assertEqual(self.game.first_turn, 2)

    def test_settle_pot(self):
        # Create a sample hand configuration
        hand1 = Hand()
        hand1.add_card(Card(14, Suit.SPADE))
        hand1.add_card(Card(13, Suit.SPADE))
        hand2 = Hand()
        hand2.add_card(Card(12, Suit.HEART))
        hand2.add_card(Card(11, Suit.HEART))
        hand3 = Hand()
        hand3.add_card(Card(12, Suit.CLUB))
        hand3.add_card(Card(11, Suit.CLUB))
        hand4 = Hand()
        hand4.add_card(Card(10, Suit.CLUB))
        hand4.add_card(Card(9, Suit.CLUB))
        self.player1.hand = hand1
        self.player2.hand = hand2
        self.player3.hand = hand3
        self.player4.hand = hand4
        self.player1.current_bid = 100
        self.player1.deduct_balance(100)
        self.player2.current_bid = 200
        self.player2.deduct_balance(200)
        self.player3.current_bid = 300
        self.player3.deduct_balance(300)
        self.player4.current_bid = 300
        self.player4.deduct_balance(300)
        self.game.pot_amount = 900

        # Verify that the pot is settled correctly
        self.game.settle_pot()

        # Player 1 should receive 200 chips (his contribution from each player)
        self.assertEqual(self.player1.balance, 1300)

        # Player 2 should lose 50 chips (split some of remaining with P3)
        self.assertEqual(self.player2.balance, 950)

        # Player 3 should gain 50 chips (from side pot with P4 and split with P2)
        self.assertEqual(self.player3.balance, 1050)

        # Player 4 should lose 300 chips (their contribution)
        self.assertEqual(self.player4.balance, 700)

    def test_remove_losers(self):
        # Set up a sample game state with a player who has a zero balance
        self.player1.balance = 0
        self.player2.balance = 1000
        self.player3.balance = 500

        # Verify that the player with zero balance is marked as out
        self.game.remove_losers()
        self.assertTrue(self.player1.is_out)
        self.assertFalse(self.player2.is_out)
        self.assertFalse(self.player3.is_out)

if __name__ == '__main__':
    unittest.main()
