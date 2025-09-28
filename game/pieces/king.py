from game.chess_piece import ChessPiece
from game.state import State



class King(ChessPiece):
    def __init__(self, x, y, is_white):
        super().__init__(x, y,is_white)
        self.can_castle = True

    def get_picture(self):
        return "images/white-king.png" if self.is_white else "images/black-king.png"

    def get_type(self):
        return '♚' if self.is_white else '♔'

    def possible_moves(self,state : State):
        from game.pieces.rook import Rook
        from game.castle_move import Castle
        from game.move import Move
        move : list[Move] = []
        for i in range (3):
            for j in range (3):
                if self.check_range_legal(self.x + i - 1, self.y + j - 1):
                    if state.chess_pieces[self.x + i - 1][self.y + j - 1] is None:
                        move.append(Move(self, (self.x + i - 1, self.y + j - 1),state))
                    elif state.chess_pieces[self.x + i - 1][self.y + j - 1] is not None:
                        if self.check_different_color(self,state.chess_pieces[self.x + i - 1][self.y + j - 1]):
                            move.append(Move(self, (self.x + i - 1, self.y + j - 1),state))
                            move[len(move)-1].is_eating_piece = True
        #castle:
        if self.can_castle is True:
            if self.is_white is True:
                if isinstance(state.chess_pieces[7][7],Rook):
                    if state.chess_pieces[7][7].can_castle is True and state.chess_pieces[5][7] is None and state.chess_pieces[6][7] is None:
                        flag = False
                        for i in range(8):
                            for j in range(8):
                                if state.chess_pieces[i][j] is not None and flag is False:
                                    if isinstance(state.chess_pieces[i][j],King):
                                        if i != 6 or j != 6:
                                            continue
                                    if state.chess_pieces[i][j].is_white != self.is_white:
                                        moves_check = state.chess_pieces[i][j].possible_moves(state)
                                        for move_c in moves_check:
                                             if move_c.target_y == 7 and 6>=move_c.target_x>=4:
                                                 flag = True
                                        if flag:
                                            break
                            if flag:
                                break
                        if flag is False:
                            move.append(Castle(self, (6,7),state))
                if isinstance(state.chess_pieces[0][7],Rook):
                    if state.chess_pieces[0][7].can_castle is True and state.chess_pieces[3][7] is None and state.chess_pieces[2][7] is None:
                        flag = False
                        for i in range(8):
                            for j in range(8):
                                if state.chess_pieces[i][j] is not None and flag is False:
                                    if isinstance(state.chess_pieces[i][j], King):
                                        if (i != 1 or 2) or j != 6:
                                            continue
                                    if state.chess_pieces[i][j].is_white != self.is_white:
                                        moves_check = state.chess_pieces[i][j].possible_moves(state)
                                        for move_c in moves_check:
                                            if move_c.target_y == 7 and 4 >= move_c.target_x >= 2:
                                                flag = True
                                        if flag:
                                            break
                            if flag:
                                break
                        if flag is False:
                            move.append(Castle(self, (2, 7),state))
            else:
                if isinstance(state.chess_pieces[7][0],Rook):
                    if state.chess_pieces[7][0].can_castle is True and state.chess_pieces[5][0] is None and state.chess_pieces[6][0] is None:
                        flag = False
                        for i in range(8):
                            for j in range(8):
                                if state.chess_pieces[i][j] is not None and flag is False:
                                    if isinstance(state.chess_pieces[i][j], King):
                                        if (i != 1 or 2) or j != 1:
                                            move.append(Castle(self, (6, 0),state))
                                            continue
                                    if state.chess_pieces[i][j].is_white != self.is_white:
                                        moves_check = state.chess_pieces[i][j].possible_moves(state)
                                        for move_c in moves_check:
                                             if move_c.target_y == 0 and 6>=move_c.target_x>=4:
                                                 flag = True
                                        if flag:
                                            break
                            if flag:
                                break
                        if flag is False:
                            move.append(Castle(self, (6,0),state))
                if isinstance(state.chess_pieces[0][0],Rook):
                    if state.chess_pieces[0][0].can_castle is True and state.chess_pieces[3][0] is None and state.chess_pieces[2][0] is None:
                        flag = False
                        for i in range(8):
                            for j in range(8):
                                if state.chess_pieces[i][j] is not None and flag is False:
                                    if isinstance(state.chess_pieces[i][j], King):
                                        if i != 6 or j != 1:
                                            continue
                                    if state.chess_pieces[i][j].is_white != self.is_white:
                                        print(state.chess_pieces[i][j].position, state.chess_pieces[i][j].get_type)
                                        moves_check = state.chess_pieces[i][j].possible_moves(state)
                                        for move_c in moves_check:
                                            if move_c.target_y == 0 and 4 >= move_c.target_x >= 2:
                                                flag = True
                                        if flag:
                                            break
                            if flag:
                                break
                        if flag is False:
                            move.append(Castle(self, (2, 0),state))
        return move

