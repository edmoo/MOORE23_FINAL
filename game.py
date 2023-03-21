import pygame
from const import *
from board import *

pawn_black = pygame.image.load("sprites/PNGs/No shadow/1x/b_pawn_1x_ns.png")
rook_black = pygame.image.load("sprites/PNGs/No shadow/1x/b_rook_1x_ns.png")
knight_black = pygame.image.load("sprites/PNGs/No shadow/1x/b_knight_1x_ns.png")
bishop_black = pygame.image.load("sprites/PNGs/No shadow/1x/b_bishop_1x_ns.png")
queen_black = pygame.image.load("sprites/PNGs/No shadow/1x/b_queen_1x_ns.png")
king_black = pygame.image.load("sprites/PNGs/No shadow/1x/b_king_1x_ns.png")

pawn_black = pygame.transform.scale(pawn_black, (SQSIZE, SQSIZE))
rook_black = pygame.transform.scale(rook_black, (SQSIZE, SQSIZE))
knight_black = pygame.transform.scale(knight_black, (SQSIZE, SQSIZE))
bishop_black = pygame.transform.scale(bishop_black, (SQSIZE, SQSIZE))
queen_black = pygame.transform.scale(queen_black, (SQSIZE, SQSIZE))
king_black = pygame.transform.scale(king_black, (SQSIZE, SQSIZE))

pawn_white = pygame.image.load("sprites/PNGs/No shadow/1x/w_pawn_1x_ns.png")
rook_white = pygame.image.load("sprites/PNGs/No shadow/1x/w_rook_1x_ns.png")
knight_white = pygame.image.load("sprites/PNGs/No shadow/1x/w_knight_1x_ns.png")
bishop_white = pygame.image.load("sprites/PNGs/No shadow/1x/w_bishop_1x_ns.png")
queen_white = pygame.image.load("sprites/PNGs/No shadow/1x/w_queen_1x_ns.png")
king_white = pygame.image.load("sprites/PNGs/No shadow/1x/w_king_1x_ns.png")

pawn_white = pygame.transform.scale(pawn_white, (SQSIZE, SQSIZE))
rook_white = pygame.transform.scale(rook_white, (SQSIZE, SQSIZE))
knight_white = pygame.transform.scale(knight_white, (SQSIZE, SQSIZE))
bishop_white = pygame.transform.scale(bishop_white, (SQSIZE, SQSIZE))
queen_white = pygame.transform.scale(queen_white, (SQSIZE, SQSIZE))
king_white = pygame.transform.scale(king_white, (SQSIZE, SQSIZE))

piece_color = (255, 255, 255)
class Game:
    
    def __init__(self):
            pass
    #show methods

    def show_bg(self, surface, brd):
        for row in range(ROWS):
            for col in range (COLS):
                if(row+col) % 2 == 0:
                    color = (234, 235, 200) #light
                else:
                    color = (119, 154, 88) #dark
                
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface,color,rect)
        brdMat = board_toMatrix(brd.fen())
        for row in range(8):
            for col in range(8):
                x = col * SQSIZE
                y = row * SQSIZE
                #gets position according to python chess positions
                brdPos = ((7-row)*8)+col
                piece = brdMat[row][col]
                if piece == "p":
                    print("\nx = "+str(col))
                    print("y = "+str(row))
                    print("test = "+str(((7-row)*8)+col))
                    surface.blit(pawn_black, (x, y))
                elif piece == "r":
                    surface.blit(rook_black, (x, y))
                elif piece == "n":
                    surface.blit(knight_black, (x, y))
                elif piece == "b":
                    surface.blit(bishop_black, (x, y))
                elif piece == "q":
                    surface.blit(queen_black, (x, y))
                elif piece == "k":
                    surface.blit(king_black, (x, y))
                elif piece == "P":
                    surface.blit(pawn_white,(x,y))
                elif piece == "R":
                    surface.blit(rook_white, (x, y))
                elif piece == "N":
                    surface.blit(knight_white, (x, y))
                elif piece == "B":
                    surface.blit(bishop_white, (x, y))
                elif piece == "Q":
                    surface.blit(queen_white, (x, y))
                elif piece == "K":
                    surface.blit(king_white, (x, y))





def mouse_position():
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_ORIGIN
    if(mouse_pos[0] == 0):mouse_pos[0] = 1
    if(mouse_pos[1] == 0):mouse_pos[1] = 1
    y = (mouse_pos[0])//SQSIZE
    x = (mouse_pos[1]+BOARD_ORIGIN[1])//SQSIZE
    if(x==0):x=7
    elif(x==1):x=6
    elif(x==2):x=5
    elif(x==3):x=4
    elif(x==4):x=3
    elif(x==5):x=2
    elif(x==6):x=1
    elif(x==7):x=0
    elif(x==8):x=0
    pos = y+(x*8)
    posInt = int(pos)
    return posInt

