import pygame
print 'hello happy bird'

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))

gameOn = True
while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
    pygame.draw.rect(gameDisplay, [255, 255, 0], [100, 100 ,100,100])
    pygame.display.update()

