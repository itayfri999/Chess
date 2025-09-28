from game.move import Move
from game.state import State


class En_Passant(Move):
    def play_move(self, state: State, test_move=False):
        if test_move is False:
            for i in range(11):
                state.last_move[11 - i] = state.last_move[11 - i - 1]
            state.last_move[0] = self
        state.chess_pieces[self.target_x][self.target_y] = state.chess_pieces[self.moving_piece.x][
            self.moving_piece.y]
        state.chess_pieces[self.moving_piece.x][self.moving_piece.y] = None
        if test_move is False:
            state.moves_since_capture = 0
            if self.moving_piece.is_white:
                state.chess_pieces[self.target_x][self.target_y + 1] = None
            else:
                state.chess_pieces[self.target_x][self.target_y - 1] = None
        self.moving_piece.position = self.target_position
        self.moving_piece.x = self.target_x
        self.moving_piece.y = self.target_y
        if test_move is False:
            state.is_turn_white = not state.is_turn_white
            win = state.check_win()
            return win
        return 0

    def reverse_move(self, state: State):
        if self.moving_piece.is_white:
            state.chess_pieces[self.target_x][self.target_y + 1] = self.en_passant
        else:
            state.chess_pieces[self.target_x][self.target_y - 1] = self.en_passant
        state.chess_pieces[self.original_x][self.original_y] = self.original_piece
        state.chess_pieces[self.target_x][self.target_y] = None
        self.moving_piece.position = self.original_position
        self.moving_piece.x = self.original_x
        self.moving_piece.y = self.original_y
