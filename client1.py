import socket
import pygame
import json
import protocol
from client2 import LIGHT_GRAY

# Pygame constants and setup
pygame.init()
pygame.font.init()

Screen_Width = 1568
Screen_Height = 980
left_gap = 300
up_gap = 5
TileSize = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
LIGHT_GRAY = (200,200,200)
BoardGREEN = (118, 150, 86)
BoardWHITE = (238, 238, 210)
highlight_white = (176, 176, 147)
highlight_green = (77, 115, 49)
last_move_white = (247, 247, 110)
last_move_green = (185, 207, 23)

big_font = pygame.font.SysFont("Arial", 80)
small_font = pygame.font.SysFont("Arial", 40)
font = pygame.font.SysFont("Arial", 55)
screen = pygame.display.set_mode((Screen_Width, Screen_Height))

clock = pygame.time.Clock()

pygame.mouse.set_cursor(pygame.cursors.diamond)
pygame.display.set_caption("Chess")
try:
    pygame.display.set_icon(pygame.image.load('images/Chess_icon.jpeg'))
except:
    pass


class ChessClient:
    def __init__(self, host='localhost', port=9876):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.is_white = None
        self.board_state = None
        self.dragging = False
        self.dragged_piece = None
        self.original_x, self.original_y = -1, -1
        self.highlight_moves = []
        self.possible_moves_checked = []
        self.state = "waiting"  # Start in waiting room immediately
        self.winner = None
        self.running = True
        self.waiting_message = "Connecting to server..."

    def receive_messages(self):
        """Thread function to receive messages from server"""
        while self.running:
            try:
                data = protocol.recv(self.sock)
                if data:
                    message = json.loads(data)
                    self.process_server_message(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def process_server_message(self, message):
        msg_type = message.get('type')

        if msg_type == 'waiting_room':
            players_connected = message['players_connected']
            players_needed = message['players_needed']
            self.waiting_message = f"Waiting for players... {players_connected}/2 connected"
            self.state = "waiting"

        elif msg_type == 'game_start':
            self.is_white = message['is_white']
            self.state = "game"
            print(f"Game started! You are playing as {'white' if self.is_white else 'black'}")

        elif msg_type == 'game_state':
            self.board_state = message

        elif msg_type == 'possible_moves':
            # Update highlight moves with server-provided data
            self.highlight_moves = []
            for move_data in message['moves']:
                self.highlight_moves.append((move_data['target_x'], move_data['target_y']))
            self.original_x, self.original_y = message['from']

        elif msg_type == 'game_end':
            self.winner = message['result']
            self.state = "winner"

        elif msg_type == 'error':
            print(f"Server error: {message['message']}")
            # Reset dragging state on error
            self.dragging = False
            self.dragged_piece = None
            self.highlight_moves = []
            self.possible_moves_checked = []

    def update_possible_moves(self, from_x, from_y):
        """Request possible moves from server for the selected piece"""
        message = {
            'type': 'get_possible_moves',
            'from': (from_x, from_y)
        }
        protocol.send(self.sock, json.dumps(message).encode())

    def send_move(self, from_pos, to_pos):
        message = {
            'type': 'move',
            'from': from_pos,
            'to': to_pos
        }
        protocol.send(self.sock, json.dumps(message).encode())

    def send_restart(self):
        message = {
            'type': 'restart'
        }
        protocol.send(self.sock, json.dumps(message).encode())

    def get_piece_image_path(self, piece_data):
        """Get the correct image path for a chess piece"""
        color_prefix = "white" if piece_data['is_white'] else "black"
        piece_type = piece_data['type'].lower()

        # Use hyphen for main piece images
        return f"images/{color_prefix}-{piece_type}.png"

    def get_small_piece_image_path(self, piece_data):
        """Get image path for small pieces (eaten pieces display)"""
        color_prefix = "white" if piece_data['is_white'] else "black"
        piece_type = piece_data['type'].lower()
        # Use underscore for small eaten pieces
        return f"images/{color_prefix}_{piece_type}.png"

    def transform_coordinates(self, x, y):
        """Transform coordinates based on player color (flip board for black)"""
        if self.is_white:
            return x, y
        else:
            return 7 - x, 7 - y

    def inverse_transform_coordinates(self, x, y):
        """Inverse transform for mouse clicks"""
        if self.is_white:
            return x, y
        else:
            return 7 - x, 7 - y

    def print_board(self):
        """Print the chess board"""
        flicker = True
        for i in range(0, 8):
            for j in range(0, 8):
                # Transform coordinates for board drawing
                draw_i, draw_j = self.transform_coordinates(j, i)

                if flicker:
                    pygame.draw.rect(screen, BoardWHITE,
                                     (left_gap + TileSize * (draw_i), up_gap + TileSize * (draw_j), TileSize, TileSize))
                else:
                    pygame.draw.rect(screen, BoardGREEN,
                                     (left_gap + TileSize * (draw_i), up_gap + TileSize * (draw_j), TileSize, TileSize))
                flicker = not flicker
            flicker = not flicker

    def default_print(self, cords: tuple):
        """Draw a default tile"""
        x, y = cords
        draw_x, draw_y = self.transform_coordinates(x, y)

        if (x + y) % 2 == 1:
            pygame.draw.rect(screen, BoardWHITE,
                             (draw_x * TileSize + left_gap, draw_y * TileSize + up_gap, TileSize, TileSize))
        else:
            pygame.draw.rect(screen, BoardGREEN,
                             (draw_x * TileSize + left_gap, draw_y * TileSize + up_gap, TileSize, TileSize))

    def print_tile(self, x, y, skip_piece=None, default_printing=True):
        """Print a single tile with piece"""
        if default_printing:
            self.default_print((x, y))

        if self.board_state and self.board_state['board'][x][y] is not None:
            piece_data = self.board_state['board'][x][y]

            # Skip if this is the dragged piece
            if skip_piece and piece_data == skip_piece:
                return None

            image_path = self.get_piece_image_path(piece_data)

            try:
                image = pygame.image.load(image_path).convert_alpha()
                draw_x, draw_y = self.transform_coordinates(x, y)
                image_rect = image.get_rect()
                image_rect.center = (int(draw_x * TileSize + left_gap + TileSize / 2),
                                     int(draw_y * TileSize + up_gap + TileSize / 2))
                screen.blit(image, image_rect)
                return image
            except Exception as e:
                print(f"Could not load image: {image_path}, error: {e}")
        return None

    def print_tiles(self, skip_piece=None):
        """Print all tiles and pieces"""
        self.screen_reset()
        for i in range(8):
            for j in range(8):
                self.default_print((i, j))
                self.print_tile(i, j, skip_piece)

    def check_range(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def highlight(self, moves):
        """Highlight possible moves using the original logic"""
        for move in moves:
            target_x, target_y = move
            from_x, from_y = self.original_x, self.original_y

            # Transform coordinates for drawing
            draw_from_x, draw_from_y = self.transform_coordinates(from_x, from_y)
            draw_target_x, draw_target_y = self.transform_coordinates(target_x, target_y)

            # Highlight the source piece
            self.default_print((from_x, from_y))
            self.print_tile(from_x, from_y)

            # Highlight the source square
            if (from_x + from_y) % 2 == 0:
                pygame.draw.rect(screen, highlight_green,
                                 (draw_from_x * TileSize + left_gap, draw_from_y * TileSize + up_gap, TileSize,
                                  TileSize))
            else:
                pygame.draw.rect(screen, highlight_white,
                                 (draw_from_x * TileSize + left_gap, draw_from_y * TileSize + up_gap, TileSize,
                                  TileSize))

            # Highlight target squares
            if self.board_state['board'][target_x][target_y] is None:
                # Empty square - draw circle
                pygame.draw.circle(screen, highlight_green if (target_x + target_y) % 2 == 0 else highlight_white,
                                   (draw_target_x * TileSize + left_gap + TileSize // 2,
                                    draw_target_y * TileSize + up_gap + TileSize // 2),
                                   TileSize // 6)
            else:
                # Occupied square - draw capture indicator
                pygame.draw.circle(screen, highlight_green if (target_x + target_y) % 2 == 0 else highlight_white,
                                   (draw_target_x * TileSize + left_gap + TileSize // 2,
                                    draw_target_y * TileSize + up_gap + TileSize // 2),
                                   TileSize // 2)
                pygame.draw.circle(screen, BoardGREEN if (target_x + target_y) % 2 == 0 else BoardWHITE,
                                   (draw_target_x * TileSize + left_gap + TileSize // 2,
                                    draw_target_y * TileSize + up_gap + TileSize // 2),
                                   TileSize // 2.5)
                self.print_tile(target_x, target_y, skip_piece=None, default_printing=False)

    def check_number_of_pieces(self):
        """Count pieces on the board for display"""
        if not self.board_state:
            return [0] * 10

        pieces = self.board_state['board']
        counts = [0] * 10  # [white_queen, white_rook, white_knight, white_bishop, white_pawn,
        #  black_queen, black_rook, black_knight, black_bishop, black_pawn]

        for row in pieces:
            for piece in row:
                if piece:
                    idx_offset = 0 if piece['is_white'] else 5
                    piece_type = piece['type'].lower()

                    if 'queen' in piece_type:
                        counts[idx_offset + 0] += 1
                    elif 'rook' in piece_type:
                        counts[idx_offset + 1] += 1
                    elif 'knight' in piece_type:
                        counts[idx_offset + 2] += 1
                    elif 'bishop' in piece_type:
                        counts[idx_offset + 3] += 1
                    elif 'pawn' in piece_type:
                        counts[idx_offset + 4] += 1

        return counts

    def print_image(self, index_x, index_y, image_path, is_black=False):
        """Print small piece image for eaten pieces display"""
        try:
            image_p = pygame.image.load(image_path).convert_alpha()
            image_rect_p = image_p.get_rect()
            if is_black:
                image_rect_p.center = (int(index_x * TileSize / 2 + left_gap + TileSize * 8.5),
                                       int(up_gap + TileSize * 7.5 - index_y * TileSize // 2))
            else:
                image_rect_p.center = (int(index_x * TileSize / 2 + left_gap + TileSize * 8.5),
                                       int(index_y * TileSize // 2 + up_gap + TileSize // 2))
            screen.blit(image_p, image_rect_p)
        except:
            print(f"Could not load image: {image_path}")

    def print_pieces_side(self, pieces_num):
        """Display eaten pieces on the side"""
        white_queen_eaten = 1 - pieces_num[0]
        white_rook_eaten = 2 - pieces_num[1]
        white_knight_eaten = 2 - pieces_num[2]
        white_bishop_eaten = 2 - pieces_num[3]
        white_pawn_eaten = 8 - pieces_num[4]
        black_queen_eaten = 1 - pieces_num[5]
        black_rook_eaten = 2 - pieces_num[6]
        black_knight_eaten = 2 - pieces_num[7]
        black_bishop_eaten = 2 - pieces_num[8]
        black_pawn_eaten = 8 - pieces_num[9]

        index_x_w, index_y_w = 0, 0
        index_x_b, index_y_b = 0, 0

        # White eaten pieces
        for _ in range(white_queen_eaten):
            self.print_image(index_x_w, index_y_w, "images/white_queen.png")
            index_x_w += 1
            if index_x_w == 3:
                index_y_w += 1
                index_x_w = 0

        for _ in range(white_rook_eaten):
            self.print_image(index_x_w, index_y_w, "images/white_rook.png")
            index_x_w += 1
            if index_x_w == 3:
                index_y_w += 1
                index_x_w = 0

        for _ in range(white_knight_eaten):
            self.print_image(index_x_w, index_y_w, "images/white_knight.png")
            index_x_w += 1
            if index_x_w == 3:
                index_y_w += 1
                index_x_w = 0

        for _ in range(white_bishop_eaten):
            self.print_image(index_x_w, index_y_w, "images/white_bishop.png")
            index_x_w += 1
            if index_x_w == 3:
                index_y_w += 1
                index_x_w = 0

        for _ in range(white_pawn_eaten):
            self.print_image(index_x_w, index_y_w, "images/white_pawn.png")
            index_x_w += 1
            if index_x_w == 3:
                index_y_w += 1
                index_x_w = 0

        # Black eaten pieces
        for _ in range(black_queen_eaten):
            self.print_image(index_x_b, index_y_b, "images/black_queen.png", is_black=True)
            index_x_b += 1
            if index_x_b == 3:
                index_y_b += 1
                index_x_b = 0

        for _ in range(black_rook_eaten):
            self.print_image(index_x_b, index_y_b, "images/black_rook.png", is_black=True)
            index_x_b += 1
            if index_x_b == 3:
                index_y_b += 1
                index_x_b = 0

        for _ in range(black_knight_eaten):
            self.print_image(index_x_b, index_y_b, "images/black_knight.png", is_black=True)
            index_x_b += 1
            if index_x_b == 3:
                index_y_b += 1
                index_x_b = 0

        for _ in range(black_bishop_eaten):
            self.print_image(index_x_b, index_y_b, "images/black_bishop.png", is_black=True)
            index_x_b += 1
            if index_x_b == 3:
                index_y_b += 1
                index_x_b = 0

        for _ in range(black_pawn_eaten):
            self.print_image(index_x_b, index_y_b, "images/black_pawn.png", is_black=True)
            index_x_b += 1
            if index_x_b == 3:
                index_y_b += 1
                index_x_b = 0

    def screen_reset(self):
        """Reset and redraw the screen"""
        screen.fill(GRAY)

        # Draw board
        self.print_board()

        # Draw turn indicator
        if self.board_state:
            if self.is_white == self.board_state['is_turn_white']:
                text_surface1 = font.render("Your", True, WHITE)
                screen.blit(text_surface1, (TileSize // 1.5, TileSize // 2))
            else:
                text_surface1 = font.render("Opponent's", True, WHITE)
                screen.blit(text_surface1, (TileSize // 7, TileSize // 2))

            pieces_num = self.check_number_of_pieces()
            self.print_pieces_side(pieces_num)

        text_surface2 = font.render("turn", True, WHITE)
        screen.blit(text_surface2, (TileSize // 1.5, TileSize))

    def draw_text_center(self, text, font, color, y):
        """Draw centered text"""
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(Screen_Width // 2, y))
        screen.blit(surface, rect)

    def waiting_screen(self):
        """Display waiting room screen"""
        try:
            # Try to load chess board background
            background_path = "images/chess_main_screen.jpg"
            background = pygame.image.load(background_path).convert()
            background_scaled = pygame.transform.scale(background, (Screen_Width, Screen_Height))
            screen.blit(background_scaled, (0, 0))
        except:
            # Fallback to gray background
            screen.fill(GRAY)

        self.draw_text_center("Chess Game", big_font, WHITE, Screen_Height // 7)
        self.draw_text_center(self.waiting_message, font, WHITE, Screen_Height // 4)

        if "Waiting for players" in self.waiting_message:
            self.draw_text_center("Waiting for another player...", small_font, LIGHT_GRAY, Screen_Height // 4 + 60)

        pygame.display.flip()

    def winner_screen(self, winner):
        """Display winner screen"""
        screen.fill(GRAY)
        if winner == 1:
            self.draw_text_center("White Wins!", big_font, WHITE, Screen_Height // 10)
        elif winner == 2:
            try:
                black_wins_image_path = "images/chess_black_wins.jpg"
                black_wins_image = pygame.image.load(black_wins_image_path).convert()
                black_wins_image_scaled = pygame.transform.scale(black_wins_image, (Screen_Width, Screen_Height))
                screen.blit(black_wins_image_scaled, (0, 0))
            except:
                pass
            self.draw_text_center("Black Wins!", big_font, BLACK, Screen_Height // 10)
        else:
            self.draw_text_center("Draw!", big_font, BLACK, Screen_Height // 10)

        self.draw_text_center("Press ENTER to start another game", small_font, BLACK, Screen_Height // 5)
        self.draw_text_center("Press ESC to Quit", small_font, BLACK, Screen_Height // 5 + 60)
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        # Start message receiving thread
        import threading
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()

        while self.running:
            if self.state == "waiting":
                self.waiting_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False

            elif self.state == "winner":
                self.winner_screen(self.winner)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.send_restart()
                            self.state = "waiting"
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False

            elif self.state == "game":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and self.board_state:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            # Transform mouse coordinates to board coordinates
                            draw_x = (mouse_x - left_gap) // TileSize
                            draw_y = (mouse_y - up_gap) // TileSize
                            # Inverse transform to get actual board coordinates
                            tile_x, tile_y = self.inverse_transform_coordinates(draw_x, draw_y)

                            if self.check_range(tile_x, tile_y):
                                piece_data = self.board_state['board'][tile_x][tile_y]
                                if (piece_data is not None and
                                        piece_data['is_white'] == self.is_white and
                                        self.board_state['is_turn_white'] == self.is_white):
                                    self.dragging = True
                                    self.dragged_piece = piece_data
                                    self.original_x, self.original_y = tile_x, tile_y
                                    # Request possible moves from server
                                    self.update_possible_moves(tile_x, tile_y)

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and self.dragging:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            draw_x = (mouse_x - left_gap) // TileSize
                            draw_y = (mouse_y - up_gap) // TileSize
                            tile_x, tile_y = self.inverse_transform_coordinates(draw_x, draw_y)

                            if self.check_range(tile_x, tile_y):
                                # Send move to server
                                self.send_move((self.original_x, self.original_y), (tile_x, tile_y))

                            self.dragging = False
                            self.dragged_piece = None
                            self.highlight_moves = []
                            self.possible_moves_checked = []
                            self.original_x, self.original_y = -1, -1

                # Render game state
                if self.board_state:
                    self.screen_reset()
                    self.print_tiles(skip_piece=self.dragged_piece if self.dragging else None)

                    if self.highlight_moves:
                        self.highlight(self.highlight_moves)

                    if self.dragging and self.dragged_piece:
                        # Draw dragged piece at mouse position
                        image_path = self.get_piece_image_path(self.dragged_piece)
                        try:
                            image = pygame.image.load(image_path).convert_alpha()
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            image_rect = image.get_rect(center=(mouse_x, mouse_y))
                            screen.blit(image, image_rect)
                        except:
                            pass

                pygame.display.flip()
                clock.tick(60)

        self.sock.close()


if __name__ == "__main__":
    client = ChessClient()
    client.run()