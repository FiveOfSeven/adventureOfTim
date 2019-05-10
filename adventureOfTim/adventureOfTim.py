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
yellow = (255, 255, 0)
position = [400, 300, 20, 20]
userInput = "no input"
bullet_pos = [position[0] + 10, position[1] - 2000, 5, 10]
bullet_bool = False
bullet_time = 80
bulletVector = [0, -10]
enemy_pos = [400, 100, 30, 30]
enemy2_pos = [200, 100, 30, 30]
wallCubes = [[800, 800, 50, 80], [200, 200, 20, 20], [0, 0, 1000, 10], [0, 1000, 1000, 10], [0, 0, 10, 1000], [1000, 0, 10, 2000]]
landCubes = [enemy_pos, enemy2_pos]
landCubesStaticCount = 2 # enemy_pos and enemy2_pos should not be deleted
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Adventure of Tim')
playerSpeed = 3
score = 0
dataArray = [position, score]
# scoreRequirements: 0 = platformer;
scoreRequirements = [50]
# moveDirection wasd determines player gun direction
moveDirection = 'w'



dataArrayDisplay = pygame.display.set_mode((800,600))
# Start of the main game
pygame.display.set_caption('Adventure of Tim')
gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    gameDisplay.fill(black)
    pygame.draw.rect(gameDisplay, green, [enemy_pos[0], enemy_pos[1], enemy_pos[2], enemy_pos[3]])
    pygame.draw.rect(gameDisplay, green, [enemy2_pos[0], enemy2_pos[1], enemy2_pos[2], enemy2_pos[3]])
    pygame.draw.rect(gameDisplay, red, [position[0], position[1], position[2], position[3]])    
    if moveDirection == 'w':
        pygame.draw.rect(gameDisplay, (204, 102, 0), [position[0] + 2, position[1] - 15, 5, 15])
        pygame.draw.rect(gameDisplay, (204, 102, 0), [position[0] + 13, position[1] - 15, 5, 15])
    elif moveDirection == 'a':
        pygame.draw.rect(gameDisplay, (204, 102, 0), [position[0] - 15, position[1] + 13, 15, 5])
        pygame.draw.rect(gameDisplay, (204, 102, 0), [position[0] - 15, position[1] + 2, 15, 5])
    elif moveDirection == 's':
        pygame.draw.rect(gameDisplay, (204, 102, 0), [position[0] + 2, position[1] + 20, 5, 15])
        pygame.draw.rect(gameDisplay, (204, 102, 0), [position[0] + 13, position[1] + 20, 5, 15])
    elif moveDirection == 'd':
        pygame.draw.rect(gameDisplay, (204, 102, 0), [position[0] + 20, position[1] + 13, 15, 5])
        pygame.draw.rect(gameDisplay, (204, 102, 0), [position[0] + 20, position[1] + 2, 15, 5])
    for cube in wallCubes:
        pygame.draw.rect(gameDisplay, yellow, [cube[0], cube[1], cube[2], cube[3]])
    pygame.draw.rect(gameDisplay, pink, [bullet_pos[0], bullet_pos[1], bullet_pos[2], bullet_pos[3]]) 

    # add wallCubes to landCubes
    landCubes = landCubes[0:landCubesStaticCount]
    for cube in wallCubes:
        landCubes.append(cube)
        

    time.sleep(.01)
    #time.sleep(.1)

    font = pygame.font.Font('freesansbold.ttf', 32)
    smallFont = pygame.font.Font('freesansbold.ttf', 12)
    text = font.render('score: ' + str(score), True, [100, 200, 255], [255, 200, 100])
    platformerScore = smallFont.render(str(scoreRequirements[0]), True, [0, 0, 0], [255, 255, 255])
    gameDisplay.blit(text, (0,0))
    gameDisplay.blit(platformerScore, (enemy_pos[0], enemy_pos[1]))

    pressed = pygame.key.get_pressed()
    if bullet_bool:
        bullet_pos[1] = bullet_pos[1] + bulletVector[1]
        bullet_pos[0] = bullet_pos[0] + bulletVector[0]
        if bulletVector[1] == 0:
            bullet_pos[2] = 10
            bullet_pos[3] = 5
        else:
            bullet_pos[2] = 5
            bullet_pos[3] = 10
        bullet_time = bullet_time - 1
        if bullet_time <= 0:
            bullet_bool = False
            bullet_time = 80
            bullet_pos[0] = position[0] + 3
            bullet_pos[1] = position[1] + 3
            bullet_pos[2] = 10
            bullet_pos[3] = 5
    if pressed[pygame.K_SPACE] and bullet_bool == False:
        bullet_bool = True
        if moveDirection == 'w':
            bullet_pos[0] = position[0] + 8
            bullet_pos[1] = position[1]
            bulletVector = [0, -10]
        if moveDirection == 'a':
            bullet_pos[0] = position[0] - 15
            bullet_pos[1] = position[1] + 8
            bulletVector = [-10, 0]
        if moveDirection == 's':
            bullet_pos[0] = position[0] + 8
            bullet_pos[1] = position[1] + 20
            bulletVector = [0, 10]
        if moveDirection == 'd':
            bullet_pos[0] = position[0] + 20
            bullet_pos[1] = position[1] + 8
            bulletVector = [10, 0]
    if pressed[pygame.K_b]:
            score += 10
    if pressed[pygame.K_v]:
            score = 0
    if pressed[pygame.K_w]:
        moveDirection = 'w'
        newPosition = position[:]
        newPosition[1] -= playerSpeed
        if col_detect(newPosition, wallCubes):
            pass
        elif position[1] <= 200:
            position[1] = 200
            for cube in landCubes:
                cube[1] += playerSpeed
        else:
            position[1] = position[1] - playerSpeed
            if not bullet_bool:
                bullet_pos[1] = bullet_pos[1] - playerSpeed
                bullet_pos[2] = 10
                bullet_pos[3] = 5
    if pressed[pygame.K_s]:
        moveDirection = 's'
        newPosition = position[:]
        newPosition[1] += playerSpeed
        if col_detect(newPosition, wallCubes):
            pass
        elif position[1] >= 400:
            position[1] = 400
            for cube in landCubes:
                cube[1] -= playerSpeed
        else:
            position[1] = position[1] + playerSpeed
            if not bullet_bool:
                bullet_pos[1] = bullet_pos[1] + playerSpeed
                bullet_pos[2] = 10
                bullet_pos[3] = 5
    if pressed[pygame.K_a]:
        moveDirection = 'a'
        newPosition = position[:]
        newPosition[0] -= playerSpeed
        if col_detect(newPosition, wallCubes):
            pass
        elif position[0] <= 200:
            position[0] = 200
            for cube in landCubes:
                cube[0] += playerSpeed
        else:
            position[0] = position[0] - playerSpeed
            if not bullet_bool:
                bullet_pos[0] = bullet_pos[0] - playerSpeed
                bullet_pos[2] = 10
                bullet_pos[3] = 5
    if pressed[pygame.K_d]:
        moveDirection = 'd'
        newPosition = position[:]
        newPosition[0] += playerSpeed
        if col_detect(newPosition, wallCubes):
            pass
        elif position[0] >= 600:
            position[0] = 600
            for cube in landCubes:
                cube[0] -= playerSpeed
        else:
            position[0] = position[0] + playerSpeed
            if not bullet_bool:
                bullet_pos[0] = bullet_pos[0] + playerSpeed
                bullet_pos[2] = 10
                bullet_pos[3] = 5
    # go to platformer level
    if score >= scoreRequirements[0] and col_detect(bullet_pos, enemy_pos):
        bullet_pos[1] = -2000
        tempPosition = dataArray[0][:]
        dataArray = platformer(pygame, [dataArray[0], score], gameDisplay)
        dataArray[0] = tempPosition
        score = dataArray[1]
        if score < 0:
            score = 0
            dataArray[1] = 0
    # go to threeD level
    if col_detect(bullet_pos, enemy2_pos):
        bullet_pos[1] = -2000
        dataArray = threeD(pygame, [dataArray[0], score], gameDisplay)
        score = dataArray[1]
    pygame.display.update()
