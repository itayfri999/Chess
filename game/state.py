from game.chess_piece import ChessPiece

class State:
    def __init__(self,chess_pieces,is_turn_white):
        from game.move import Move
        self.chess_pieces : list[list] = []
        self.chess_pieces = chess_pieces
        self.last_move : list[Move] = []
        for i in range (12):
            self.last_move.append(Move(ChessPiece(0, 0, True), (0, 0),self))
            if len(self.last_move)>12:
                self.last_move.pop()
        self.moves_since_capture = 0
        self.is_turn_white = is_turn_white

    def __repr__(self) -> str:
        string = ''
        for i in range (8):
            for j in range (8):
                if self.chess_pieces[j][i] is not None:
                    string +=self.chess_pieces[j][i].get_type()
                    string += ' '
                else:
                    string += "▭ "
            string += "\n"
        return string


    def check_king_attacked(self, possible_moves):
        from game.pieces.king import King
        from game.move import Move
        if len(possible_moves) == 0:
            return possible_moves
        for move in possible_moves.copy():
            move.play_move(self,test_move = True)
            removed = False

            for i in range(8):
                for j in range(8):
                    if self.chess_pieces[i][j] is not None:
                        if self.chess_pieces[i][j].is_white != move.moving_piece.is_white:
                            moves_check = self.chess_pieces[i][j].possible_moves(self)
                            for move_c in moves_check:
                                target_piece = self.chess_pieces[move_c.target_x][move_c.target_y]
                                if isinstance(target_piece, King):
                                    possible_moves.remove(move)
                                    removed = True
                                if removed:
                                    break
                            if removed:
                                break
                if removed:
                    break
            move.reverse_move(self)
        return possible_moves


    def is_king_in_check(self):
        from game.pieces.king import King
        for i in range(8):
            for j in range(8):
                if self.chess_pieces[i][j] is not None:
                    if self.chess_pieces[i][j].is_white != self.is_turn_white:
                        moves_check = self.chess_pieces[i][j].possible_moves(self)
                        for move_c in moves_check:
                            target_piece = self.chess_pieces[move_c.target_x][move_c.target_y]
                            if isinstance(target_piece, King):
                                return True
        return False

    def check_win(self):
        from game.move import Move
        possible_moves_total: list[Move] = []
        for i in range(8):
            for j in range(8):
                if self.chess_pieces[i][j] is not None:
                    if self.chess_pieces[i][j].is_white == self.is_turn_white:
                        possible_moves_total += self.chess_pieces[i][j].possible_moves(self)
        possible_moves_check = self.check_king_attacked(possible_moves_total)
        if len(possible_moves_check) == 0:
            if self.is_king_in_check():
                if self.is_turn_white:
                    return 2
                else:
                    return 1
            else:
                return 3
        elif self.last_move[0].moving_piece and self.last_move[1].moving_piece and self.last_move[2].moving_piece and self.last_move[3].moving_piece and self.last_move[4].moving_piece and self.last_move[5].moving_piece and self.last_move[6].moving_piece and self.last_move[7].moving_piece and self.last_move[8].moving_piece and self.last_move[9].moving_piece and self.last_move[10].moving_piece and self.last_move[11].moving_piece is not None:
            if self.moves_since_capture > 100 or (self.last_move[0].get_all() == self.last_move[
                    4].get_all() == self.last_move[8].get_all() and self.last_move[
                    2].get_all() == self.last_move[6].get_all() == self.last_move[
                    10].get_all() and self.last_move[1].get_all() == self.last_move[
                    5].get_all() == self.last_move[9].get_all() and self.last_move[
                    3].get_all() == self.last_move[7].get_all() == self.last_move[
                    11].get_all()):
                if self.last_move[11].target_position != self.last_move[11].moving_piece.position:
                    return 3
        return 0
