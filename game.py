import pygame
from const import *


class Game:
    
    def __init__(self):
        pass

    #show methods

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range (COLS):
                if(row+col) % 2 == 0:
                    color = (234, 235, 200) #light
                else:
                    color = (119, 154, 88) #dark
                
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface,color,rect)

    
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

