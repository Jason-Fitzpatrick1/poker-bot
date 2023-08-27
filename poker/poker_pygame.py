import pygame
import sys
from typing import Dict, List
from .deck import Deck
from .player import Player
from .game import Game

# Set up display dimensions
WIDTH, HEIGHT = 1200, 700
CARD_WIDTH, CARD_HEIGHT = 50, 73
CARD_GAP = 10
TABLE_IMAGE_PATH = "C:\\Users\\jason\\Desktop\\poker-bot\\poker-bot\\poker\\poker_images\\table.jpg"
CARD_PATH = "C:\\Users\\jason\\Desktop\\poker-bot\\poker-bot\\poker\\poker_images\\cards\\"

# Define colors
WHITE = (255, 255, 255)

LABEL_POS = {
    1: ((0.5*WIDTH) - CARD_WIDTH - (CARD_GAP/2), HEIGHT - (2*CARD_HEIGHT) - CARD_GAP),
    2: ((0.25*WIDTH) - CARD_WIDTH - (CARD_GAP/2), HEIGHT - (2*CARD_HEIGHT) - CARD_GAP),
    3: (CARD_GAP, 0.75*HEIGHT - CARD_HEIGHT),
    4: (CARD_GAP, 0.25*HEIGHT - CARD_HEIGHT),
    5: ((0.25*WIDTH) - CARD_WIDTH - (CARD_GAP/2), (2*CARD_GAP) + CARD_HEIGHT),
    6: ((0.5*WIDTH) - CARD_WIDTH - (CARD_GAP/2), (2*CARD_GAP) + CARD_HEIGHT),
    7: ((0.75*WIDTH) - CARD_WIDTH - (CARD_GAP/2), (2*CARD_GAP) + CARD_HEIGHT),
    8: (WIDTH - (2*CARD_WIDTH) - (2*CARD_GAP), 0.25*HEIGHT - CARD_HEIGHT),
    9: (WIDTH - (2*CARD_WIDTH) - (2*CARD_GAP), 0.75*HEIGHT - CARD_HEIGHT),
    10: ((0.75*WIDTH) - CARD_WIDTH - (CARD_GAP/2), HEIGHT - (2*CARD_HEIGHT) - CARD_GAP)
}
POT_LABEL_X, POT_LABEL_Y = 0.5*WIDTH, 0.6*HEIGHT

CARD_POS = {
    (0, 1): ((0.5*WIDTH) - (2.5*CARD_WIDTH) - (2*CARD_GAP), (HEIGHT/2) - (CARD_HEIGHT//2)),
    (0, 2): ((0.5*WIDTH) - (1.5*CARD_WIDTH) - CARD_GAP, (HEIGHT/2) - (CARD_HEIGHT//2)),
    (0, 3): ((0.5*WIDTH) - (0.5*CARD_WIDTH), (HEIGHT/2) - (CARD_HEIGHT//2)),
    (0, 4): ((0.5*WIDTH) + (0.5*CARD_WIDTH) + CARD_GAP, (HEIGHT/2) - (CARD_HEIGHT//2)),
    (0, 5): ((0.5*WIDTH) + (1.5*CARD_WIDTH) + (2*CARD_GAP), (HEIGHT/2) - (CARD_HEIGHT//2)),
    (1, 1): ((0.5*WIDTH) - CARD_WIDTH - (CARD_GAP/2), HEIGHT - CARD_HEIGHT - CARD_GAP),
    (1, 2): ((0.5*WIDTH) + (CARD_GAP/2), HEIGHT - CARD_HEIGHT - CARD_GAP),
    (2, 1): ((0.25*WIDTH) - CARD_WIDTH - (CARD_GAP/2), HEIGHT - CARD_HEIGHT - CARD_GAP),
    (2, 2): ((0.25*WIDTH) + (CARD_GAP/2), HEIGHT - CARD_HEIGHT - CARD_GAP),
    (3, 1): (CARD_GAP, 0.75*HEIGHT),
    (3, 2): (CARD_WIDTH + (2*CARD_GAP), 0.75*HEIGHT),
    (4, 1): (CARD_GAP, 0.25*HEIGHT),
    (4, 2): (CARD_WIDTH + (2*CARD_GAP), 0.25*HEIGHT),
    (5, 1): ((0.25*WIDTH) - CARD_WIDTH - (CARD_GAP/2), CARD_GAP),
    (5, 2): ((0.25*WIDTH) + (CARD_GAP/2), CARD_GAP),
    (6, 1): ((0.5*WIDTH) - CARD_WIDTH - (CARD_GAP/2), CARD_GAP),
    (6, 2): ((0.5*WIDTH) + (CARD_GAP/2), CARD_GAP),
    (7, 1): ((0.75*WIDTH) - CARD_WIDTH - (CARD_GAP/2), CARD_GAP),
    (7, 2): ((0.75*WIDTH) + (CARD_GAP/2), CARD_GAP),
    (8, 1): (WIDTH - (2*CARD_WIDTH) - (2*CARD_GAP), 0.25*HEIGHT),
    (8, 2): (WIDTH - CARD_WIDTH - CARD_GAP, 0.25*HEIGHT),
    (9, 1): (WIDTH - (2*CARD_WIDTH) - (2*CARD_GAP), 0.75*HEIGHT),
    (9, 2): (WIDTH - CARD_WIDTH - CARD_GAP, 0.75*HEIGHT),
    (10, 1): ((0.75*WIDTH) - CARD_WIDTH - (CARD_GAP/2), HEIGHT - CARD_HEIGHT - CARD_GAP),
    (10, 2): ((0.75*WIDTH) + (CARD_GAP/2), HEIGHT - CARD_HEIGHT - CARD_GAP),
}

class HoldemFrontend:
    def __init__(self, game: Game) -> None:
        self.game = game
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Texas Hold'em")

        self.table_image = pygame.image.load(TABLE_IMAGE_PATH)
        self.font = pygame.font.Font(None, 24)

        # Create a separate surface for double buffering
        self.buffered_surface = pygame.Surface((WIDTH, HEIGHT))

        # Initialize backend_data
        self.backend_data = {}
    
    def step(self, action_index: int) -> None:
        """
        Performs a poker action according to the index:
        0: Shuffle and deal
        1: Round of betting
        2: Show flop
        3: Round of betting
        4: Show turn
        5: Round of betting
        6: Show river
        7: Round of betting
        8. Settle pot and reset round

        Returns:
            None
        """
        if action_index == 0:
            self.game.deck = Deck()
            self.game.deck.shuffle()
            self.game.deal()
            # show face down cards for each player
        elif action_index % 2 != 0:
            for p in self.game.players:
                p.round_bid = 0
            self.game.deduct_blinds()
            self.game.process_player_actions()
        elif action_index in [2, 4, 6]:
            self.game.show_next_cards(action_index-1) # will pass a 1 for index 2, and next rounds will be > 1
            # show dealt community cards
        elif action_index == 8:
            # show player cards face up
            self.show_cards()
            self.game.settle_pot()
            self.game.remove_losers()
            self.game.move_blinds()
            self.game.reset_round() 

    def show(self) -> None:
        self.running = True
        action_index = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.step(action_index)
            if action_index >= 8:
                action_index = 0
            else:
                action_index += 1

            self.update()

            pygame.display.flip()

        self.quit()
    
    def quit(self):
        pygame.quit()
        sys.exit()

    def get_card_path(self, card_name: str) -> str:
        return CARD_PATH + card_name + ".png"

    # Function to draw player labels
    def draw_player_labels(self, player_num: int, player_balance: int, player_bet: int, player_action: str) -> None:
        player_label = self.font.render(f"Player {player_num}", True, WHITE)
        money_label = self.font.render(f"${player_balance} (${player_bet})", True, WHITE)
        action_label = self.font.render(player_action, True, WHITE)
        x, y = LABEL_POS[player_num]

        self.screen.blit(player_label, (x, y))
        self.screen.blit(money_label, (x, y + 20))
        self.screen.blit(action_label, (x, y + 40))
    
    def draw_pot_label(self) -> None:
        pot_label = self.font.render(f"Round winnings: {self.game.pot_amount}", True, WHITE)
        self.screen.blit(pot_label, (POT_LABEL_X, POT_LABEL_Y))

    # Function to place cards
    def place_card(self, player_num: int, card_num: int, card_name: str) -> None:
        x, y = CARD_POS[(player_num, card_num)]
        card_image = pygame.image.load(self.get_card_path(card_name))
        scaled_card = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
        self.screen.blit(scaled_card, (x, y))

    def update_backend_data(self) -> Dict[int, Dict[str, any]]:
        # data = {1: {"balance", "bet", "action"}}
        player_list = self.game.players
        data = {}
        for i, player in enumerate(player_list):
            data[i+1] = {"balance": player.balance, "bet": player.round_bid, "action": player.prev_action}
        return data

    def update(self) -> None:
        # Clear the buffered surface
        self.buffered_surface.fill(WHITE)
        # Draw the table background on the buffered surface
        self.buffered_surface.blit(self.table_image, (0, 0))
        # Update the display with the buffered surface
        self.screen.blit(self.buffered_surface, (0, 0))

        self.draw_pot_label()

        self.update_backend_data()
        for player_num, player_data in self.backend_data.items():
            self.draw_player_labels(player_num, player_data["balance"], player_data["bet"], player_data["action"])
        

