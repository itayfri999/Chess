from game.state import State
from game.board import ChessPiece
from game.pieces.king import King
from game.pieces.rook import Rook
from game.pieces.pawn import Pawn


class Move:

    def __init__(self, moving_piece: ChessPiece, target_position, state: State):
        self.moving_piece: ChessPiece = moving_piece
        self.target_position = target_position
        self.original_position = moving_piece.position
        self.original_x = moving_piece.x
        self.original_y = moving_piece.y
        self.target_x = target_position[0]
        self.target_y = target_position[1]
        self.original_piece = state.chess_pieces[self.original_x][self.original_y]
        self.original_target_piece = state.chess_pieces[self.target_x][self.target_y]
        self.is_eating_piece = False
        if moving_piece.is_white and isinstance(moving_piece, Pawn):
            self.en_passant = state.chess_pieces[self.target_x][self.target_y + 1]
        else:
            self.en_passant = state.chess_pieces[self.target_x][self.target_y - 1]

    def get_all(self):
        if self.target_position != self.moving_piece.position:
            return [self.target_position, self.is_eating_piece, self.moving_piece.get_type(),
                    self.moving_piece.position]

    def check_win(self, state, possible_moves_total):
        for i in range(8):
            for j in range(8):
                if state.chess_pieces[i][j] is not None:
                    if state.chess_pieces[i][j].is_white == state.is_turn_white:
                        possible_moves_total += state.chess_pieces[i][j].possible_moves(state)
        return possible_moves_total

    def play_move(self, state: State, test_move=False):
        if test_move is False:
            for i in range(11):
                state.last_move[11 - i] = state.last_move[11 - i - 1]
            state.last_move[0] = self
        state.chess_pieces[self.target_x][self.target_y] = state.chess_pieces[self.moving_piece.x][
            self.moving_piece.y]
        state.chess_pieces[self.moving_piece.x][self.moving_piece.y] = None

        if test_move is False:
            if isinstance(self.moving_piece, Rook) or isinstance(self.moving_piece, King):
                self.moving_piece.can_castle = False
            if self.is_eating_piece is False:
                state.moves_since_capture += 1
            else:
                state.moves_since_capture = 0
            if isinstance(self.moving_piece, Pawn):
                state.moves_since_capture = 0
        self.moving_piece.position = self.target_position
        self.moving_piece.x = self.target_x
        self.moving_piece.y = self.target_y

        # promotion
        if isinstance(self.moving_piece, Pawn):
            if self.moving_piece.is_white and self.target_y == 0:
                from game.pieces.queen import Queen
                queen = Queen(self.target_x, self.target_y, self.moving_piece.is_white)
                state.chess_pieces[self.target_x][self.target_y] = queen
            elif not self.moving_piece.is_white and self.target_y == 7:
                from game.pieces.queen import Queen
                queen = Queen(self.target_x, self.target_y, self.moving_piece.is_white)
                state.chess_pieces[self.target_x][self.target_y] = queen
        if test_move is False:
            state.is_turn_white = not state.is_turn_white
            win = state.check_win()
            return win
        return 0

    def reverse_move(self, state: State):
        state.chess_pieces[self.original_x][self.original_y] = self.original_piece
        state.chess_pieces[self.target_x][self.target_y] = self.original_target_piece
        self.moving_piece.position = self.original_position
        self.moving_piece.x = self.original_x
        self.moving_piece.y = self.original_y
        if isinstance(self.moving_piece, Pawn):
            if (self.moving_piece.is_white and self.target_y) == 0 or \
               (not self.moving_piece.is_white and self.target_y == 7):
                state.chess_pieces[self.original_x][self.original_y] = self.original_piece
