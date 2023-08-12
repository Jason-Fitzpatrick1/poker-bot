import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display dimensions
WIDTH, HEIGHT = 1200, 700
CARD_WIDTH, CARD_HEIGHT = 50, 73
CARD_GAP = 10
TABLE_IMAGE_PATH = "C:\\Users\\jason\\Desktop\\poker-bot\\poker-bot\\poker\\poker_images\\table.jpg"
CARD_PATH = "C:\\Users\\jason\\Desktop\\poker-bot\\poker-bot\\poker\\poker_images\\cards\\"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texas Hold'em")

# Define colors
WHITE = (255, 255, 255)

# Load images and fonts (adjust paths accordingly)
table_image = pygame.image.load(TABLE_IMAGE_PATH)
font = pygame.font.Font(None, 24)

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

def get_card_path(card_name):
    return CARD_PATH + card_name + ".png"

# Function to draw player labels
def draw_player_labels(player_num, player_balance, player_bet, player_action):
    player_label = font.render(f"Player {player_num}", True, WHITE)
    money_label = font.render(f"${player_balance} (${player_bet})", True, WHITE)
    action_label = font.render(player_action, True, WHITE)
    x, y = LABEL_POS[player_num]

    screen.blit(player_label, (x, y))
    screen.blit(money_label, (x, y + 20))
    screen.blit(action_label, (x, y + 40))

# Function to place cards
def place_card(player_num, card_num, card_name):
    x, y = CARD_POS[(player_num, card_num)]
    card_image = pygame.image.load(get_card_path(card_name))
    scaled_card = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(scaled_card, (x, y))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the table background
    screen.blit(table_image, (0, 0))

    # Draw community cards
    for card_num in range(1, 6):
        place_card(0, card_num, "face_down")

    # Draw player cards & labels
    for player_num in range(1, 11):
        draw_player_labels(player_num, 1000, 250, "CHECK")
        for card_num in range(1, 3):
            place_card(player_num, card_num, "face_down")
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
