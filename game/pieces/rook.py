from game.chess_piece import ChessPiece
from game.state import State

class Rook (ChessPiece):
    def __init__(self, x, y, is_white):
        super().__init__(x, y,is_white)
        self.can_castle = True

    def get_picture(self):
        return "images/white-rook.png" if self.is_white else "images/black-rook.png"

    def get_type(self):
        return '♜' if self.is_white else '♖'


    def possible_moves(self,state : State):
        from game.move import Move
        moves : list[Move] = []

        moves += self.default_line_move_check(state.chess_pieces, 1, 0,state)
        moves += self.default_line_move_check(state.chess_pieces, -1, 0,state)
        moves += self.default_line_move_check(state.chess_pieces, 0, 1,state)
        moves += self.default_line_move_check(state.chess_pieces, 0, -1,state)
        return moves
