import pygame

#screen dimensions
WIDTH = 600
HEIGHT = 600

#board dimensions
ROWS = 8
COLS = 8
SQSIZE = WIDTH // COLS

DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

BOARD_ORIGIN = (0,599)


pawnImg = pygame.image.load('b_pawn_1x_ns.png')

