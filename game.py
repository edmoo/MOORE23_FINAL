import pygame
import chess.svg
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

# Define the position and size of the list box
LIST_BOX_X = 650
LIST_BOX_Y = 30
LIST_BOX_WIDTH = 300
LIST_BOX_HEIGHT = 300

# Define the position and size of the text area within the list box
TEXT_AREA_X = LIST_BOX_X + 10
TEXT_AREA_Y = LIST_BOX_Y + 10
TEXT_AREA_WIDTH = LIST_BOX_WIDTH - 20
TEXT_AREA_HEIGHT = LIST_BOX_HEIGHT - 20

pygame.font.init()

#create the font
font = font = pygame.font.SysFont("Arial", 32)
base_font = pygame.font.Font(None, 32)
surr_text = font.render("Surrender", True, (0,0,0))
button_x = GAMEWIDTH + ((WIDTH - GAMEWIDTH) // 2) - (surr_text.get_width() // 2)
button_y = HEIGHT // 1.5 + 8
surr_rect = surr_text.get_rect()
surr_rect.x = button_x
surr_rect.y = button_y
class Game:
    
    def __init__(self):
            self.dragInit = True
            self.dragPiece = None
            self.valid_moves = None
    
    #show methods
    def show_bg(self, surface, brd, dragging, team, prevMoves):
        WHITE = (255, 255, 255)
        BLACK = (0,0,0)
        surface.fill(WHITE)
        brdMat = board_toMatrix(brd.fen())
        for row in range(ROWS):
            for col in range (COLS):
                if(row+col) % 2 == 0:
                    color = (235, 235, 200) #light
                else:
                    color = (120, 155, 90) #dark
                #gets position according to python chess positions
                brdPos = ((7-row)*8)+col
                targetPiece = None
                if(dragging and (brd.turn == team)):
                    if(self.dragInit):
                        self.dragPiece = mouse_position()
                        self.dragInit = False
                        if(self.dragPiece != -1):
                            targetPiece = brd.piece_at(self.dragPiece)
                            colo = brd.color_at(self.dragPiece)
                            if targetPiece is not None and colo == team:
                                self.valid_moves = [move.to_square for move in brd.legal_moves if move.from_square == self.dragPiece]
                    if(brdPos in self.valid_moves):
                        #green
                        color = (100,240,120)
                else:
                    self.dragInit = True
                    self.valid_moves = []

                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface,color,rect)
        for row in range(8):
            for col in range(8):
                x = col * SQSIZE
                y = row * SQSIZE
                #gets position according to python chess positions
                brdPos = ((7-row)*8)+col
                piece = brdMat[row][col]
                if(dragging):
                    if(brdPos == self.dragPiece):
                        mouse_pos = pygame.mouse.get_pos()
                        image_pos = (mouse_pos[0] - SQSIZE / 2, mouse_pos[1] - SQSIZE / 2)
                        if(brd.turn == chess.BLACK):
                            if piece == "p":
                                pawn_black.set_alpha(128)
                                surface.blit(pawn_black, image_pos)
                            elif piece == "r":
                                rook_black.set_alpha(128)
                                surface.blit(rook_black, image_pos)
                            elif piece == "n":
                                knight_black.set_alpha(128)
                                surface.blit(knight_black, image_pos)
                            elif piece == "b":
                                bishop_black.set_alpha(128)
                                surface.blit(bishop_black, image_pos)
                            elif piece == "q":
                                queen_black.set_alpha(128)
                                surface.blit(queen_black, image_pos)
                            elif piece == "k":
                                king_black.set_alpha(128)
                                surface.blit(king_black, image_pos)
                        else:
                            if piece == "P":
                                pawn_white.set_alpha(128)
                                surface.blit(pawn_white,image_pos)
                            elif piece == "R":
                                rook_white.set_alpha(128)
                                surface.blit(rook_white, image_pos)
                            elif piece == "N":
                                knight_white.set_alpha(128)
                                surface.blit(knight_white, image_pos)
                            elif piece == "B":
                                bishop_white.set_alpha(128)
                                surface.blit(bishop_white,image_pos)
                            elif piece == "Q":
                                queen_white.set_alpha(128)
                                surface.blit(queen_white,image_pos)
                            elif piece == "K":
                                king_white.set_alpha(128)
                                surface.blit(king_white,image_pos)
                else:
                    self.dragInit = True

                    
                if piece == "p":
                    pawn_black.set_alpha(256)
                    surface.blit(pawn_black, (x, y))
                elif piece == "r":
                    rook_black.set_alpha(256)
                    surface.blit(rook_black, (x, y))
                elif piece == "n":
                    knight_black.set_alpha(256)
                    surface.blit(knight_black, (x, y))
                elif piece == "b":
                    bishop_black.set_alpha(256)
                    surface.blit(bishop_black, (x, y))
                elif piece == "q":
                    queen_black.set_alpha(256)
                    surface.blit(queen_black, (x, y))
                elif piece == "k":
                    king_black.set_alpha(256)
                    surface.blit(king_black, (x, y))
                elif piece == "P":
                    pawn_white.set_alpha(256)
                    surface.blit(pawn_white,(x,y))
                elif piece == "R":
                    rook_white.set_alpha(256)
                    surface.blit(rook_white, (x, y))
                elif piece == "N":
                    knight_white.set_alpha(256)
                    surface.blit(knight_white, (x, y))
                elif piece == "B":
                    bishop_white.set_alpha(256)
                    surface.blit(bishop_white, (x, y))
                elif piece == "Q":
                    queen_white.set_alpha(256)
                    surface.blit(queen_white, (x, y))
                elif piece == "K":
                    king_white.set_alpha(256)
                    surface.blit(king_white, (x, y))
        


        pygame.draw.rect(surface, BLACK, surr_rect, 2)
        surface.blit(surr_text,(button_x,button_y))

        # Clear the list box
        pygame.draw.rect(surface, (255, 255, 255), (LIST_BOX_X, LIST_BOX_Y, LIST_BOX_WIDTH, LIST_BOX_HEIGHT))

        # Draw the text in the list boxes
        box_height = LIST_BOX_HEIGHT // 10
        for i, move in enumerate(prevMoves):
            text = f"{move[3]} - {move[1]} to {move[2]}"
            text_surface = font.render(text, True, (0, 0, 0))

            box_y = LIST_BOX_Y + (i * box_height)
            box_rect = pygame.Rect(LIST_BOX_X, box_y, LIST_BOX_WIDTH, box_height)
            pygame.draw.rect(surface, (200, 200, 200), box_rect, 1)

            text_x = box_rect.centerx - text_surface.get_width() // 2
            text_y = box_rect.centery - text_surface.get_height() // 2
            surface.blit(text_surface, (text_x, text_y))

        # Draw the list box
        pygame.draw.rect(surface, (0, 0, 0), (LIST_BOX_X, LIST_BOX_Y, LIST_BOX_WIDTH, LIST_BOX_HEIGHT), 2)



def int_to_square(n):
    row = n // 8
    col = n % 8
    letter = chr(ord('A') + row)
    number = col + 1
    return f"{letter}{number}"
    
def mouse_position():
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_ORIGIN
    if(mouse_pos[0] == 0):mouse_pos[0] = 1
    if(mouse_pos[1] == 0):mouse_pos[1] = 1
    y = (mouse_pos[0])//SQSIZE
    x = (mouse_pos[1]+BOARD_ORIGIN[1])//SQSIZE
    if(y>7):
        return -1
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

