import chess
import pygame
import sys

from const import *
from game import *
from board import *
from login import *

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.login = Login()

    def mainloop(self):

        game = self.game
        login = self.login
        screen = self.screen
        board = initialise_board()
        print(board)
        while True:
            login.show_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Check if the login button was clicked
                    if login_button.collidepoint(pygame.mouse.get_pos()):
                        print("Login button clicked!")
            pygame.display.update()


main = Main()
main.mainloop()