from const import *
import chess

#creates and returns a board
def initialise_board(fenCode = ""):
    #if fen is not included, do default setup
    if fenCode != "" and validate_fen(fenCode):
        board = chess.Board(fenCode)
    else:
        board = chess.Board()
    print("returning board")
    return board

def validate_fen(s):
    a = [0]*12
    n = x = 0
    for c in s:
        if c.isdigit():
            n += int(c)
        elif c.isalpha():
            i = 'pP/KkQqRrBbNn'.find(c)
            if i >= 0 and i < 12:
                i &= i>4 and a[i]>(i>6)
                a[i] += 1
            n += 1
        elif c == '/':
            x += 1
        else:
            return False

    valid = n == 71 and x == 7 and all(x <= 8 for x in a[:6])
    return valid
#converts the python chess board to a fencode, which then is converted to a matrix
def board_toMatrix(fenCode):
    board = []
    for row in fenCode.split('/'):
        tempRow = []
        #builds board row by row, appending to board[]
        for c in row:
            if c == ' ':
                break
            elif c in '12345678':
                tempRow.extend( ['--'] * int(c) )
            elif c == 'P':
                tempRow.append( c.upper() )
            elif c == 'p':
                tempRow.append( c.lower() )
            elif c > 'Z':
                tempRow.append( c.lower() )
            else:
                tempRow.append( c.upper() )

        board.append( tempRow )
    return board

def make_move(start, end, board, surface, promote):
    chess_pieces = [chess.ROOK,chess.KNIGHT,chess.BISHOP,chess.QUEEN]
    chess_strings = ["R","K","B","Q"]
    move = chess.Move(start, end)
    #promoMove used to check if a promotion move is needed
    promoMove = chess.Move(from_square=start, to_square=end, promotion=chess.QUEEN)

    #if this is a move sent from opponent with a promotion
    if(promote is not None):
        if(promote>1):
            print(promote)
            promoMove = chess.Move(from_square=start, to_square=end, promotion=chess_pieces[promote-2])
            if promoMove in board.legal_moves:
                board.push(promoMove)
                return 1
    
    if move in board.legal_moves:
        board.push(move)
        return 1
    #if a pawn has reached the other side of the board
    elif promoMove in board.legal_moves:
        choosing = True
        # Define colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

        # Define the chess pieces (excluding pawns) as a list of strings

        # Create a font object for the text
        font = pygame.font.SysFont(None, 30)

        # Create a surface object for the text
        text_surface = font.render(", ".join(chess_strings), True, WHITE)

        # Get the dimensions of the text surface
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()

        # Create a surface object for the rectangle
        rect_surface = pygame.Surface((text_width + 20, text_height + 20))
        rect_surface.fill(BLACK)

        # Blit the text surface onto the rectangle surface
        rect_surface.blit(text_surface, (10, 10))
        mouse = pygame.mouse.get_pos()
        rect_x = mouse[0]
        rect_y = mouse[1]

        # Make sure the rectangle doesn't go off screen
        if rect_x + text_width + 20 > WIDTH:
            rect_x = WIDTH - text_width - 20
        if rect_y + text_height + 20 > HEIGHT:
            rect_y = HEIGHT - text_height - 20

        # Blit the rectangle surface onto the given surface at position (rect_x, rect_y)
        surface.blit(rect_surface, (rect_x, rect_y))
        pygame.display.flip()


        #wait for the user to choose
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    #check which chess piece option was clicked
                    for i, piece in enumerate(chess_pieces):
                        if x >= rect_x + 10 and x <= rect_x + text_width + 10 and y >= rect_y + 10 + i * 25 and y <= rect_y + 35 + i * 25:
                            #column index
                            distance = x - rect_x
                            column_index = distance // (text_width / 4)

                            if(column_index>3.0):
                                column_index = 3.0
                            promoMove = chess.Move(from_square=start, to_square=end, promotion=chess_pieces[int(column_index)])
                            choosing = False
                            print(str(promoMove))
                            break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        promoMove = chess.Move(from_square=start, to_square=end, promotion=chess.ROOK)
                        column_index = 0.0
                        choosing = False
                    elif event.key == pygame.K_2:
                        promoMove = chess.Move(from_square=start, to_square=end, promotion=chess.KNIGHT)
                        column_index = 1.0
                        choosing = False
                    elif event.key == pygame.K_3:
                        promoMove = chess.Move(from_square=start, to_square=end, promotion=chess.BISHOP)
                        column_index = 2.0
                        choosing = False
                    elif event.key == pygame.K_4:
                        promoMove = chess.Move(from_square=start, to_square=end, promotion=chess.QUEEN)
                        column_index = 3.0
                        choosing = False

        board.push(promoMove)
        return int(column_index+2)
    else:
        return 0


