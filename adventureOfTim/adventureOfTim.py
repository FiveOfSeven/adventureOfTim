import pygame 
import time
import copy
import math
import pdb
import random

# import Enemy
import sys
sys.path.insert(0, './gameClasses')
sys.path.insert(0, './adventureOfTim/gameClasses')
from Enemy import Enemy
from defsPygame1 import col_detect, platform_detect
from platformer import platformer, deleteBottomSquares
from threeD import threeD

pygame.init()


 
pink = (255, 100, 100)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 255, 0)
position = [400, 300, 20, 20]
userInput = "no input"
bullet_pos = [position[0] + 10, position[1] - 2000, 5, 10]
bullet_bool = False
bullet_time = 80
enemy_pos = [400, 100, 30, 30]
enemy2_pos = [200, 100, 30, 30]
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('game_of_the_bloxx')
playerSpeed = 5
score = 0
dataArray = [position, score]



dataArrayDisplay = pygame.display.set_mode((800,600))
# Start of the main game
pygame.display.set_caption('game_of_the_bloxx')
gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    gameDisplay.fill(black)
    pygame.draw.rect(gameDisplay, pink, [bullet_pos[0], bullet_pos[1], bullet_pos[2], bullet_pos[3]]) 
    pygame.draw.rect(gameDisplay, green, [enemy_pos[0], enemy_pos[1], enemy_pos[2], enemy_pos[3]])
    pygame.draw.rect(gameDisplay, green, [enemy2_pos[0], enemy2_pos[1], enemy2_pos[2], enemy2_pos[3]])
    pygame.draw.rect(gameDisplay, red, [position[0], position[1], position[2], position[3]])    
    pygame.draw.rect(gameDisplay, white, [position[0] + 20, position[1], 10, 10])
    pygame.draw.rect(gameDisplay, green, [position[0] + 10, position[1] - 30, 10, 20])
    time.sleep(.01)
    #time.sleep(.1)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('score: ' + str(score), True, [100, 200, 255], [255, 200, 100])
    gameDisplay.blit(text, (0,0))

    pressed = pygame.key.get_pressed()
    if bullet_bool:
        bullet_pos[1] = bullet_pos[1] - 10
        bullet_time = bullet_time - 1
        if bullet_time <= 0:
            bullet_bool = False
            bullet_time = 80
    if pressed[pygame.K_SPACE] and bullet_bool == False:
        bullet_bool = True
        bullet_pos[1] = position[1] - 20
        bullet_pos[0] = position[0] + 13
    if pressed[pygame.K_b]:
            score += 10
    if pressed[pygame.K_w]:
        position[1] = position[1] - playerSpeed
        if position[1] <= 30:
            position[1] = 30
    if pressed[pygame.K_s]:
        position[1] = position[1] + playerSpeed
        if position[1] >= 590:
            position[1] = 590
    if pressed[pygame.K_a]:
        position[0] = position[0] - playerSpeed
    if position[0] <= 0:
        position[0] = 0
    if pressed[pygame.K_d]:
        position[0] = position[0] + playerSpeed
    if position[0] >= 770:
        position[0] = 770
    if col_detect(bullet_pos, enemy_pos):
        #enemy_pos[0] = enemy_pos[0] + 100
        #enemy_pos[1] = enemy_pos[1] + 100
        bullet_pos[1] = -2000
        dataArray = platformer(pygame, [dataArray[0], score], gameDisplay)
        score = dataArray[1]
        if score < 0:
            score = 0
            dataArray[1] = 0
    if col_detect(bullet_pos, enemy2_pos):
        bullet_pos[1] = -2000
        dataArray = threeD(pygame, [dataArray[0], score], gameDisplay)
        score = dataArray[1]
    pygame.display.update()
