import pygame

pygame.init()
screen = pygame.display.set_mode((1440, 900))
chessboard = pygame.image.load("Chess_board.png").convert_alpha()
screen.blit(chessboard, (300, 45))
pygame.display.flip()
chessboard_rect = chessboard.get_rect()

print(chessboard_rect)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
