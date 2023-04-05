from const import *
import chess

#creates and returns a board
def initialise_board(fenCode = ""):
    #if fen is not included, do default setup
    if fenCode != "":
        board = chess.Board(fenCode)
    else:
        board = chess.Board()
    
    return board

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
            print("PROMOTE IS...")
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



        while choosing:
            # Wait for the user to close the window or click on the rectangle
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # Check which chess piece option was clicked and return the corresponding promotion move
                    for i, piece in enumerate(chess_pieces):
                        if x >= rect_x + 10 and x <= rect_x + text_width + 10 and y >= rect_y + 10 + i * 25 and y <= rect_y + 35 + i * 25:
                            # Calculate the column index
                            distance = x - rect_x
                            column_index = distance // (text_width / 4)
                            
                            # Print the result
                            print("Column index:", column_index)
                            if(column_index>3.0):
                                column_index = 3.0
                            promoMove = chess.Move(from_square=start, to_square=end, promotion=chess_pieces[int(column_index)])
                            choosing = False
                            print(str(promoMove))
                            break
        board.push(promoMove)
        return int(column_index+2)
    else:
        return 0


