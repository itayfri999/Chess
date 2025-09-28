from typing import Tuple, Optional
from game.chess_piece import ChessPiece
from game.move import Move
from game.state import State
from game.pieces.king import King
from game.pieces.pawn import Pawn
from game.pieces.rook import Rook
from game.pieces.bishop import Bishop
from game.pieces.queen import Queen
from game.pieces.knight import Knight


random_string1 = '8/pPP3bp/1R1qk2B/P2N4/1r1P3P/3pK2R/1p2B2p/3Qn1r1'
random_string2 = '2n2N1r/1p1P1B2/P1N1p1n1/3prPKb/4P1p1/2P1B1k1/QR1p2p1/5R2'
INITIALISING_STRING = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
STRING_AFTER_E4 = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR'
STRING_AFTER_E4_with_rook = '1nbqkbnr/pppppppp/8/8/r3P3/8/PPPP1PPP/RNBQKBNR'
STRING_AFTER_E4_with_bishop = 'rnbqkbnr/pppppppp/8/8/2B1P3/8/PPPP1PPP/RNBQK1NR'
STRING_AFTER_E4_with_queen = 'rnbqkbnr/pppppppp/8/8/2Q1P3/8/PPPP1PPP/RNB1KBNR'
STRING_KNIGHT = 'rnbqkbnr/pppppppp/8/1N6/3P4/8/PPPP1PPP/R1BQKBNR'

string_pawn = 'rnbqkbnr/1pp2ppp/8/3p4/3KP3/1p6/PPPP1PPP/RNBQ1BNR'

STRING_AFTER_C5 = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR'
STRING_AFTER_Nf3 = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'


class Board:
    def __init__(self):
        chess_pieces: list[list] = []
        new: list[Optional[ChessPiece]] = []
        for i in range(8):
            for j in range(8):
                new.append(None)
            chess_pieces.append(new)
            new: list[Optional[ChessPiece]] = []

        self.state = State(chess_pieces,True)
        self.last_move : Move

    def board_initialise(self,given_string='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
        x = 0
        y = 0

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
                        self.state.chess_pieces[x][y] = (Rook(x, y, is_white=False))
                        x = x + 1
                    case 'n':
                        self.state.chess_pieces[x][y] = (Knight(x, y, is_white=False))
                        x = x + 1
                    case 'b':
                        self.state.chess_pieces[x][y] = (Bishop(x, y, is_white=False))
                        x = x + 1
                    case 'q':
                        self.state.chess_pieces[x][y] = (Queen(x, y, is_white=False))
                        x = x + 1
                    case 'k':
                        self.state.chess_pieces[x][y] = (King(x, y, is_white=False))
                        x = x + 1
                    case 'p':
                        self.state.chess_pieces[x][y] = (Pawn(x, y, is_white=False))
                        x = x + 1
                    case 'P':
                        self.state.chess_pieces[x][y] = (Pawn(x, y, is_white=True))
                        x = x + 1
                    case 'R':
                        self.state.chess_pieces[x][y] = (Rook(x, y, is_white=True))
                        x = x + 1
                    case 'N':
                        self.state.chess_pieces[x][y] = (Knight(x, y, is_white=True))
                        x = x + 1
                    case 'B':
                        self.state.chess_pieces[x][y] = (Bishop(x, y, is_white=True))
                        x = x + 1
                    case 'Q':
                        self.state.chess_pieces[x][y] = (Queen(x, y, is_white=True))
                        x = x + 1
                    case 'K':
                        self.state.chess_pieces[x][y] = (King(x, y, is_white=True))
                        x = x + 1
                    case _:
                        raise Exception('Invalid char')
        return self
