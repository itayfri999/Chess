t ='''
import pygame

pygame.init()
screen = pygame.display.set_mode((1440, 900))
chessboard = pygame.image.load("images/Chess_board.png").convert_alpha()
screen.blit(chessboard, (300, 45))
pygame.display.flip()
chessboard_rect = chessboard.get_rect()

for i in range(3):
    for j in range(3):
        print("i:", i, "j:", j)


print(chessboard_rect)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
'''
y = (5,6)
u = y[0]
j = y[1]
print("l1:",u,"l2:",j)