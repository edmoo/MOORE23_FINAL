import chess
import pygame
import sys
import socket
import select
import re 
import tkinter as tk
import sqlite3

from const import *
from game import *
from board import *
from login import *
from menu import *
from host_menu import *
from client_menu import *
from end_screen import *
from join_lobby import *


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
        REN = ""
        ipInput = ""
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
        dragging = False
        sockets_list = []
        incorrectPass = False
        surrender = False
        board_list = []
        while True:
            if(curr_window=="login"):
                login.show_screen(screen,username,password)
                if(incorrectPass):
                    text_login = base_font.render("Incorrect Username or password", True, (255,0,0))
                    screen.blit(text_login, (password_field.x, password_field.y+35))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        # Check if the login button was clicked
                        if login_button.collidepoint(pygame.mouse.get_pos()):
                            conn = sqlite3.connect('user_data.db')

                            # create a cursor object to execute SQL commands
                            curr = conn.cursor()

                            # retrieve the entry from the user_stats table with the matching username
                            curr.execute("SELECT * FROM user_stats WHERE username = ?", (username,))
                            row = curr.fetchone()

                            # check if a row was returned and if the password matches
                            if row and row[1] == password:
                                curr_window = "menu"
                            else:
                                incorrectPass = True
                                print("Incorrect username or password.")

                            conn.close()
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
                    HostMenu.show_screen(self,screen,REN)
                    #START HOSTING, WAIT FOR CLIENT TO JOIN BEFORE STARTING GAME
                    host = socket.gethostname()
                    ip = socket.gethostbyname(host)
                    port = 5000
                    print(ip)
                    s = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((ip, port))
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
                        
                HostMenu.show_screen(self,screen,REN)
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
                                    board = initialise_board(REN)
                                    c.send(board.fen().encode())
                                    curr_window = "host_game"
                            except NameError:
                                print("No Client")
                    elif event.type == pygame.KEYDOWN:
                        #UPDATE REN FIELD
                        if host_field.collidepoint(pygame.mouse.get_pos()):
                            if event.key == pygame.K_BACKSPACE:
                                REN = REN[:-1]
                            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                # Check if CTRL+V is pressed
                                root = tk.Tk()
                                root.withdraw()
                                clipboard_text = root.clipboard_get()
                                if clipboard_text:
                                    # If clipboard has text, append it to REN
                                    REN += clipboard_text
                            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                # Check if CTRL+Z is pressed
                                REN = ''
                            else:
                                REN += event.unicode


            elif(curr_window == "host_game"):
                game.show_bg(screen,board,dragging,chess.WHITE, board_list)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for conn in sockets_list:
                            conn.close()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        dragging = True
                        move_start = mouse_position()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if surr_rect.collidepoint(pygame.mouse.get_pos()):
                            surrender = True
                            print("surrender")
                        dragging = False
                        move_end = mouse_position()
                        if(team_turn == "w"):
                            if(surrender):
                                board.result = "0-1"
                                surrString = "s"
                                c.send(surrString.encode())
                                curr_window = "endScreen"
                            #if move valid and gets made
                            if(make_move(move_start,move_end,board)):
                                listApp = board.fen()
                                board_list.append([listApp,move_start,move_end])
                                if len(board_list) > 10:
                                    board_list.pop(0)
                                    for i in range(len(board_list)):
                                        board_list[i][0] = i
                                moveArr = str(move_start)+","+str(move_end)
                                c.send(moveArr.encode())
                                team_turn = "b"
                            if(board.outcome()):
                                outcome = board.outcome()
                                if(outcome.winner==chess.WHITE):
                                    board.result = "1-0"
                                elif(outcome.winner==chess.BLACK):
                                    board.result = "0-1"
                                else:
                                    board.result = "1/2-1/2"
                                curr_window = "endScreen" 
                if(team_turn=="b"):
                    #RECIEVE MOVE FROM CLIENT
                    ready_to_read, _, _ = select.select([c], [], [], 0.5)
                    if ready_to_read:
                        try:
                            data = c.recv(1024)
                        except BrokenPipeError:
                            # If the client has closed the connection, a BrokenPipeError will be raised
                            print('Client closed the connection')
                            break
                    else:
                        data = None

                    # use the received data
                    if data:
                        dataDec = data.decode('utf-8').strip("b'").strip("'")
                        if(dataDec=='s'):
                            print("enemy surrender!1")
                            board.result = "1-0"
                            curr_window = "endScreen"
                        else:
                            numbers =  re.findall(r'\d+', str(data))
                            numbers = [int(num) for num in numbers]
                            make_move(numbers[0],numbers[1],board)
                            listApp = board.fen()
                            board_list.append([listApp,numbers[0],numbers[1]])
                            if len(board_list) > 10:
                                board_list.pop(0)
                                for i in range(len(board_list)):
                                    board_list[i][0] = i
                            print(board)
                            team_turn = "w"
                    if(board.outcome()):
                        outcome = board.outcome()
                        if(outcome.winner==chess.WHITE):
                            board.result = "1-0"
                        elif(outcome.winner==chess.BLACK):
                            board.result = "0-1"
                        else:
                            board.result = "1/2-1/2"
                        curr_window = "endScreen"

            elif(curr_window == "joinMenu"):
                ClientMenu.show_screen(self,screen,ipInput)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for conn in sockets_list:
                            conn.close()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if(back_button.collidepoint(pygame.mouse.get_pos())):
                            curr_window = "menu"
                        elif(join_field.collidepoint(pygame.mouse.get_pos())):
                            connectStart = 0
                            port = 5000
                            s = socket.socket(socket.AF_INET,
                            socket.SOCK_STREAM)
                            print("Trying")
                            try:
                                parts = ipInput.split(".")
                                if len(parts) != 4:
                                    raise ValueError
                                for part in parts:
                                    if not 0 <= int(part) <= 255:
                                        raise ValueError
                                socket.inet_aton(ipInput)
                                s.connect((ipInput, port))
                                connectStart = 1
                                s.setblocking(False)
                                curr_window = "joinLobby"
                                print("Connected")
                            except ConnectionRefusedError as e:
                                print("Failed to connect to server:", e)
                            except (socket.error, ValueError):
                                print("Invalid IP")
                    elif event.type == pygame.KEYDOWN:
                        #UPDATE REN FIELD
                        if client_field.collidepoint(pygame.mouse.get_pos()):
                            if event.key == pygame.K_BACKSPACE:
                                ipInput = ipInput[:-1]
                            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                # Check if CTRL+V is pressed
                                root = tk.Tk()
                                root.withdraw()
                                clipboard_text = root.clipboard_get()
                                if clipboard_text:
                                    # If clipboard has text, append it to REN
                                    ipInput += clipboard_text
                            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                # Check if CTRL+Z is pressed
                                ipInput = ''
                            else:
                                ipInput += event.unicode
            elif(curr_window == "joinLobby"):
                JoinLobby.show_screen(self,screen
                                      )
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for conn in sockets_list:
                            conn.close()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if lobback_button.collidepoint(pygame.mouse.get_pos()):
                            for conn in sockets_list:
                                conn.close()
                            curr_window = "joinMenu"

                # receive data in non-blocking mode
                ready_to_read, _, _ = select.select([s], [], [], 5)
                if ready_to_read:
                    data = s.recv(1024)
                else:
                    data = None

                # use the received data
                if data:
                    data = data.decode('utf-8').strip("b'").strip("'")
                    print(data)
                    board = initialise_board(data)
                    curr_window = "clientGame"
                else:
                    print("No data received")

            elif(curr_window == "clientGame"):
                game.show_bg(screen,board,dragging,chess.BLACK, board_list)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for conn in sockets_list:
                            conn.close()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        dragging = True
                        move_start = mouse_position()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if surr_rect.collidepoint(pygame.mouse.get_pos()):
                            surrender = True
                        dragging = False
                        move_end = mouse_position()
                        if(team_turn == "b"):
                            if(surrender):
                                board.result = "1-0"
                                surrString = "s"
                                s.send(surrString.encode())
                                curr_window = "endScreen"
                            if(make_move(move_start,move_end,board)):
                                listApp = board.fen()
                                board_list.append([listApp,move_start,move_end])
                                if len(board_list) > 10:
                                    board_list.pop(0)
                                    for i in range(len(board_list)):
                                        board_list[i][0] = i
                                moveArr = str(move_start)+","+str(move_end)
                                #SEND MOVE ARR TO SERVER!!!
                                s.send(moveArr.encode())
                                team_turn = "w"
                                if(board.outcome()):
                                    outcome = board.outcome()
                                    if(outcome.winner==chess.WHITE):
                                        board.result = "1-0"
                                    elif(outcome.winner==chess.BLACK):
                                        board.result = "0-1"
                                    else:
                                        board.result = "1/2-1/2"
                                    print("checkmate")
                                    curr_window = "endScreen"
                                print(board)
                if(team_turn == "w"):
                    # receive data in non-blocking mode
                    ready_to_read, _, _ = select.select([s], [], [], 0.5)
                    if ready_to_read:
                        data = s.recv(1024)
                    else:
                        data = None

                    # use the received data
                    if data:
                        dataDec = data.decode('utf-8').strip("b'").strip("'")
                        if(dataDec=='s'):
                            print("Opponent surrender!")
                            board.result = "0-1"
                            curr_window = "endScreen"
                        else:
                            numbers =  re.findall(r'\d+', str(data))
                            numbers = [int(num) for num in numbers]
                            listApp = board.fen()
                            board_list.append([listApp,numbers[0],numbers[1]])
                            if len(board_list) > 10:
                                board_list.pop(0)
                                for i in range(len(board_list)):
                                    board_list[i][0] = i
                            make_move(numbers[0],numbers[1],board)
                            team_turn = "b"
                            print(board)

                    if(board.outcome()):
                        outcome = board.outcome()
                        if(outcome.winner==chess.WHITE):
                            board.result = "1-0"
                        elif(outcome.winner==chess.BLACK):
                            board.result = "0-1"
                        else:
                            board.result = "1/2-1/2"
                        curr_window = "endScreen"
            elif(curr_window=="endScreen"):
                EndScreen.show_screen(self,screen,board)
                print("ENDSCREEN!")
            
            pygame.display.update()


main = Main()
main.mainloop()