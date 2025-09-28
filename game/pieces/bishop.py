from game.chess_piece import ChessPiece
from game.state import State
from game.move import Move

class Bishop (ChessPiece):
    def get_picture(self):
        return "images/white-bishop.png" if self.is_white else "images/black-bishop.png"

    def get_type(self):
        return '♝' if self.is_white else '♗'


    def possible_moves(self,state : State):

        moves : list[Move] = []

        moves += self.default_line_move_check(state.chess_pieces, 1, 1,state)
        moves += self.default_line_move_check(state.chess_pieces, -1, 1,state)
        moves += self.default_line_move_check(state.chess_pieces, 1, -1,state)
        moves += self.default_line_move_check(state.chess_pieces, -1, -1,state)
        return moves


