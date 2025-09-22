from game.chess_piece import ChessPiece
from game.move import Move

class King(ChessPiece):
    def __init__(self, x, y, is_white):
        super().__init__(x, y,is_white)
        self.can_castle = True

    def get_type(self):
        return '♚' if self.is_white else '♔'

    def possible_moves(self,pieces):
        move : list[Move] = []
        for i in range (3):
            for j in range (3):
                if pieces[self.x + i - 1][self.y + j - 1] is None and self.check_range_legal(self.x + i - 1, self.y + j - 1):
                    move.append(Move(self, (self.x + i - 1, self.y + j - 1)))
                elif pieces[self.x + i - 1][self.y + j - 1] is not None and self.check_range_legal(self.x + i - 1, self.y + j - 1):
                    if self.check_different_color(self,pieces[self.x + i - 1][self.y + j - 1]):
                        move.append(Move(self, (self.x + i - 1, self.y + j - 1)))
        return move

