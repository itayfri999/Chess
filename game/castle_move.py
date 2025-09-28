from game.state import State
from game.move import Move


class Castle(Move):
    def default_castle_action(self, rook_start_x, rook_y, rook_target_x, chess_pieces):
        self.moving_piece.can_castle = False
        chess_pieces[rook_start_x][rook_y].can_castle = False
        chess_pieces[self.target_x][self.target_y] = self.moving_piece
        chess_pieces[self.moving_piece.x][self.moving_piece.y] = None
        chess_pieces[rook_target_x][rook_y] = chess_pieces[rook_start_x][rook_y]
        chess_pieces[rook_start_x][rook_y] = None
        self.moving_piece.x = self.target_x
        self.moving_piece.position = self.target_position
        chess_pieces[rook_target_x][rook_y].x = rook_target_x
        chess_pieces[rook_target_x][rook_y].position = (rook_target_x, rook_y)

    def play_move(self, state: State, test_move=False):
        temp: Move
        if test_move is False:
            for i in range(11):
                state.last_move[11 - i] = state.last_move[11 - i - 1]
            state.last_move[0] = self
        if self.moving_piece.is_white is True:
            if self.target_x == 2:
                self.default_castle_action(0, 7, 3, state.chess_pieces)
            else:
                self.default_castle_action(7, 7, 5, state.chess_pieces)
        else:
            if self.target_x == 2:
                self.default_castle_action(0, 0, 3, state.chess_pieces)
            else:
                self.default_castle_action(7, 0, 5, state.chess_pieces)
        if test_move is False:
            state.moves_since_capture += 1
            state.is_turn_white = not state.is_turn_white
            win = state.check_win()
            return win
        return 0

    def reverse_move(self, state: State):
        state.chess_pieces[self.original_x][self.original_y] = self.original_piece
        state.chess_pieces[self.target_x][self.target_y] = None
        self.moving_piece.can_castle = True
        if self.target_x == 2:
            state.chess_pieces[0][self.target_y] = state.chess_pieces[3][self.target_y]
            state.chess_pieces[0][self.target_y].can_castle = True
            state.chess_pieces[3][self.target_y] = None
            state.chess_pieces[0][self.target_y].position = (0, self.target_y)
            state.chess_pieces[0][self.target_y].x = 0
        elif self.target_x == 6:
            state.chess_pieces[7][self.target_y] = state.chess_pieces[5][self.target_y]
            state.chess_pieces[7][self.target_y].can_castle = True
            state.chess_pieces[5][self.target_y] = None
            state.chess_pieces[7][self.target_y].position = (7, self.target_y)
            state.chess_pieces[7][self.target_y].x = 7
        self.moving_piece.position = self.original_position
        self.moving_piece.x = self.original_x
