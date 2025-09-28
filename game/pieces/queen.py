from game.chess_piece import ChessPiece
from game.move import Move
from game.state import State



class Queen(ChessPiece):
    def get_picture(self):
        return "images/white-queen.png" if self.is_white else "images/black-queen.png"

    def get_type(self):
        return '♛' if self.is_white else '♕'

    def possible_moves(self,state : State):
        moves: list[Move] = []
        #bishop moves:
        moves += self.default_line_move_check(state.chess_pieces, 1, 1,state)
        moves += self.default_line_move_check(state.chess_pieces, -1, 1,state)
        moves += self.default_line_move_check(state.chess_pieces, 1, -1,state)
        moves += self.default_line_move_check(state.chess_pieces, -1, -1,state)
        #rook moves:
        moves += self.default_line_move_check(state.chess_pieces, 1, 0,state)
        moves += self.default_line_move_check(state.chess_pieces, -1, 0,state)
        moves += self.default_line_move_check(state.chess_pieces, 0, 1,state)
        moves += self.default_line_move_check(state.chess_pieces, 0, -1,state)
        return moves
