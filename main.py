import chess
import pygame
import sys
import socket
import select
import re 

from const import *
from game import *
from board import *
from login import *
from menu import *
from host_menu import *
from client_menu import *


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
        board = None
        curr_window = "login"
        move_start = ""
        move_end = ""
        team_turn = "w"
        c = None
        s = None
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
            elif(curr_window=="menu"):
                Menu.show_screen(self,screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if (host_button.collidepoint(pygame.mouse.get_pos())):
                            connectStart = 0
                            curr_window = "hostMenu"
                        elif(quit_field.collidepoint(pygame.mouse.get_pos())):
                            pygame.quit()
                            sys.exit()
                        elif(join_field.collidepoint(pygame.mouse.get_pos())):
                            connectStart = 0
                            curr_window = "joinMenu"
            elif(curr_window=="hostMenu"):
                if(connectStart == 0):
                    HostMenu.show_screen(self,screen)
                    #START HOSTING, WAIT FOR CLIENT TO JOIN BEFORE STARTING GAME
                    host = 'local host'
                    port = 5000
                    s = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('', port))
                    #allows one client as opponent
                    s.listen(1)

                    sockets_list = [s]

                    connectStart = 1

                read_sockets, _, _ = select.select(sockets_list, [], [], 0)
                for sock in read_sockets:
                    if sock == s:
                        c, addr = s.accept()
                        print(f"Accepted connection from {addr}")
                        sockets_list.append(c)
                        
                HostMenu.show_screen(self,screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for conn in sockets_list:
                            conn.close()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        #remember quit_field is from menu.py but has same location as back button for this menu
                        if(quit_field.collidepoint(pygame.mouse.get_pos())):
                            curr_window = "menu"
                            for conn in sockets_list:
                                conn.close()
                        if(start_field.collidepoint(pygame.mouse.get_pos())):
                            try:
                                if(c is not None):
                                    board = initialise_board()
                                    c.send(board.fen().encode())
                                    curr_window = "host_game"
                            except NameError:
                                print("No Client")
            elif(curr_window == "host_game"):
                game.show_bg(screen,board)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for conn in sockets_list:
                            conn.close()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        move_start = mouse_position()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        move_end = mouse_position()
                        if(team_turn == "w"):
                            #if move valid and gets made
                            if(make_move(move_start,move_end,board)):
                                moveArr = str(move_start)+","+str(move_end)
                                c.send(moveArr.encode())
                                team_turn = "b"
                                print(board)
                if(team_turn=="b"):
                    #RECIEVE MOVE FROM CLIENT
                    ready_to_read, _, _ = select.select([c], [], [], 0.5)
                    if ready_to_read:
                        data = c.recv(1024)
                    else:
                        data = None

                    # use the received data
                    if data:
                        numbers =  re.findall(r'\d+', str(data))
                        numbers = [int(num) for num in numbers]
                        make_move(numbers[0],numbers[1],board)
                        print(board)
                        team_turn = "w"

            elif(curr_window == "joinMenu"):
                ClientMenu.show_screen(self,screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for conn in sockets_list:
                            conn.close()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        #remember quit_field is from menu.py but has same location as back button for this menu
                        if(quit_field.collidepoint(pygame.mouse.get_pos())):
                            curr_window = "menu"
                        elif(join_field.collidepoint(pygame.mouse.get_pos())):
                            connectStart = 0
                            host = 'local host'
                            port = 5000
                            s = socket.socket(socket.AF_INET,
                            socket.SOCK_STREAM)
                            print("Trying")
                            try:
                                s.connect(('127.0.0.1', port))
                                connectStart = 1
                                s.setblocking(False)
                                curr_window = "joinLobby"
                                print("Connected")
                            except ConnectionRefusedError as e:
                                print("Failed to connect to server:", e)
            elif(curr_window == "joinLobby"):
                HostMenu.show_screen(self,screen)
                
                # receive data in non-blocking mode
                ready_to_read, _, _ = select.select([s], [], [], 5)
                if ready_to_read:
                    data = s.recv(1024)
                else:
                    data = None

                # use the received data
                if data:
                    print(data)
                    board = initialise_board()
                    curr_window = "clientGame"
                else:
                    print("No data received")

            elif(curr_window == "clientGame"):
                game.show_bg(screen,board)
                for event in pygame.event.get():
                    print("events")
                    if event.type == pygame.QUIT:
                        for conn in sockets_list:
                            conn.close()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        move_start = mouse_position()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        move_end = mouse_position()
                        if(team_turn == "b"):
                            if(make_move(move_start,move_end,board)):
                                print("if...")
                                moveArr = str(move_start)+","+str(move_end)
                                #SEND MOVE ARR TO SERVER!!!
                                s.send(moveArr.encode())
                                team_turn = "w"
                                print(board)
                print("CLIENT GAME WAHOO")
                if(team_turn == "w"):
                    # receive data in non-blocking mode
                    ready_to_read, _, _ = select.select([s], [], [], 0.5)
                    if ready_to_read:
                        data = s.recv(1024)
                    else:
                        data = None

                    # use the received data
                    if data:
                        numbers =  re.findall(r'\d+', str(data))
                        numbers = [int(num) for num in numbers]
                        make_move(numbers[0],numbers[1],board)
                        team_turn = "b"
                        print(board)
            
            pygame.display.update()


main = Main()
main.mainloop()