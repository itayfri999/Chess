import socket
import protocol
import pygame

server = socket.socket()
server.bind(("127.0.0.1", 9876))
server.listen()
client, adr = server.accept()


# Chess Pieces


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = (x, y)


class Bishop_W(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Color = "White"

    self = pygame.image.load("images/white_bishop.png").convert_alpha()
    bishop_rect = self.get_rect()
    #self.center =

    pygame.rect.move(10, 5)
