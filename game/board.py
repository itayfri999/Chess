from typing import Tuple, Optional
from game.chess_piece import ChessPiece
from game.move import Move
#from tile import Tile
from pieces.king import King
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.knight import Knight

random_string1 = '8/pPP3bp/1R1qk2B/P2N4/1r1P3P/3pK2R/1p2B2p/3Qn1r1'
INITIALISING_STRING = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
STRING_AFTER_E4 = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR'
STRING_AFTER_E4_with_rook = '1nbqkbnr/pppppppp/8/8/r3P3/8/PPPP1PPP/RNBQKBNR'
STRING_AFTER_E4_with_bishop = 'rnbqkbnr/pppppppp/8/8/2B1P3/8/PPPP1PPP/RNBQK1NR'
STRING_AFTER_E4_with_queen = 'rnbqkbnr/pppppppp/8/8/2Q1P3/8/PPPP1PPP/RNB1KBNR'
STRING_KNIGHT = 'rnbqkbnr/pppppppp/8/1N6/3P4/8/PPPP1PPP/R1BQKBNR'

string_pawn = 'rnbqkbnr/1pp2ppp/8/3p4/3KP3/1p6/PPPP1PPP/RNBQ1BNR'

STRING_AFTER_C5 = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR'
STRING_AFTER_Nf3 = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'

def board_initialise(given_string):
    board = Board()
    x = 0
    y = 0

    print (len(given_string))
    for char in given_string:
        if x > 8:
            y += 1
        elif '8' >= char >= '1':
            if x + int(char) > 7:
                x = 7
            else:
                x = x + int(char)

        else:
            match char:
                case '/':
                    y = y + 1
                    x = 0
                case 'r':
                    board.chess_pieces[x][y] = (Rook(x,y,is_white=False))
                    x = x + 1
                case 'n':
                    board.chess_pieces[x][y] = (Knight(x,y,is_white=False))
                    x = x + 1
                case 'b':
                    board.chess_pieces[x][y] = (Bishop(x,y,is_white=False))
                    x = x + 1
                case 'q':
                    board.chess_pieces[x][y] = (Queen(x,y,is_white=False))
                    x = x + 1
                case 'k':
                    board.chess_pieces[x][y] = (King(x,y,is_white=False))
                    x = x + 1
                case 'p':
                    board.chess_pieces[x][y] = (Pawn(x,y,is_white=False))
                    x = x + 1
                case 'P':
                    board.chess_pieces[x][y] = (Pawn(x,y,is_white=True))
                    x = x + 1
                case 'R':
                    board.chess_pieces[x][y] = (Rook(x,y,is_white=True))
                    x = x + 1
                case 'N':
                    board.chess_pieces[x][y] = (Knight(x,y,is_white=True))
                    x = x + 1
                case 'B':
                    board.chess_pieces[x][y] = (Bishop(x,y,is_white=True))
                    x = x + 1
                case 'Q':
                    board.chess_pieces[x][y] = (Queen(x, y, is_white=True))
                    x = x + 1
                case 'K':
                    board.chess_pieces[x][y] = (King(x,y,is_white=True))
                    x = x + 1
                case _:
                    raise Exception('Invalid char')
    return board

def check_king_attacked(chess_pieces,possible_moves):
    temp_moving_position = (possible_moves[0].target_x, possible_moves[0].target_y)
    temp_moving_piece_x = possible_moves[0].moving_piece.x
    temp_moving_piece_y = possible_moves[0].moving_piece.y
    for move in possible_moves.copy():
        using_temp = False
        temp_target : ChessPiece = chess_pieces[move.target_x][move.target_y]

        chess_pieces[move.target_x][move.target_y] = move.moving_piece
        chess_pieces[move.moving_piece.x][move.moving_piece.y] = None
        move.moving_piece.position = (move.target_x, move.target_y)
        move.moving_piece.x = move.target_x
        move.moving_piece.y = move.target_y



        for i in range (8):
            for j in range (8):
                if chess_pieces[i][j] is not None:
                    if chess_pieces[i][j].is_white != move.moving_piece.is_white:
                        moves_check = chess_pieces[i][j].possible_moves(chess_pieces)
                        for move_c in moves_check:
                            target_piece = chess_pieces[move_c.target_x][move_c.target_y]
                            if isinstance(target_piece, King):
                                    possible_moves.remove(move)
                                    print("removed:",move.target_position)
       # string = ''
        #for i in range(8):
         #   for j in range(8):
          #      if chess_pieces[j][i] is not None:
           #         string += chess_pieces[j][i].get_type()
            #        string += ' '
             #   else:
              #      string += "▭ "
            #string += "\n"
        #print(string)
        move.moving_piece.x = temp_moving_piece_x
        move.moving_piece.y = temp_moving_piece_y
        move.moving_piece.position = temp_moving_position
        if using_temp:
            chess_pieces[move.target_x][move.target_y] = temp_target
        chess_pieces[temp_moving_piece_x][temp_moving_piece_y] = move.moving_piece
        chess_pieces[move.target_x][move.target_y] = temp_target





    return possible_moves


class Board:
    def __init__(self):
        self.chess_pieces: list[list] = []
        new: list[Optional[ChessPiece]] = []
        for i in range(8):
            for j in range(8):
                new.append(None)
            self.chess_pieces.append(new)
            new: list[Optional[ChessPiece]] = []

        self.is_turn_white = True


    def play_turn(self,position1:Tuple[int,int],position2:Tuple[int,int]):
        raise NotImplementedError()


    def __repr__(self) -> str:
        string = ''
        for i in range (8):
            for j in range (8):
                if self.chess_pieces[j][i] is not None:
                    string +=self.chess_pieces[j][i].get_type()
                    string += ' '
                else:
                    string += "▭ "
            string += "\n"
        return string




T = board_initialise(random_string1)
print(T)
selected_piece = T.chess_pieces[4][2]

if selected_piece is not None:
    print(selected_piece.get_type(),selected_piece.position,selected_piece.is_white)
else:
    raise Exception('selected piece is None')
moves : list[Move] = (selected_piece.possible_moves(T.chess_pieces))
checked_moves : list[Move] = check_king_attacked(T.chess_pieces, moves)


def print_moves(moves_p):
    print("starting to print")
    i = 0
    for j in moves_p:
        print(moves_p[i].target_position)
        i += 1

print_moves(checked_moves)