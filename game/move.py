class Move:
    def __init__(self, moving_piece, target_position):
        self.moving_piece = moving_piece
        self.target_position = target_position
        self.target_x = target_position[0]
        self.target_y = target_position[1]
