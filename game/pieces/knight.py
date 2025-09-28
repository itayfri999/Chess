from game.chess_piece import ChessPiece
from game.move import Move
from game.state import State

class Knight (ChessPiece):
    def get_picture(self):
        return "images/white-knight.png" if self.is_white else "images/black-knight.png"

    def get_type(self):
        return '♞' if self.is_white else '♘'

    def default_moves(self,pieces,i,j,state):
        moves_part: list[Move] = []
        if self.check_range_legal(self.x + i, self.y + j):
            if pieces[self.x + i][self.y + j] is None:
                moves_part.append(Move(self, (self.x + i, self.y + j),state))
            elif pieces[self.x + i][self.y + j] is not None:
                if self.check_different_color(pieces[self.x + i][self.y + j],self):
                    moves_part.append(Move(self, (self.x + i, self.y + j),state))
                    moves_part[len(moves_part)-1].is_eating_piece = True
        return moves_part

    def possible_moves(self,state : State):
        moves : list[Move] = []

        moves += self.default_moves(state.chess_pieces, 1, 2,state)
        moves += self.default_moves(state.chess_pieces, -1, 2,state)
        moves += self.default_moves(state.chess_pieces, 1, -2,state)
        moves += self.default_moves(state.chess_pieces, -1, -2,state)
        moves += self.default_moves(state.chess_pieces, 2, 1,state)
        moves += self.default_moves(state.chess_pieces, -2, 1,state)
        moves += self.default_moves(state.chess_pieces, 2, -1,state)
        moves += self.default_moves(state.chess_pieces, -2, -1,state)

        return moves