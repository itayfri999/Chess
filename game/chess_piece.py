from game.move import Move

class ChessPiece:
    def __init__(self,x,y,is_white):
        self.x = x
        self.y = y
        self.position = (x,y)
        self.is_white:bool = is_white


    def get_type(self):
        raise NotImplementedError()

    def possible_moves(self, pieces):
        raise NotImplementedError()

    def check_range_legal(self,i,j):
        if 8 > i >= 0 and 8 > j >= 0:
            return True
        else:
            return False
    def check_different_color(self ,first_piece,second_piece):
        if first_piece.is_white != second_piece.is_white:
            return True
        else:
            return False
    def default_line_move_check(self,pieces,i,j):
        moves_part : list[Move] = []
        while True:
            if self.check_range_legal(self.x + i,self.y + j):
                if pieces[self.x + i][self.y + j] is None:
                    moves_part.append(Move(self, (self.x + i, self.y + j)))
                    if i > 0:
                        i += 1
                    elif i < 0:
                        i -= 1
                    if j > 0:
                        j += 1
                    elif j < 0:
                        j -= 1
                elif self.check_different_color(self,pieces[self.x + i][self.y + j]):
                    moves_part.append(Move(self, (self.x + i, self.y + j)))
                    return moves_part
                else:
                    return moves_part
            else:
                return moves_part
