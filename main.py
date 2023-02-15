import chess
import pygame
import sys

from const import *
from game import *
from board import *

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        game = self.game
        screen = self.screen
        board = initialise_board()
        print(board)
        while True:
            game.show_bg(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseDown = mouse_position()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouseUp = mouse_position()
                    print("HERE")
                    print(mouseDown)
                    print(mouseUp)
                    print("DONE")
                    make_move(mouseDown,mouseUp,board)
                    print(board)
            #mouse_position()
            pygame.display.update()


main = Main()
main.mainloop()