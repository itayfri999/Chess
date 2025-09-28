from game.chess_piece import ChessPiece
from game.state import State


class Pawn(ChessPiece):
    def get_picture(self):
        return "images/white-pawn.png" if self.is_white else "images/black-pawn.png"

    def get_type(self):
        return '♟' if self.is_white else '♙'

    def possible_moves(self,state : State):
        from game.move_en_passant import En_Passant
        from game.move import Move

        moves : list[Move] = []
        if self.y == 6 and self.is_white == True and state.chess_pieces[self.x][self.y - 2] is None  and state.chess_pieces[self.x][self.y - 1] is None:
            moves.append(Move(self,(self.x,self.y - 2),state))
        if self.y == 1 and self.is_white == False and state.chess_pieces[self.x][self.y + 2] is None and state.chess_pieces[self.x][self.y + 1] is None:
            moves.append(Move(self,(self.x,self.y + 2),state))

        if self.is_white:
            if state.chess_pieces[self.x][self.y - 1] is None and self.check_range_legal(self.x, self.y - 1):
                moves.append(Move(self,(self.x ,self.y - 1),state))
            if self.check_range_legal(self.x + 1, self.y - 1):
                if state.chess_pieces[self.x + 1][self.y - 1] is not None:
                    if self.check_different_color(state.chess_pieces[self.x + 1][self.y - 1], self):
                        moves.append(Move(self,(self.x + 1,self.y - 1),state))
                        moves[len(moves)-1].is_eating_piece = True
            if self.check_range_legal(self.x - 1, self.y - 1):
                if state.chess_pieces[self.x - 1][self.y - 1] is not None:
                    if self.check_different_color(state.chess_pieces[self.x - 1][self.y - 1], self):
                        moves.append(Move(self,(self.x - 1,self.y - 1),state))
                        moves[len(moves)-1].is_eating_piece = True
            # en passant:
            if self.y == 3:
                if state.last_move[0].original_y == 1:
                    if state.last_move[0].target_y == 3:
                        if state.last_move[0].target_x == self.x + 1 or state.last_move[0].target_x == self.x - 1:
                            moves.append(En_Passant(self, (state.last_move[0].target_x , self.y - 1),state))
                            moves[len(moves) - 1].is_eating_piece = True


        else:
            if state.chess_pieces[self.x][self.y + 1] is None and self.check_range_legal(self.x, self.y + 1):
                moves.append(Move(self,(self.x,self.y + 1),state))
            if self.check_range_legal(self.x + 1, self.y + 1):
                if state.chess_pieces[self.x + 1][self.y + 1] is not None:
                    if self.check_different_color(state.chess_pieces[self.x + 1][self.y + 1], self):
                        moves.append(Move(self,(self.x + 1,self.y + 1),state))
                        moves[len(moves)-1].is_eating_piece = True
            if self.check_range_legal(self.x - 1, self.y + 1):
                if state.chess_pieces[self.x - 1][self.y + 1] is not None:
                    if self.check_different_color(state.chess_pieces[self.x - 1][self.y + 1], self):
                        moves.append(Move(self,(self.x - 1,self.y + 1),state))
                        moves[len(moves)-1].is_eating_piece = True
            #en passant:
            if self.y == 4:
                if state.last_move[0].original_y == 6:
                    if state.last_move[0].target_y == 4:
                        if state.last_move[0].target_x == self.x + 1 or state.last_move[0].target_x == self.x - 1:
                            moves.append(En_Passant(self, (state.last_move[0].target_x, self.y + 1),state))
                            moves[len(moves) - 1].is_eating_piece = True
        return moves
