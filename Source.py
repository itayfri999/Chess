import pygame

pygame.init()

Screen_Width = 1440
Screen_Height = 900
left_gap = 300
up_gap = 45
TileSize = 90
rows = 8
columns = 8
board_size = TileSize * rows

top_left_board_corner = (left_gap, up_gap)

IDK = (103, 127, 212)
BLACK = (0, 0, 0)
BoardGREEN = (118, 150, 86)
BoardWHITE = (238, 238, 210)

LeftMouseButton = (True, False, False)
RightMouseButton = (False, False, True)
MiddleMouseButton = (False, True, False)

screen = pygame.display.set_mode((Screen_Width, Screen_Height))

clock = pygame.time.Clock()

pygame.mouse.set_cursor(pygame.cursors.diamond)
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load('images/Chess_icon.jpeg'))
screen.fill(BLACK)

running = True


# chessboard = pygame.image.load("Chess_board.png").convert_alpha()


# chessboard_rect = chessboard.get_rect()


# screen.blit(chessboard,(left_gap,up_gap))
# pygame.display.update()


class ChessPiece:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(-10, -10, 10, 10)
        self.color = ""

    def update(self, mouse_position):
        self.rect.centerx = mouse_position[0]
        self.rect.centery = mouse_position[1]
        pygame.draw.ellipse(screen, IDK, self.rect)
        print(self.rect.x, self.rect.y)

    def draw(self, screen):
        pygame.draw.ellipse(screen, IDK, self.rect)


class Tile:
    def __init__(self):
        self.is_occupied = 0
        self.tile_x = 0  # 0-7
        self.tile_y = 0  # 0-7

        Tile()

    # def posible_moves


dantheking = ChessPiece()
print(type(dantheking))


class Bishop [Chess_piece](pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    self = pygame.image.load("images/white_bishop.png").convert_alpha()
    bishop_rect = self.get_rect()
    # self.center =


def print_board():
    flicker = True
    for i in range(0, 8):
        for j in range(0, 8):
            if flicker:

                pygame.draw.rect(screen, BoardWHITE,
                                 (left_gap + TileSize * (j), up_gap + TileSize * (i), TileSize, TileSize))
            else:
                pygame.draw.rect(screen, BoardGREEN,
                                 (left_gap + TileSize * (j), up_gap + TileSize * (i), TileSize, TileSize))
            flicker = not flicker
        flicker = not flicker

    pygame.display.update()


def get_tile_node(tile_x, tile_y):
    print()


print_board()

while running:

    for event in pygame.event.get():
        mouse_position = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed() == LeftMouseButton:
            bishop.update(mouse_position)
            bishop = ChessPiece()
            bishop.draw(screen)
            pygame.display.flip()

        if event.type == pygame.QUIT:
            running = False
