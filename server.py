import socket
import threading
import json
from game.board import Board


class ChessServer:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []  # List of (socket, is_white, player_id)
        self.waiting_clients = []  # Clients waiting for game to start
        self.board = None
        self.game_started = False
        self.running = True
        self.player_counter = 0

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)  # Only 2 players for chess
        print(f"Chess server started on {self.host}:{self.port}")

        while self.running:
            client_socket, address = self.socket.accept()
            print(f"New connection from {address}")

            if len(self.waiting_clients) < 2 and not self.game_started:
                player_id = self.player_counter
                self.player_counter += 1

                # First player is white, second is black
                is_white = len(self.waiting_clients) == 0

                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, is_white, player_id)
                )
                client_thread.start()
                self.waiting_clients.append((client_socket, is_white, player_id))

                # Send waiting room status
                self.send_waiting_room_status()

                # Start game if we have 2 players
                if len(self.waiting_clients) == 2:
                    self.start_game()
            else:
                # Game is full or already started
                self.send_game_full(client_socket)
                client_socket.close()

    def start_game(self):
        """Initialize the game board and notify clients"""
        self.board = Board()
        self.board.board_initialise()
        self.game_started = True
        self.clients = self.waiting_clients.copy()

        print("Starting new chess game!")
        self.broadcast_game_start()
        self.broadcast_game_state()

    def handle_client(self, client_socket, is_white, player_id):
        try:
            while self.running:
                data = self.recv(client_socket)
                if not data:
                    break

                message = json.loads(data)
                self.process_message(client_socket, message, is_white, player_id)

        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.remove_client(client_socket)
            client_socket.close()

    def process_message(self, client_socket, message, is_white, player_id):
        msg_type = message.get('type')

        if msg_type == 'get_possible_moves' and self.game_started:
            # Handle request for possible moves
            from_pos = message['from']
            from_x, from_y = from_pos

            piece = self.board.state.chess_pieces[from_x][from_y]
            if piece is None or piece.is_white != is_white:
                self.send_error(client_socket, "Invalid piece selection")
                return

            # Get possible moves and filter them
            possible_moves = piece.possible_moves(self.board.state)
            possible_moves_checked = self.board.state.check_king_attacked(possible_moves)

            # Send possible moves back to client
            moves_data = []
            for move in possible_moves_checked:
                moves_data.append({
                    'target_x': move.target_x,
                    'target_y': move.target_y,
                    'is_eating': move.is_eating_piece
                })

            response = {
                'type': 'possible_moves',
                'from': from_pos,
                'moves': moves_data
            }
            self.send(client_socket, json.dumps(response))

        elif msg_type == 'move' and self.game_started:
            # Verify it's the player's turn
            if is_white != self.board.state.is_turn_white:
                self.send_error(client_socket, "Not your turn")
                return

            from_pos = message['from']
            to_pos = message['to']
            from_x, from_y = from_pos
            to_x, to_y = to_pos

            # Find the piece and validate move
            piece = self.board.state.chess_pieces[from_x][from_y]
            if piece is None or piece.is_white != is_white:
                self.send_error(client_socket, "Invalid piece selection")
                return

            # Get possible moves and validate
            possible_moves = piece.possible_moves(self.board.state)
            possible_moves_checked = self.board.state.check_king_attacked(possible_moves)

            move_made = False
            for move in possible_moves_checked:
                if (to_x, to_y) == move.target_position:
                    result = move.play_move(self.board.state)
                    move_made = True

                    # Broadcast new game state to all clients
                    self.broadcast_game_state()

                    # Check for game end
                    if result in [1, 2, 3]:
                        self.broadcast_game_end(result)
                    break

            if not move_made:
                self.send_error(client_socket, "Invalid move")

        elif msg_type == 'restart':
            if self.game_started:
                self.board = Board()
                self.board.board_initialise()
                self.broadcast_game_state()
                # Move clients back to waiting room
                self.waiting_clients = self.clients.copy()
                self.game_started = False
                self.send_waiting_room_status()

    def send_waiting_room_status(self):
        """Send waiting room status to all waiting clients"""
        status = {
            'type': 'waiting_room',
            'players_connected': len(self.waiting_clients),
            'players_needed': 2 - len(self.waiting_clients)
        }

        for client_socket, _, _ in self.waiting_clients:
            self.send(client_socket, json.dumps(status))

        # Auto-start game if we have 2 players in waiting room
        if len(self.waiting_clients) == 2 and not self.game_started:
            self.start_game()

    def send_game_start(self, client_socket, is_white):
        """Notify client that game is starting"""
        message = {
            'type': 'game_start',
            'is_white': is_white
        }
        self.send(client_socket, json.dumps(message))

    def broadcast_game_start(self):
        """Notify all clients that game is starting"""
        for client_socket, is_white, _ in self.clients:
            self.send_game_start(client_socket, is_white)

    def send_game_state(self, client_socket, is_white):
        """Send current game state to a client"""
        game_state = self.serialize_game_state(is_white)
        self.send(client_socket, json.dumps(game_state))

    def broadcast_game_state(self):
        """Send current game state to all clients"""
        for client_socket, is_white, _ in self.clients:
            self.send_game_state(client_socket, is_white)

    def broadcast_game_end(self, result):
        """Notify all clients about game end"""
        message = {
            'type': 'game_end',
            'result': result
        }
        for client_socket, _, _ in self.clients:
            self.send(client_socket, json.dumps(message))

    def send_error(self, client_socket, error_msg):
        """Send error message to client"""
        message = {
            'type': 'error',
            'message': error_msg
        }
        self.send(client_socket, json.dumps(message))

    def send_game_full(self, client_socket):
        """Notify client that game is full"""
        message = {
            'type': 'game_full'
        }
        self.send(client_socket, json.dumps(message))

    def serialize_game_state(self, is_white):
        """Convert game state to serializable format"""
        if not self.board:
            return None

        # Convert board state to serializable format
        board_state = []
        for x in range(8):
            row = []
            for y in range(8):
                piece = self.board.state.chess_pieces[x][y]
                if piece:
                    row.append({
                        'type': type(piece).__name__,
                        'is_white': piece.is_white,
                        'x': piece.x,
                        'y': piece.y
                    })
                else:
                    row.append(None)
            board_state.append(row)

        return {
            'type': 'game_state',
            'board': board_state,
            'is_turn_white': self.board.state.is_turn_white,
            'player_is_white': is_white,
            'game_over': False
        }

    def remove_client(self, client_socket):
        """Remove client from active connections"""
        # Remove from waiting clients
        was_in_waiting = any(client[0] == client_socket for client in self.waiting_clients)
        self.waiting_clients = [client for client in self.waiting_clients if client[0] != client_socket]

        # Remove from game clients
        was_in_game = any(client[0] == client_socket for client in self.clients)
        self.clients = [client for client in self.clients if client[0] != client_socket]

        # If game was in progress and a client disconnects, reset the game
        if was_in_game and self.game_started:
            self.game_started = False
            self.board = None
            # Move remaining client back to waiting room
            for remaining_client, is_white, player_id in self.clients:
                if remaining_client != client_socket:
                    self.waiting_clients.append((remaining_client, is_white, player_id))
                    self.send_waiting_room_status()

        print(f"Client disconnected. {len(self.waiting_clients)} waiting, {len(self.clients)} in game.")

        # Update waiting room status for remaining clients
        self.send_waiting_room_status()

    def send(self, sock, data):
        """Wrapper for protocol.send"""
        import protocol
        protocol.send(sock, data.encode())

    def recv(self, sock):
        """Wrapper for protocol.recv"""
        import protocol
        data = protocol.recv(sock)
        return data

    def stop(self):
        self.running = False
        for client_socket, _, _ in self.waiting_clients + self.clients:
            try:
                client_socket.close()
            except:
                pass
        self.socket.close()


if __name__ == "__main__":
    server = ChessServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()