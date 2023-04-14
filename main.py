import chess
import pygame
import sys
import socket
import select
import re 
import tkinter as tk
import sqlite3
import smtplib
import pyttsx3
import threading
from email.mime.text import MIMEText

from const import *
from game import *
from board import *
from login import *
from menu import *
from host_menu import *
from client_menu import *
from end_screen import *
from join_lobby import *
from settings import *

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.login = Login()
        self.menu = Menu()

    def mainloop(self):
        username = ""
        password = ""
        FEN = ""
        login = self.login
        screen = self.screen
        curr_window = "login"
        incorrectPass = False
        passAuth = ""
        email = ""
        audioFeedback = False
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-50)
        base_font = pygame.font.Font(None, 32)

        while True:
            if(curr_window=="login"):
                login.show_screen(screen,username,password)
                if(incorrectPass):
                    text_login = base_font.render("Incorrect Username or password", True, COLOUR_THREE)
                    screen.blit(text_login, (password_field.x, password_field.y+35))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        # Check if the login button was clicked
                        if login_button.collidepoint(pygame.mouse.get_pos()):
                            conn = sqlite3.connect('users.db')

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
                        if reg_button.collidepoint(pygame.mouse.get_pos()):
                            username = ""
                            password = ""
                            username_active = 0
                            user_taken = False
                            passMatch = True
                            curr_window = "register"
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
                            surrender = False
                            board_list = []  
                            sockets_list = []
                            c = None
                            s = None
                            move_start = ""
                            move_end = ""
                            team_turn = "w"
                            dragging = False
                            board = None
                            ipInput = ""
                            game = Game(username)
                            curr_window = "hostMenu"
                            loop = True
                            numTurns = 0
                            toggleBoard = False
                        elif(quit_field.collidepoint(pygame.mouse.get_pos())):
                            pygame.quit()
                            sys.exit()
                        elif(join_field.collidepoint(pygame.mouse.get_pos())):
                            connectStart = 0
                            surrender = False
                            board_list = []  
                            sockets_list = []
                            c = None
                            s = None
                            move_start = ""
                            move_end = ""
                            team_turn = "w"
                            dragging = False
                            board = None
                            ipInput = ""
                            game = Game(username)
                            curr_window = "joinMenu"
                            loop = True
                            numTurns = 0
                            toggleBoard = False
                        elif(account_button.collidepoint(pygame.mouse.get_pos())):
                            selected_button = 0
                            visible = 0
                            settings = Settings(audioFeedback,username)
                            curr_window = "acc_settings"
                            # Open the database connection
                            conn = sqlite3.connect('users.db')

                            # Create a cursor object
                            cursor = conn.cursor()

                            # Get the win, loss, and draw columns for the current user
                            cursor.execute("SELECT wins, losses, draws FROM user_stats WHERE username = ?", (username,))
                            results = cursor.fetchone()
                            wins, losses, draws = results

                            # Close the database connection
                            conn.close()
            elif(curr_window=="hostMenu"):
                if(connectStart == 0):
                    #START HOSTING, WAIT FOR CLIENT TO JOIN BEFORE STARTING GAME
                    host = socket.gethostname()
                    ip = socket.gethostbyname(host)
                    HostMenu.show_screen(self,screen,FEN,ip)
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
                        
                HostMenu.show_screen(self,screen,FEN,ip)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        #remember quit_field is from menu.py but has same location as back button for this menu
                        if(quit_field.collidepoint(pygame.mouse.get_pos())):
                            curr_window = "menu"
                            for con in sockets_list:
                                con.close()
                                sockets_list.remove(con)
                        if(start_field.collidepoint(pygame.mouse.get_pos())):
                            try:
                                if(c is not None):
                                    board = initialise_board(FEN)
                                    c.send(board.fen().encode())
                                    curr_window = "host_game"
                            except NameError:
                                print("No Client")
                    elif event.type == pygame.KEYDOWN:
                        #UPDATE REN FIELD
                        if host_field.collidepoint(pygame.mouse.get_pos()):
                            if event.key == pygame.K_BACKSPACE:
                                FEN = FEN[:-1]
                            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                # Check if CTRL+V is pressed
                                root = tk.Tk()
                                root.withdraw()
                                clipboard_text = root.clipboard_get()
                                if clipboard_text:
                                    # If clipboard has text, append it to REN
                                    FEN += clipboard_text
                            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                # Check if CTRL+Z is pressed
                                FEN = ''
                            else:
                                FEN += event.unicode


            elif(curr_window == "host_game"):
                game.show_bg(screen,board,dragging,chess.WHITE, board_list)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        dragging = True
                        move_start = mouse_position()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if surr_rect.collidepoint(pygame.mouse.get_pos()) and team_turn == "w":
                            surrender = True
                        dragging = False
                        move_end = mouse_position()
                        mouse_pos = pygame.mouse.get_pos()
                        for i, move in enumerate(board_list):
                            box_y = LIST_BOX_Y + (i * (LIST_BOX_HEIGHT // 10))
                            box_rect = pygame.Rect(LIST_BOX_X, box_y, LIST_BOX_WIDTH, (LIST_BOX_HEIGHT // 10))
                            if box_rect.collidepoint(mouse_pos):
                                tempWindow = tk.Tk()
                                tempWindow.withdraw()
                                tempWindow.clipboard_clear()
                                tempWindow.clipboard_append(board_list[i][0])
                                tempWindow.destroy()
                        if(team_turn == "w"):
                            if(surrender):
                                board.result = "0-1"
                                surrString = "s"
                                c.send(surrString.encode())
                                curr_window = "endScreen"
                            #if move valid and gets made
                            promote = make_move(move_start,move_end,board,screen,None)
                            if(promote):
                                numTurns += 1
                                listApp = board.fen()
                                board_list.append([listApp,int_to_square(move_start),int_to_square(move_end),board.piece_at(move_end)])
                                if len(board_list) > 10:
                                    board_list.pop(0)
                                    for i in range(len(board_list)):
                                        board_list[i][0] = i
                                moveArr = str(move_start)+","+str(move_end)+","+str(promote)
                                c.send(moveArr.encode())
                                moveSay = "White moves "+int_to_square(move_start)+" to "+int_to_square(move_end)                
                                def say_thread():
                                    # Check if the engine is already running a loop
                                    if not engine._inLoop:
                                        engine.say(moveSay)
                                        engine.runAndWait()
                                if(audioFeedback):
                                    thread = threading.Thread(target = say_thread)
                                    thread.start()
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
                    ready_to_read, _, _ = select.select([c], [], [], 0.1)
                    if ready_to_read:
                        try:
                            data = c.recv(1024)
                        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                            # If the client has closed the connection, a BrokenPipeError will be raised
                            print('Client closed the connection')
                            for con in sockets_list:
                                con.close()
                                sockets_list.remove(con)
                            data = None
                            curr_window = "connection_cut"
                    else:
                        data = None

                    # Check if the other side has closed the connection
                    try:
                        c.send(b'ping')
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                        # If the client has closed the connection, a BrokenPipeError, ConnectionResetError, or ConnectionAbortedError will be raised
                        print('Client closed the connection')
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        curr_window = "connection_cut"
                    if data:
                        data = data.replace(b"ping", b"")
                    # use the received data
                    if data:
                        dataDec = data.decode('utf-8').strip("b'").strip("'")
                        if(dataDec=='s'):
                            board.result = "1-0"
                            curr_window = "endScreen"
                        else:
                            numbers =  re.findall(r'\d+', str(data))
                            numbers = [int(num) for num in numbers]
                            make_move(numbers[0],numbers[1],board,screen,numbers[2])
                            moveSay = "Black moves "+int_to_square(numbers[0])+" to "+int_to_square(numbers[1])                
                            def say_thread():
                                # Check if the engine is already running a loop
                                if not engine._inLoop:
                                    # If not, start a new loop and speak the text asynchronously
                                    engine.say(moveSay)
                                    engine.runAndWait()
                            if(audioFeedback):
                                thread = threading.Thread(target = say_thread)
                                thread.start()
                            listApp = board.fen()
                            board_list.append([listApp,int_to_square(numbers[0]),int_to_square(numbers[1]),board.piece_at(numbers[1])])
                            if len(board_list) > 10:
                                board_list.pop(0)
                                for i in range(len(board_list)):
                                    board_list[i][0] = i
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
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
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
                JoinLobby.show_screen(self,screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if lobback_button.collidepoint(pygame.mouse.get_pos()):
                            for con in sockets_list:
                                con.close()
                                sockets_list.remove(con)
                            curr_window = "joinMenu"

                # receive data in non-blocking mode
                ready_to_read, _, _ = select.select([s], [], [], 0.1)
                if ready_to_read:
                    data = s.recv(1024)
                else:
                    data = None

                # use the received data
                if data:
                    data = data.decode('utf-8').strip("b'").strip("'")
                    board = initialise_board(data)
                    curr_window = "clientGame"
                else:
                    print("No data received")

            elif(curr_window == "clientGame"):
                game.show_bg(screen,board,dragging,chess.BLACK, board_list)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        dragging = True
                        move_start = mouse_position()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if surr_rect.collidepoint(pygame.mouse.get_pos()) and team_turn == "b":
                            surrender = True
                        dragging = False
                        move_end = mouse_position()
                        if(team_turn == "b"):
                            if(surrender):
                                board.result = "1-0"
                                surrString = "s"
                                s.send(surrString.encode())
                                curr_window = "endScreen"
                            promote = make_move(move_start,move_end,board,screen,None)
                            # 0 if invalid, 1 if no promotion, 2-5 to designate promotion
                            if(promote):
                                numTurns += 1
                                listApp = board.fen()
                                board_list.append([listApp,int_to_square(move_start),int_to_square(move_end),board.piece_at(move_end)])
                                if len(board_list) > 10:
                                    board_list.pop(0)
                                    for i in range(len(board_list)):
                                        board_list[i][0] = i
                                moveArr = str(move_start)+","+str(move_end)+","+str(promote)
                                moveSay = "Black moves "+int_to_square(move_start)+" to "+int_to_square(move_end)                
                                def say_thread():
                                    # Check if the engine is already running a loop
                                    if not engine._inLoop:
                                        engine.say(moveSay)
                                        engine.runAndWait()
                                if(audioFeedback):
                                    thread = threading.Thread(target = say_thread)
                                    thread.start()
                                #SEND MOVE ARR TO SERVER!!!
                                s.send(moveArr.encode())
                                loop = True
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
                if(team_turn == "w"):
                    # receive data in non-blocking mode
                    ready_to_read, _, _ = select.select([s], [], [], 0.1)
                    if ready_to_read:
                        try:
                            data = s.recv(1024)
                        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                            # If the client has closed the connection, a BrokenPipeError will be raised
                            print('Client closed the connection')
                            for con in sockets_list:
                                con.close()
                                sockets_list.remove(con)
                            data = None
                            curr_window = "connection_cut"
                    else:
                        data = None

                    # Check if the other side has closed the connection
                    try:
                        s.send(b'ping')
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                        # If the client has closed the connection, a BrokenPipeError, ConnectionResetError, or ConnectionAbortedError will be raised
                        print('Client closed the connection')
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        curr_window = "connection_cut"
                    if(data):
                        data = data.replace(b"ping", b"")
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
                            print("HEEEERE")
                            print(data)
                            make_move(numbers[0],numbers[1],board,screen,numbers[2])
                            listApp = board.fen()
                            moveSay = "White moves "+int_to_square(numbers[0])+" to "+int_to_square(numbers[1])                
                            def say_thread():
                                # Check if the engine is already running a loop
                                if not engine._inLoop:
                                    engine.say(moveSay)
                                    engine.runAndWait()
                            if(audioFeedback):
                                thread = threading.Thread(target = say_thread)
                                thread.start()
                            board_list.append([listApp,int_to_square(numbers[0]),int_to_square(numbers[1]),board.piece_at(numbers[1])])
                            if len(board_list) > 10:
                                board_list.pop(0)
                                for i in range(len(board_list)):
                                    board_list[i][0] = i
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
            elif(curr_window=="endScreen"):
                if(toggleBoard):
                    game.show_bg(screen,board,dragging,chess.BLACK, board_list)
                else:
                    EndScreen.show_screen(self,screen,board,numTurns,toggleBoard)
                for con in sockets_list:
                    con.close()
                    sockets_list.remove(con)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if toggleBoard:
                            toggleBoard = False
                        elif continue_button.collidepoint(pygame.mouse.get_pos()):
                            curr_window = "menu"
                        elif toggle_button.collidepoint(pygame.mouse.get_pos()):
                            toggleBoard = True
            elif(curr_window == "connection_cut"):
                #window displays if there is an unexpected loss of connection
                screen.fill((255,255,255))
                cont_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
                font = font = pygame.font.SysFont("Arial", 32)
                base_font = pygame.font.Font(None, 32)
                pygame.draw.rect(screen, (0,0,0), continue_button, 2)
                text1 = font.render("Continue", True, (0,0,0))
                screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 1.5 + 8))
                text2 = font.render("Opponent Disconnected: Connection Closed", True, (0,0,0))
                screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 8))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if cont_button.collidepoint(pygame.mouse.get_pos()):
                            curr_window = "menu"   
            elif(curr_window == "register"):
                login.register(screen,username,password,passAuth,email)   
                if(user_taken):
                    base_font = pygame.font.Font(None, 22)
                    text_taken= base_font.render("Username Taken or Invalid", True, (255,0,0))
                    screen.blit(text_taken, (REGusername_field.x, REGusername_field.y+35))
                if(not passMatch):
                    base_font = pygame.font.Font(None, 22)
                    text_pass= base_font.render("Passwords Dont Match", True, (255,0,0))
                    screen.blit(text_pass, (REGpassAuth_field.x, REGpassAuth_field.y+35))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Check if the user clicked on the username field
                        username_active = 0
                        if REGusername_field.collidepoint(event.pos):
                            username_active = 1
                        elif REGpassword_field.collidepoint(event.pos):
                            username_active = 2
                        elif REGpassAuth_field.collidepoint(event.pos):
                            username_active = 3
                        elif REGemail_field.collidepoint(event.pos):
                            username_active = 4
                        elif back_rect.collidepoint(event.pos):
                            username_active = 0
                            username = ""
                            password = ""
                            passAuth = ""
                            email = ""
                            curr_window = "login"
                        elif register_button.collidepoint(event.pos): 
                            regFail = False                           
                            # check if email is in valid format
                            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                                print("not valid email format")
                                regFail = True
                            if password != passAuth:
                                passMatch = False
                                regFail = True
                            else: 
                                passMatch = True
                            smtp_server = 'smtp.gmail.com'
                            smtp_port = 587
                            smtp_username = 'oppoppoppopop@gmail.com'
                            smtp_password = 'rocket99'
                            
                            message = f'Your username is {username} and your password is {password}.'
                            msg = MIMEText(message)
                            msg['Subject'] = 'Your Login Information'
                            msg['From'] = smtp_username
                            msg['To'] = smtp_username
                            
                            with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                                smtp.ehlo()
                                smtp.starttls()
                                smtp.login(smtp_username, smtp_password)
                                smtp.sendmail(smtp_username, smtp_username, msg.as_string())
                                print("sent")


                            conn = sqlite3.connect('users.db')
                            curr = conn.cursor()
                            curr.execute("SELECT * FROM user_stats WHERE username = ?", (username,))
                            row = curr.fetchone()
                            if not row:
                                curr.execute("INSERT INTO user_stats (username, password, wins, losses, draws) VALUES (?, ?, ?, ?, ?)", (username, password, 0, 0, 0))
                                conn.commit()
                            else:
                                user_taken = True
                                regFail = True
                            conn.close()

                    elif event.type == pygame.KEYDOWN:
                        # Check if the user typed a character
                        if username_active == 1:
                            if event.key == pygame.K_BACKSPACE:
                                username = username[:-1]
                            else:
                                username += event.unicode
                        if username_active == 2:
                            if event.key == pygame.K_BACKSPACE:
                                password = password[:-1]
                            else:
                                password += event.unicode
                        if username_active == 3:
                            if event.key == pygame.K_BACKSPACE:
                                passAuth = passAuth[:-1]
                            else:
                                passAuth += event.unicode
                        if username_active == 4:
                            if event.key == pygame.K_BACKSPACE:
                                email = email[:-1]
                            else:
                                email += event.unicode
            elif(curr_window == "acc_settings"):
                settings.show_screen(screen, wins, losses, draws,selected_button,audioFeedback)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if colour_wheel_rect.collidepoint(pygame.mouse.get_pos()) and visible:
                            update_color(screen,selected_button,username)
                        elif colour_one_rect.collidepoint(pygame.mouse.get_pos()):
                            visible = 1
                            selected_button = 1
                        elif colour_two_rect.collidepoint(pygame.mouse.get_pos()):
                            visible = 1
                            selected_button = 2
                        elif audio_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                            if(audioFeedback):
                                audioFeedback = 0
                            else:
                                audioFeedback = 1
                        elif sett_quit_field.collidepoint(pygame.mouse.get_pos()):
                            curr_window = "menu"
                        else: 
                            selected_button = 0
                            visible = 0
                        


            pygame.display.update()


main = Main()
main.mainloop()