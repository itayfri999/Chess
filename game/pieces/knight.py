from game.chess_piece import ChessPiece
from game.move import Move

class Knight (ChessPiece):
    def get_type(self):
        return '♞' if self.is_white else '♘'

    def default_moves(self,pieces,i,j):
        moves_part: list[Move] = []
        if self.check_range_legal(self.x + i, self.y + j):
            if pieces[self.x + i][self.y + j] is None:
                moves_part.append(Move(self, (self.x + i, self.y + j)))
            elif pieces[self.x + i][self.y + j] is not None:
                if self.check_different_color(pieces[self.x + i][self.y + j],self):
                    moves_part.append(Move(self, (self.x + i, self.y + j)))
        return moves_part

    def possible_moves(self,pieces):
        moves : list[Move] = []

        moves += self.default_moves(pieces, 1, 2)
        moves += self.default_moves(pieces, -1, 2)
        moves += self.default_moves(pieces, 1, -2)
        moves += self.default_moves(pieces, -1, -2)
        moves += self.default_moves(pieces, 2, 1)
        moves += self.default_moves(pieces, -2, 1)
        moves += self.default_moves(pieces, 2, -1)
        moves += self.default_moves(pieces, -2, -1)

        return moves