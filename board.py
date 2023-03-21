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

def make_move(start,end,board):
    move = chess.Move(start,end)
    promoMove = chess.Move(from_square=start,to_square=end,promotion=chess.QUEEN)
    if move in board.legal_moves:
        board.push(move)
        return board
    elif promoMove in board.legal_moves:
        board.push(promoMove)
        return board
    else:
        return 0




