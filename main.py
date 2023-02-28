import chess
import pygame
import sys

from const import *
from game import *
from board import *
from login import *
from menu import *
from host_menu import *

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.login = Login()
        self.menu = Menu()

    def mainloop(self):
        username = ""
        password = ""
        game = self.game
        login = self.login
        screen = self.screen
        board = initialise_board()
        curr_window = "login"
        print(board)
        while True:
            if(curr_window=="login"):
                login.show_screen(screen,username,password)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        # Check if the login button was clicked
                        if login_button.collidepoint(pygame.mouse.get_pos()):
                            print("Username: "+username)
                            print("Password: "+password)
                            curr_window = "menu"
                    elif event.type == pygame.KEYDOWN:
                        # Update the text of the username or password field
                        if username_field.collidepoint(pygame.mouse.get_pos()):
                            if event.key == pygame.K_BACKSPACE:
                                username = username[:-1]
                            else:
                                username += event.unicode
                        elif password_field.collidepoint(pygame.mouse.get_pos()):
                            if event.key == pygame.K_BACKSPACE:
                                password = password[:-1]
                            else:
                                password += event.unicode
            elif(curr_window=="game"):
                game.show_bg(screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouseDown = mouse_position()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        mouseUp = mouse_position()
                        print(mouseDown)
                        print(mouseUp)
                        make_move(mouseDown,mouseUp,board)
                        print(board)
            elif(curr_window=="menu"):
                Menu.show_screen(self,screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if (host_button.collidepoint(pygame.mouse.get_pos())):
                            curr_window = "hostMenu"
                        elif(quit_field.collidepoint(pygame.mouse.get_pos())):
                            pygame.quit()
                            sys.exit()
            elif(curr_window=="hostMenu"):
                HostMenu.show_screen(self,screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        #remember quit_field is from menu.py but has same location as back
                        if(quit_field.collidepoint(pygame.mouse.get_pos())):
                            curr_window = "menu"
                        
        
            pygame.display.update()


main = Main()
main.mainloop()