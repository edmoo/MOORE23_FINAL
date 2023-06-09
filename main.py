import os
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
import speech_recognition as sr
from pocketsphinx import LiveSpeech, get_model_path
import pyaudio
import hashlib
import requests

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
    
    def add_stats(self, username, column):
        db_path = os.path.join(os.path.dirname(__file__), 'users.db')
        conn = sqlite3.connect(db_path)        
        curr = conn.cursor()
        curr.execute("UPDATE user_stats SET {} = {} + 1 WHERE username = ?".format(column, column), (username,))
        conn.commit()
        #close the cursor and database connection
        curr.close()
        conn.close()

    def mainloop(self):
        username = ""
        password = ""
        FEN = ""
        login = self.login
        screen = self.screen
        curr_window = "login"
        incorrectPass = False
        passAuth = ""
        user_email = ""
        audioFeedback = False
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-50)
        base_font = pygame.font.Font(None, 32)
        valid_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@.!#$%&\'*+-/=?^_`{ | }~'
        valid_ip_chars = '1234567890.'
        hex_chars = '0123456789ABCDEFabcdef'
        #voice related
        voice_enabled = False     
        mov = ["","","",""]
        number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        letter_words = ["a","b","c","d","e","f","g","h"]
        username_active = 0
        button = 0
        response = requests.get('https://api.ipify.org?format=json')
        my_ip = response.json()['ip']
        print(my_ip)
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
                        if login_button.collidepoint(pygame.mouse.get_pos()):
                            button = 3
                        elif reg_button.collidepoint(pygame.mouse.get_pos()):
                            button = 4
                        elif username_field.collidepoint(pygame.mouse.get_pos()):
                            username_active = 1
                        elif password_field.collidepoint(pygame.mouse.get_pos()):
                            username_active = 2
                        else:
                            username_active = 0

                    elif event.type == pygame.KEYDOWN:
                        # Update the text of the username or password field
                        if username_active == 1:
                            if event.key == pygame.K_BACKSPACE:
                                username = username[:-1]
                            elif(len(username) < 24 and event.unicode in valid_characters):
                                username += event.unicode
                        elif username_active == 2:
                            if event.key == pygame.K_BACKSPACE:
                                password = password[:-1]
                            elif(len(password) < 35 and event.unicode in valid_characters):
                                password += event.unicode
                        elif event.key == pygame.K_3:
                            button = 3
                        elif event.key == pygame.K_4:
                            button = 4
                        if event.key == pygame.K_RETURN:
                            username_active = 0
                        elif event.key == pygame.K_1 and username_active == 0:
                            username_active = 1
                        elif event.key == pygame.K_2 and username_active == 0:
                            username_active = 2
                if(button == 3):
                    button = 0
                    db_path = os.path.join(os.path.dirname(__file__), 'users.db')
                    conn = sqlite3.connect(db_path)
                    # create a cursor object to execute SQL commands
                    curr = conn.cursor()

                    # retrieve the entry from the user_stats table with the matching username
                    curr.execute("SELECT * FROM user_stats WHERE username = ?", (username,))
                    row = curr.fetchone()

                    # check if a row was returned and if the password matches
                    password_hashed = hashlib.sha256(password.encode()).hexdigest()

                    if row and row[1] == password_hashed:
                        pygame.display.set_caption("Main Menu")
                        curr_window = "menu"
                    else:
                        incorrectPass = True

                    conn.close()
                elif(button == 4):
                    button = 0
                    username = ""
                    password = ""
                    username_active = 0
                    user_taken = False
                    passMatch = True
                    selected_button = 0
                    pygame.display.set_caption("Register Menu")
                    curr_window = "register"

            elif(curr_window=="menu"):
                Menu.show_screen(self,screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if (host_button.collidepoint(pygame.mouse.get_pos())):
                            button = 1
                        elif(quit_field.collidepoint(pygame.mouse.get_pos())):
                            button = 4
                        elif(join_field.collidepoint(pygame.mouse.get_pos())):
                            button = 3
                        elif(account_button.collidepoint(pygame.mouse.get_pos())):
                            button = 2
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            button = 1
                        elif event.key == pygame.K_2:
                            button = 2
                        elif event.key == pygame.K_3:
                            button = 3
                        elif event.key == pygame.K_4:
                            button = 4
                if(button == 1):
                    button = 0
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
                    pygame.display.set_caption("Host Menu")
                    curr_window = "hostMenu"
                    loop = True
                    numTurns = 0
                    toggleBoard = False
                    selected_square = -1
                elif(button == 2):
                    button = 0
                    selected_button = 0
                    visible = 0
                    settings = Settings(audioFeedback,username)
                    pygame.display.set_caption("Account Settings")
                    h_code = ""
                    curr_window = "acc_settings"
                    # Open the database connection
                    db_path = os.path.join(os.path.dirname(__file__), 'users.db')
                    conn = sqlite3.connect(db_path)
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Get the win, loss, and draw columns for the current user
                    cursor.execute("SELECT wins, losses, draws FROM user_stats WHERE username = ?", (username,))
                    results = cursor.fetchone()
                    wins, losses, draws = results

                    # Close the database connection
                    conn.close()
                elif(button == 3):
                    button = 0
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
                    pygame.display.set_caption("Join Menu")
                    curr_window = "joinMenu"
                    loop = True
                    numTurns = 0
                    toggleBoard = False
                    selected_square = -1
                elif(button == 4):
                    button = 0
                    pygame.quit()
                    sys.exit()
                
    
            elif(curr_window=="hostMenu"):
                if(connectStart == 0):
                    client_joined = False
                    #START HOSTING, WAIT FOR CLIENT TO JOIN BEFORE STARTING GAME
                    host = socket.gethostname()
                    ip = socket.gethostbyname(host)
                    HostMenu.show_screen(self,screen,FEN,ip,client_joined)
                    port = 5000
                    s = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('0.0.0.0', port))
                    #allows one client as opponent
                    s.listen(1)

                    sockets_list = [s]

                    connectStart = 1

                read_sockets, _, _ = select.select(sockets_list, [], [], 0)
                HostMenu.show_screen(self,screen,FEN,ip,client_joined)
                for sock in read_sockets:
                    if sock == s:
                        c, addr = s.accept()
                        sockets_list.append(c)
                        client_joined = True                  
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
                            button = 3
                        if(start_field.collidepoint(pygame.mouse.get_pos())):
                            button = 2
                        if host_field.collidepoint(pygame.mouse.get_pos()):
                            username_active = 1
                        else:
                            username_active = 0
                    elif event.type == pygame.KEYDOWN:
                        #deactivates typing
                        if(event.key == pygame.K_RETURN):
                            username_active = 0
                        if username_active == 1:
                            if event.key == pygame.K_BACKSPACE:
                                FEN = FEN[:-1]
                            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                #check if CTRL+V is pressed
                                root = tk.Tk()
                                root.withdraw()
                                clipboard_text = root.clipboard_get()
                                if clipboard_text and len(clipboard_text) <= 90:
                                    #if clipboard has text, append it to REN
                                    FEN += clipboard_text
                                    FEN = FEN.strip()
                            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                #check if CTRL+Z is pressed
                                FEN = ''
                            elif(len(FEN) < 35 and event.unicode in valid_characters):
                                FEN += event.unicode
                        #after so that 1 isnt immediately input into text
                        if(username_active == 0):
                            if(event.key == pygame.K_1):
                                username_active = 1
                            elif(event.key == pygame.K_2):
                                button = 2
                            elif(event.key == pygame.K_3):
                                button = 3
            if(button == 2):
                button = 0
                try:
                    if(c is not None):
                        board = initialise_board(FEN)
                        c.send(board.fen().encode())
                        move_start = -1
                        move_end = -1
                        pygame.display.set_caption("Hosting Game")
                        curr_window = "host_game"
                except NameError:
                    print("No Client")
            elif(button == 3):
                button = 0
                pygame.display.set_caption("Main Menu")
                curr_window = "menu"
                for con in sockets_list:
                    con.close()
                    sockets_list.remove(con)
            elif(curr_window == "host_game"):
                game.show_bg(screen,board,dragging,chess.WHITE, board_list,mov,selected_square)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            surrender = True
                        elif event.key == pygame.K_LEFT:
                            selected_square -= 1
                            if(selected_square<0):
                                selected_square = 0
                        elif event.key == pygame.K_RIGHT:
                            selected_square += 1
                            if(selected_square>63):
                                selected_square = 63
                        elif event.key == pygame.K_UP:
                            selected_square -= 8
                            if(selected_square<0):
                                selected_square += 8
                        elif event.key == pygame.K_DOWN:
                            selected_square += 8
                            if(selected_square>63):
                                selected_square -= 8 
                        elif event.key == pygame.K_RETURN:
                            if(move_start == -1):
                                move_start = 63-selected_square
                                row = move_start // 8
                                col = move_start % 8
                                flipped_col = abs(col - 7)
                                move_start = row * 8 + flipped_col 
                                dragging = True
                            elif(move_end == -1):
                                move_end = 63-selected_square
                                row = move_end // 8 
                                col = move_end % 8
                                flipped_col = abs(col - 7) 
                                move_end = row * 8 + flipped_col 
                                dragging = False
                                if(team_turn == "w"):
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
                                            #check if the engine is already running a loop
                                            if not engine._inLoop:
                                                engine.say(moveSay)
                                                engine.runAndWait()
                                        if(audioFeedback):
                                            thread = threading.Thread(target = say_thread)
                                            thread.start()
                                        team_turn = "b"
                                    if(board.outcome()):
                                        db_path = os.path.join(os.path.dirname(__file__), 'users.db')
                                        conn = sqlite3.connect(db_path)
                                        curr = conn.cursor()
                                        outcome = board.outcome()
                                        if(outcome.winner==chess.WHITE):
                                            board.result = "1-0"
                                            self.add_stats(username,"wins")
                                        elif(outcome.winner==chess.BLACK):
                                            board.result = "0-1"
                                            self.add_stats(username,"losses")
                                        else:
                                            board.result = "1/2-1/2"
                                            self.add_stats(username,"draws")
                                        pygame.display.set_caption("Game over")
                                        curr_window = "endScreen" 
                                        conn.commit()
                                        #close the cursor and database connection
                                        curr.close()
                                        conn.close()
                                move_start = -1
                                move_end = -1

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
                                self.add_stats(username,"losses")
                                pygame.display.set_caption("Game Over")
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
                                    self.add_stats(username,"wins")
                                elif(outcome.winner==chess.BLACK):
                                    board.result = "0-1"
                                    self.add_stats(username,"losses")
                                else:
                                    board.result = "1/2-1/2"
                                    self.add_stats(username,"draws")
                                pygame.display.set_caption("Game Over")
                                curr_window = "endScreen" 
                        move_start = -1
                        move_end = -1
                if(voice_enabled and team_turn == "w"):
                    #set up the audio stream
                    p = pyaudio.PyAudio()
                    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

                    #set up the speech recognizer
                    model_path = get_model_path()
                    dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__))) # Get the absolute path of the 'chess.dict' file in the same directory as this Python file
                    pygame.display.update()
                    speech = LiveSpeech(
                        verbose=False,
                        sampling_rate=16000,
                        buffer_size=1024,
                        no_search=False,
                        full_utt=False,
                        hmm=os.path.join(model_path, 'en-us'),
                        lm=os.path.join(model_path, 'en-us.lm.bin'),
                        dic=os.path.join(dict_path, 'chess.dict')
                    )
                    if("" not in mov):
                        mov = ["","","",""]
                    for phrase in speech:
                        for i,space in enumerate(mov):
                            if space == "":
                                if((i is 1 or i is 3) and str(phrase) in number_words):
                                    mov[i] = phrase
                                elif((i is 0 or i is 2) and str(phrase) in letter_words):
                                    mov[i] = phrase
                                break
                        break #stop after the first recognized phrase

                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    number_words = {
                        'zero': 0,
                        'one': 1,
                        'two': 2,
                        'three': 3,
                        'four': 4,
                        'five': 5,
                        'six': 6,
                        'seven': 7,
                        'eight': 8,
                        'nine': 9
                    }
                    if("surrender" in mov):
                        board.result = "0-1"
                        surrString = "s"
                        c.send(surrString.encode())
                        self.add_stats(username,"losses")
                        pygame.display.set_caption("Game over")
                        curr_window = "endScreen"
                    if("quit" in mov):
                        board.result = "0-1"
                        surrString = "s"
                        c.send(surrString.encode())
                        self.add_stats(username,"losses")
                        pygame.display.set_caption("Game over")
                        curr_window = "endScreen"
                    elif("" not in mov):
                        number = number_words.get(str(mov[1]).lower())
                        sqr = str(mov[0]).upper()+str(number)
                        move_start = square_to_int(str(sqr))
                        number = number_words.get(str(mov[3]).lower())
                        sqr = str(mov[2]).upper()+str(number)
                        move_end = square_to_int(str(sqr))
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

                if(team_turn=="b"):
                    #RECIEVE MOVE FROM CLIENT
                    ready_to_read, _, _ = select.select([c], [], [], 0.1)
                    if ready_to_read:
                        try:
                            data = c.recv(1024)
                        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                            # If the client has closed the connection, a BrokenPipeError will be raised
                            for con in sockets_list:
                                con.close()
                                sockets_list.remove(con)
                            data = None
                            pygame.display.set_caption("Connection Interrupted")
                            curr_window = "connection_cut"
                    else:
                        data = None

                    #check if the other side has closed the connection
                    try:
                        c.send(b'ping')
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                        #if the client has closed the connection
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        pygame.display.set_caption("Connection Interrupted")
                        curr_window = "connection_cut"
                    if data:
                        data = data.replace(b"ping", b"")
                    # use the received data
                    if data:
                        dataDec = data.decode('utf-8').strip("b'").strip("'")
                        if(dataDec=='s'):
                            board.result = "1-0"
                            self.add_stats(username,"wins")
                            pygame.display.set_caption("Game Over")
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
                            self.add_stats(username,"wins")
                        elif(outcome.winner==chess.BLACK):
                            board.result = "0-1"
                            self.add_stats(username,"losses")
                        else:
                            board.result = "1/2-1/2"
                            self.add_stats(username,"draws")
                        pygame.display.set_caption("Game Over")
                        curr_window = "endScreen"
            #input ip and join host game
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
                            button = 3
                        elif(join_field.collidepoint(pygame.mouse.get_pos())):
                            button = 2
                        if client_field.collidepoint(pygame.mouse.get_pos()):
                            username_active = 1
                        else:
                            username_active = 0
                    elif event.type == pygame.KEYDOWN:
                        #UPDATE FEN FIELD
                        if(event.key == pygame.K_RETURN):
                            username_active = 0
                        if username_active == 1:
                            if event.key == pygame.K_BACKSPACE:
                                ipInput = ipInput[:-1]
                            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                root = tk.Tk()
                                root.withdraw()
                                clipboard_text = root.clipboard_get()
                                if (clipboard_text and len(clipboard_text) < 35):
                                    #if clipboard has text, append it to REN
                                    ipInput += clipboard_text
                            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                                ipInput = ''
                            elif(len(ipInput) < 35 and event.unicode in valid_ip_chars):
                                ipInput += event.unicode
                        if(username_active == 0):
                            if(event.key == pygame.K_1):
                                username_active = 1
                            elif(event.key == pygame.K_2):
                                button = 2
                            elif(event.key == pygame.K_3):
                                button = 3
                if(button == 2):
                    button = 0
                    connectStart = 0
                    port = 5000
                    s = socket.socket(socket.AF_INET,
                    socket.SOCK_STREAM)
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
                        pygame.display.set_caption("Client Lobby")
                        curr_window = "joinLobby"
                    except ConnectionRefusedError as e:
                        print("Failed to connect to server:", e)
                    except (socket.error, ValueError):
                        print("Invalid IP")
                elif(button == 3):
                    button = 0
                    pygame.display.set_caption("Main Menu")
                    curr_window = "menu"

            #wait for host to start
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
                            pygame.display.set_caption("Client Menu")
                            curr_window = "joinMenu"
                    elif(event.type == pygame.KEYDOWN):
                        if(event.key == pygame.K_RETURN):
                            for con in sockets_list:
                                con.close()
                                sockets_list.remove(con)
                            pygame.display.set_caption("Client Menu")
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
                    move_start = -1
                    move_end = -1
                    pygame.display.set_caption("Game start")
                    curr_window = "clientGame"

            elif(curr_window == "clientGame"):
                game.show_bg(screen,board,dragging,chess.BLACK, board_list,mov,selected_square)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            surrender = True
                        elif event.key == pygame.K_LEFT:
                            selected_square -= 1
                            if(selected_square<0):
                                selected_square = 0
                        elif event.key == pygame.K_RIGHT:
                            selected_square += 1
                            if(selected_square>63):
                                selected_square = 63
                        elif event.key == pygame.K_UP:
                            selected_square -= 8
                            if(selected_square<0):
                                selected_square += 8
                        elif event.key == pygame.K_DOWN:
                            selected_square += 8
                            if(selected_square>63):
                                selected_square -= 8 
                        elif event.key == pygame.K_RETURN:
                            if(move_start == -1):
                                move_start = 63-selected_square
                                row = move_start // 8
                                col = move_start % 8
                                flipped_col = abs(col - 7)
                                move_start = row * 8 + flipped_col 
                                dragging = True
                            elif(move_end == -1):
                                move_end = 63-selected_square
                                row = move_end // 8 
                                col = move_end % 8
                                flipped_col = abs(col - 7) 
                                move_end = row * 8 + flipped_col 
                                dragging = False
                                if(team_turn == "b"):
                                    promote = make_move(move_start,move_end,board,screen,None)
                                    # 0 if invalid move, 1 if no promotion, 2-5 to designate promotion
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
                                        move_start = -1
                                        move_end = -1
                                        team_turn = "w"
                                        if(board.outcome()):
                                            outcome = board.outcome()
                                            if(outcome.winner==chess.WHITE):
                                                board.result = "1-0"
                                                self.add_stats(username,"losses")
                                            elif(outcome.winner==chess.BLACK):
                                                board.result = "0-1"
                                                self.add_stats(username,"wins")
                                            else:
                                                board.result = "1/2-1/2"
                                                self.add_stats(username,"draws")
                                            pygame.display.set_caption("Game Over")
                                            curr_window = "endScreen"
                            else:
                                move_start = -1
                                move_end = -1
                        
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
                                pygame.display.set_caption("Game Over")
                                curr_window = "endScreen"
                                self.add_stats(username,"losses")
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
                                        self.add_stats(username,"losses")
                                    elif(outcome.winner==chess.BLACK):
                                        board.result = "0-1"
                                        self.add_stats(username,"wins")
                                    else:
                                        board.result = "1/2-1/2"
                                        self.add_stats(username,"draws")
                                    pygame.display.set_caption("Game Over")
                                    curr_window = "endScreen"
                        move_start = -1
                        move_end = -1
                
                
                if(voice_enabled and team_turn == "b"):
                    # Set up the audio stream
                    p = pyaudio.PyAudio()
                    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

                    # Set up the speech recognizer
                    model_path = get_model_path()
                    dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__))) # Get the absolute path of the 'chess.dict' file in the same directory as this Python file
                    pygame.display.update()

                    speech = LiveSpeech(
                        verbose=False,
                        sampling_rate=16000,
                        buffer_size=1024,
                        no_search=False,
                        full_utt=False,
                        hmm=os.path.join(model_path, 'en-us'),
                        lm=os.path.join(model_path, 'en-us.lm.bin'),
                        dic=os.path.join(dict_path, 'chess.dict')
                    )

                    if("" not in mov):
                        mov = ["","","",""]

                    for phrase in speech:
                        for i,space in enumerate(mov):
                            if space == "":
                                if((i is 1 or i is 3) and str(phrase) in number_words):
                                    mov[i] = phrase
                                elif((i is 0 or i is 2) and str(phrase) in letter_words):
                                    mov[i] = phrase
                                break
                        break #stop after the first recognized phrase

                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    number_words = {
                        'zero': 0,
                        'one': 1,
                        'two': 2,
                        'three': 3,
                        'four': 4,
                        'five': 5,
                        'six': 6,
                        'seven': 7,
                        'eight': 8,
                        'nine': 9
                    }
                    if("surrender" in mov):
                        board.result = "1-0"
                        surrString = "s"
                        s.send(surrString.encode())
                        pygame.display.set_caption("Game Over")
                        curr_window = "endScreen"
                        self.add_stats(username,"losses")
                    elif("quit" in mov):
                        board.result = "1-0"
                        surrString = "s"
                        s.send(surrString.encode())
                        pygame.display.set_caption("Game Over")
                        curr_window = "endScreen"
                        self.add_stats(username,"losses")
                    elif("" not in mov):
                        number = number_words.get(str(mov[1]).lower())
                        sqr = str(mov[0]).upper()+str(number)
                        move_start = square_to_int(str(sqr))
                        number = number_words.get(str(mov[3]).lower())
                        sqr = str(mov[2]).upper()+str(number)
                        move_end = square_to_int(str(sqr))

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
                                    self.add_stats(username,"losses")
                                elif(outcome.winner==chess.BLACK):
                                    board.result = "0-1"
                                    self.add_stats(username,"wins")
                                else:
                                    board.result = "1/2-1/2"
                                    self.add_stats(username,"draws")
                                pygame.display.set_caption("Game Over")
                                curr_window = "endScreen"
          
                
                if(team_turn == "w"):
                    # receive data in non-blocking mode
                    ready_to_read, _, _ = select.select([s], [], [], 0.1)
                    if ready_to_read:
                        try:
                            data = s.recv(1024)
                        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                            # If the client has closed the connection, a BrokenPipeError will be raised
                            for con in sockets_list:
                                con.close()
                                sockets_list.remove(con)
                            data = None
                            pygame.display.set_caption("Connection Error")
                            curr_window = "connection_cut"
                    else:
                        data = None

                    # Check if the other side has closed the connection
                    try:
                        s.send(b'ping')
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                        # If the client has closed the connection, a BrokenPipeError, ConnectionResetError, or ConnectionAbortedError will be raised
                        for con in sockets_list:
                            con.close()
                            sockets_list.remove(con)
                        pygame.display.set_caption("Connection Error")
                        curr_window = "connection_cut"
                    if(data):
                        data = data.replace(b"ping", b"")
                    # use the received data
                    if data:
                        dataDec = data.decode('utf-8').strip("b'").strip("'")
                        if(dataDec=='s'):
                            board.result = "0-1"
                            pygame.display.set_caption("Game Over")
                            curr_window = "endScreen"
                            self.add_stats(username,"wins")
                        else:
                            numbers =  re.findall(r'\d+', str(data))
                            numbers = [int(num) for num in numbers]
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
                            self.add_stats(username,"losses")
                        elif(outcome.winner==chess.BLACK):
                            board.result = "0-1"
                            self.add_stats(username,"wins")
                        else:
                            board.result = "1/2-1/2"
                            self.add_stats(username,"draws")
                        pygame.display.set_caption("Game Over")
                        curr_window = "endScreen"
            elif(curr_window=="endScreen"):
                if(toggleBoard):
                    #selected square -1 because no need to show user input here
                    game.show_bg(screen,board,dragging,chess.BLACK, board_list,["","","",""],-1)
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
                            pygame.display.set_caption("Main Menu")
                            curr_window = "menu"
                        elif toggle_button.collidepoint(pygame.mouse.get_pos()):
                            toggleBoard = True
                    elif event.type == pygame.KEYDOWN:
                        if toggleBoard:
                            toggleBoard = False
                        elif event.key == pygame.K_1:
                            pygame.display.set_caption("Main Menu")
                            curr_window = "menu"   
                        elif event.key == pygame.K_2:
                            toggleBoard = True       
            elif(curr_window == "connection_cut"):
                #window displays if there is an unexpected loss of connection
                screen.fill(COLOUR_ONE)
                cont_button = pygame.Rect(WIDTH // 4, HEIGHT // 1.5, WIDTH // 2, 32)
                pygame.draw.rect(screen, (0,0,0), continue_button, 2)
                text1 = base_font.render("Continue", True, (0,0,0))
                screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 1.5 + 8))
                text2 = base_font.render("Opponent Disconnected: Connection Closed", True, (0,0,0))
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
                            pygame.display.set_caption("Main Menu")
                            curr_window = "menu"   
            elif(curr_window == "register"):
                login.register(screen,username,password,passAuth,user_email)   
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
                            selected_button = 6
                        elif register_button.collidepoint(event.pos): 
                            selected_button = 5

                    elif event.type == pygame.KEYDOWN:
                        # Check if the user typed a character
                        if event.key == pygame.K_RETURN:
                            username_active = 0
                            selected_button = 0
                        if username_active == 1:
                            if event.key == pygame.K_BACKSPACE:
                                username = username[:-1]
                            elif(len(username)<24 and event.unicode in valid_characters):
                                username += event.unicode
                        elif username_active == 2:
                            if event.key == pygame.K_BACKSPACE:
                                password = password[:-1]
                            elif(len(password)<24 and event.unicode in valid_characters):
                                password += event.unicode
                        elif username_active == 3:
                            if event.key == pygame.K_BACKSPACE:
                                passAuth = passAuth[:-1]
                            elif(len(passAuth)<24 and event.unicode in valid_characters):
                                passAuth += event.unicode
                        elif username_active == 4:
                            if event.key == pygame.K_BACKSPACE:
                                user_email = user_email[:-1]
                            elif(len(user_email)<30 and event.unicode in valid_characters):
                                user_email += event.unicode
                        elif username_active == 0:
                            if event.key == pygame.K_1:
                                username_active = 1
                            elif event.key == pygame.K_2:
                                username_active = 2
                            elif event.key == pygame.K_3:
                                username_active = 3
                            elif event.key == pygame.K_4:
                                username_active = 4
                            elif event.key == pygame.K_5:
                                selected_button = 5
                            elif event.key == pygame.K_6:
                                selected_button = 6
                if(selected_button == 5):
                    selected_button = 0
                    regFail = False                           
                    # check if email is in valid format
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
                        regFail = True
                    if password != passAuth:
                        passMatch = False
                        regFail = True
                    else: 
                        passMatch = True


                    if not regFail:
                        subject = "Your account details..."
                        body = f'''Welcome to ChessPAL!\nYour username is {username} and your password is {password}.\nHave fun!
                        \n\nAt ChessPAL we are committed to keeping your data safe and secure. Please note that we store your
                        email address, username and password upon account creation. We use this only to provide our service and
                        none of your data is processed by a third party. You will not be contacted without permission nor will
                        your information be shared. You have the right to delete your information, if you wish to do so please
                        contact us, along with any questions or concerns.'''
                        sender = "oppoppoppopop@gmail.com"
                        recipients = [user_email]
                        email_password = "eijnqoecpnwwklgf"
                        msg = MIMEText(body)
                        msg['Subject'] = subject
                        msg['From'] = sender
                        msg['To'] = ', '.join(recipients)
                        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        smtp_server.login(sender, email_password)
                        smtp_server.sendmail(sender, recipients, msg.as_string())
                        smtp_server.quit()

                    if(not regFail):
                        db_path = os.path.join(os.path.dirname(__file__), 'users.db')
                        conn = sqlite3.connect(db_path)
                        curr = conn.cursor()
                        curr.execute("SELECT * FROM user_stats WHERE username = ?", (username,))
                        row = curr.fetchone()
                        if not row:
                            password_hash = hashlib.sha256(password.encode()).hexdigest()
                            curr.execute("INSERT INTO user_stats (username, password, wins, losses, draws, white, black,email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (username, password_hash, 0, 0, 0,"(255,255,255)","(0,0,0)",user_email))
                            conn.commit()
                            pygame.display.set_caption("Login")
                            user_email = ""
                            passAuth = ""
                            curr_window = "login"
                        else:
                            user_taken = True
                            regFail = True
                        conn.close()
                if(selected_button == 6):
                    selected_button = 0
                    username_active = 0
                    username = ""
                    password = ""
                    passAuth = ""
                    user_email = ""
                    pygame.display.set_caption("Login")
                    curr_window = "login"
            #colours, audio feedback, stats
            elif(curr_window == "acc_settings"):
                settings.show_screen(screen, wins, losses, draws,selected_button,audioFeedback,voice_enabled,h_code)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(visible)
                        if colour_wheel_rect.collidepoint(pygame.mouse.get_pos()) and visible==1:
                            update_color(screen,selected_button,username)
                        elif colour_one_rect.collidepoint(pygame.mouse.get_pos()):
                            visible = 1
                            selected_button = 1
                        elif colour_two_rect.collidepoint(pygame.mouse.get_pos()):
                            visible = 1
                            selected_button = 2
                        elif audio_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                            selected_button = 3
                        elif voice_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                            selected_button = 4
                        elif sett_quit_field.collidepoint(pygame.mouse.get_pos()):
                            selected_button = 5
                        else: 
                            selected_button = 0
                            visible = 0
                    elif event.type == pygame.KEYDOWN:
                        visible = 0
                        if event.key == pygame.K_RETURN:
                            if(selected_button == 1 or selected_button == 2):
                                update_color_hex(screen,selected_button,username,h_code)
                            selected_button = 0
                            h_code = ""
                        if(selected_button == 0):
                            if event.key == pygame.K_1:
                                selected_button = 1
                            elif event.key == pygame.K_2:
                                selected_button = 2
                            elif event.key == pygame.K_3:
                                selected_button = 3
                            elif event.key == pygame.K_4:
                                selected_button = 4
                            elif event.key == pygame.K_5:
                                selected_button = 5
                        elif(selected_button == 1):
                            if event.key == pygame.K_BACKSPACE:
                                h_code = h_code[:-1]
                            elif(len(h_code) < 7 and event.unicode in hex_chars):
                                print(h_code)
                                h_code += event.unicode            
                        elif(selected_button == 2):
                            if event.key == pygame.K_BACKSPACE:
                                h_code = h_code[:-1]
                            elif(len(h_code) < 7 and event.unicode in hex_chars):
                                print(h_code)
                                h_code += event.unicode    
                
                if(selected_button == 1):
                    hex_text = font.render(h_code, True, BLACK)
                    hex_text_pos = hex_text.get_rect(center=colour_one_rect.center)
                    hex_text_pos.centerx += 100  # move the text 20 pixels to the right
                    screen.blit(hex_text, hex_text_pos)
                if(selected_button == 2):
                    hex_text = font.render(h_code, True, BLACK)
                    hex_text_pos = hex_text.get_rect(center=colour_two_rect.center)
                    hex_text_pos.centerx += 100  # move the text 20 pixels to the right
                    screen.blit(hex_text, hex_text_pos)


                if(selected_button == 3):
                    selected_button = 0
                    if(audioFeedback):
                        audioFeedback = 0
                    else:
                        audioFeedback = 1
                elif(selected_button == 4):
                    selected_button = 0
                    if(voice_enabled):
                        voice_enabled = 0
                    else:
                        voice_enabled = 1
                elif(selected_button == 5):
                    selected_button = 0
                    pygame.display.set_caption("Main Menu")
                    curr_window = "menu"


            pygame.display.update()


main = Main()
main.mainloop()