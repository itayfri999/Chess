from game.chess_piece import ChessPiece
from game.move import Move

class Pawn(ChessPiece):
    def get_type(self):
        return '♟' if self.is_white else '♙'

    def possible_moves(self,pieces):
        moves : list[Move] = []
        if self.y == 6 and self.is_white == True and pieces[self.x][self.y - 2] is None:
            moves.append(Move(self,(self.x,self.y - 2)))
        if self.y == 1 and self.is_white == False and pieces[self.x][self.y + 2] is None:
            moves.append(Move(self,(self.x,self.y + 2)))

        if self.is_white:
            if pieces[self.x][self.y - 1] is None and self.check_range_legal(self.x, self.y - 1):
                moves.append(Move(self,(self.x ,self.y - 1)))
            if self.check_range_legal(self.x + 1, self.y - 1):
                if pieces[self.x + 1][self.y - 1] is not None:
                    if self.check_different_color(pieces[self.x + 1][self.y - 1], self):
                        moves.append(Move(self,(self.x + 1,self.y - 1)))
            if self.check_range_legal(self.x - 1, self.y - 1):
                if pieces[self.x - 1][self.y - 1] is not None:
                    if self.check_different_color(pieces[self.x - 1][self.y - 1], self):
                        moves.append(Move(self,(self.x - 1,self.y - 1)))
        else:
            if pieces[self.x][self.y + 1] is None and self.check_range_legal(self.x, self.y + 1):
                moves.append(Move(self,(self.x,self.y + 1)))
            if self.check_range_legal(self.x + 1, self.y + 1):
                if pieces[self.x + 1][self.y + 1] is not None:
                    if self.check_different_color(pieces[self.x + 1][self.y + 1], self):
                        moves.append(Move(self,(self.x + 1,self.y + 1)))
            if self.check_range_legal(self.x - 1, self.y + 1):
                if pieces[self.x - 1][self.y + 1] is not None:
                    if self.check_different_color(pieces[self.x - 1][self.y + 1], self):
                        moves.append(Move(self,(self.x - 1,self.y + 1)))

        return moves


# isinstance(piece, Rook)