import pygame
pygame.font.init()

#screen dimensions
WIDTH = 1000
HEIGHT = 600
GAMEWIDTH = (WIDTH/2)+100

#board dimensions
ROWS = 8
COLS = 8
SQSIZE = GAMEWIDTH // COLS

DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

BOARD_ORIGIN = (0,599)

COLOUR_ONE = (55,62,152)
COLOUR_TWO = (206,185,44)
COLOUR_THREE = (241,103,117)
BLACK = (0,0,0)
WHITE = (255,255,255)
COLOUR_BLACK = (0,0,0)
COLOUR_WHITE = (255,255,255)

# Create the font
font = pygame.font.SysFont("Arial", 32)
base_font = pygame.font.Font(None, 32)

def update_black(colour):
    global COLOUR_BLACK 
    COLOUR_BLACK = colour

def update_white(colour):
    global COLOUR_WHITE
    COLOUR_WHITE = colour

def get_black():
    return COLOUR_BLACK

def get_white():
    return COLOUR_WHITE