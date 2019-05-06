import pygame

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

pygame.init()
screenWidth = 800
screenHeight = 600
window = pygame.display.set_mode((screenWidth, screenHeight),0,24)
pygame.display.set_caption("carl pong")
leftPaddle = [0, 200, 10, 50]
rightPaddle = [790, 200, 10, 50]
ball = [300, 200]
ballRadius = 10
ballVector = [2, 2]

carryOn = True
clock = pygame.time.Clock()
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False

    pressed = pygame.key.get_pressed()
    ball[0] += ballVector[0]
    ball[1] += ballVector[1]
    if ball[0] + ballRadius >= screenWidth:
        ballVector[0] = -2
    if ball[0] - ballRadius <= 0:
        ballVector[0] = 2
    if ball[1] + ballRadius >= screenHeight:
        ballVector[1] = -2
    if ball[1] - ballRadius <= 0:
        ballVector[1] = 2
    
    if pressed[pygame.K_a] and leftPaddle[1] >= 0:
        leftPaddle[1] += 2
    if pressed[pygame.K_s] and leftPaddle[1] + leftPaddle[3] <= screenHeight:
        leftPaddle[1] -= 2

    if pressed[pygame.K_j] and rightPaddle[1] >= 0:
        rightPaddle[1] += 2
    if pressed[pygame.K_k] and rightPaddle[1] + rightPaddle[3] <= screenHeight:
        rightPaddle -= 2

    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, leftPaddle, 0)
    pygame.draw.rect(window, WHITE, rightPaddle, 0)
    pygame.draw.circle(window, WHITE, ball, 10)
    pygame.display.flip()
    clock.tick(60)
            
