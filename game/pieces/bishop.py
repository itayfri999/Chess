from game.chess_piece import ChessPiece
from game.move import Move

class Bishop (ChessPiece):
    def get_type(self):
        return '♝' if self.is_white else '♗'


    def possible_moves(self,pieces):

        moves : list[Move] = []

        moves += self.default_line_move_check(pieces, 1, 1)
        moves += self.default_line_move_check(pieces, -1, 1)
        moves += self.default_line_move_check(pieces, 1, -1)
        moves += self.default_line_move_check(pieces, -1, -1)
        return moves
