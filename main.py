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
        username = ""
        password = ""
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
                        print("Username: "+username)
                        print("Password: "+password)
                elif event.type == pygame.KEYDOWN:
                    # Update the text of the username or password field
                    if username_field.collidepoint(pygame.mouse.get_pos()):
                        print("MMMM")
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        else:
                            username += event.unicode
                    elif password_field.collidepoint(pygame.mouse.get_pos()):
                        print("HAAA")
                        if event.key == pygame.K_BACKSPACE:
                            password = password
                        else:
                            password += event.unicode


            pygame.display.update()


main = Main()
main.mainloop()