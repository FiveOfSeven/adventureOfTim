
import pygame
import time
import random


def randomBox():
    return [random.randint(0, 800), random.randint(0, 600), 20, 20]


BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

pygame.init()
screenWidth = 800
screenHeight = 600
window = pygame.display.set_mode((screenWidth, screenHeight),0,24)
pygame.display.set_caption("carl snake game")
snake = [200, 200, 20, 20]
snakeVector = [20, 0]
moveWaitStart = 20
moveWait = moveWaitStart
foodBoxes = []
newFoodStart = 300
newFoodCount = newFoodStart

carryOn = True
clock = pygame.time.Clock()
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
    
    clock.tick(60)
    #time.sleep(0.5)

    # add random food
    newFoodCount -= 1
    if newFoodCount <= 0:
        newFoodCount = newFoodStart
        foodBoxes.append(randomBox())

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_s] and snake[1] + snake[3] <= screenHeight:
        snakeVector = [0, 20]
    if pressed[pygame.K_w] and snake[1] >= 0:
        snakeVector = [0, -20]
    if pressed[pygame.K_d] and snake[0] + snake[2] <= screenWidth:
        snakeVector = [20, 0]
    if pressed[pygame.K_a] and snake[0] >= 0:
        snakeVector = [-20, 0]
    if snake[1] + snake[3] == screenHeight \
        or snake[1] == 0 \
        or snake[0] + snake[2] == screenWidth \
        or snake[0] == 0:
            carryOn = False

    if moveWait <= 0:
        snake[0] += snakeVector[0]
        snake[1] += snakeVector[1]
        moveWait = moveWaitStart
    else:
        moveWait -= 1

    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, snake, 0)
    for food in foodBoxes:
        pygame.draw.rect(window, RED, food, 0)
    pygame.display.flip()
            
