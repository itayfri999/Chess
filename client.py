import socket
import protocol
import pygame

sock = socket.socket()
sock.connect(("127.0.0.1", 9876))
data = protocol.recv(sock)
with open("Chess_board.png", 'wb') as f:
    f.write(data)

LeftMouseButton = (True, False, False)
RightMouseButton = (False, False, True)
MiddleMouseButton = (False, True, False)


running = True
while running:
    for event in pygame.event.get():
        mouse_position = pygame.mouse.get_pos()
        protocol.send(sock, f"MOUSE_POSITION {mouse_position[0]} {mouse_position[1]}").encode()

        if pygame.mouse.get_pressed() == LeftMouseButton:
            print()

        if event.type == pygame.QUIT:
            running = False
            protocol.send(b"quit")
