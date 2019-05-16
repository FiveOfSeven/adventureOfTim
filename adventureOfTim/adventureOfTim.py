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

def moveCloser(monster, position, magnitude):
    # later you should take into account when the vector is 0
    # position is opposite of the actual position so make opposite position
    print 'begining monster', monster
    print 'begining position', position
    #opositePosition = [-position[0], -position[1]]
    vector = [position[0] - monster[0], position[1] - monster[1]]
    # if the vector is 0, don't do anything
    x = monster[0] - position[0]
    y = monster[1] - position[1]
    realDistance = math.sqrt(x**2 + y**2)
    if vector[0] == 0 or vector[1] == 0:
        return monster
    else:
        normalizedVector = [vector[0] * magnitude / realDistance, vector[1] * magnitude / realDistance]
        newMonster = [normalizedVector[0] + monster[0], normalizedVector[1] + monster[1]]
        print 'vector', vector
        print 'normalizedVector', normalizedVector
        print 'newMonster', newMonster
        return newMonster
 
def isClose(square1, square2, maxDistance):
    print 'in isClose'
    # pythagorean theorum 
    returnBool = False
    x = square2[0] - square1[0]
    y = square2[1] - square1[1]
    realDistance = math.sqrt(x**2 + y**2)
    print 'square1', square1
    print 'square2', square2
    print 'x', x
    print 'y', y
    print 'realDistance', realDistance
    if realDistance <= maxDistance:
        returnBool = True
    return returnBool
 
pink = (255, 100, 100)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 255, 0)
yellow = (255, 255, 0)
darkBrown = (50, 25, 0)
darkGreen = (25, 50, 0)
position = [400, 300, 20, 20]
userInput = "no input"
bullet_pos = [position[0] + 10, position[1] - 2000, 5, 10]
bullet_bool = False
bullet_time = 80
bulletVector = [0, -10]
level1 = [400, 100, 30, 30]
level2 = [200, 100, 30, 30]
worldPosition = [0, 0]
backgroundCubes = []

#wallCubes = [[800, 800, 50, 80], [200, 200, 20, 20], [0, 0, 1000, 10], [0, 1000, 1000, 10], [0, 0, 10, 1000], [1000, 0, 10, 2000]]
wallCubes = [[800, 800, 50, 80], [200, 200, 20, 20], [0, 0, 1000, 10], \
    [0, 1000, 590, 10], [640, 1000, 370, 10], [0, 0, 10, 1000], \
    [1000, 0, 10, 1010]]
landCubes = [level1, level2]
landCubesStaticCount = 2 # level1 and level2 should not be deleted
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Adventure of Tim')
playerSpeed = 3
score = 0
dataArray = [position, score]
# scoreRequirements: 0 = platformer;
scoreRequirements = [50]
# moveDirection wasd determines player gun direction
moveDirection = 'w'
# monsterCube
monsters = [[900, 800, 50, 50], [-500, -500, 50, 50]]



dataArrayDisplay = pygame.display.set_mode((800,600))
# Start of the main game
pygame.display.set_caption('Adventure of Tim')
gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    gameDisplay.fill(black)
    # background tiles
    backgroundCubes = []
    for x in range(1, 6):
        for y in range(1,6):
            backgroundCubes.append([worldPosition[0] + (x * 200) - 400, worldPosition[1] + (y * 200) - 400, 100, 100])
    for cube in backgroundCubes:
        pygame.draw.rect(gameDisplay, darkBrown, [cube[0] % 1000 - 200, cube[1] % 1000 - 200, 100, 100])
        pygame.draw.rect(gameDisplay, darkBrown, [(cube[0] + 100) % 1000 - 200, (cube[1] + 100) % 1000 - 200, 100, 100])
        pygame.draw.rect(gameDisplay, darkGreen, [(cube[0] + 100) % 1000 - 200, cube[1] % 1000 - 200, 100, 100])
        pygame.draw.rect(gameDisplay, darkGreen, [cube[0] % 1000 - 200, (cube[1] + 100) % 1000 - 200, 100, 100])

    # draw level, character
    pygame.draw.rect(gameDisplay, green, [level1[0], level1[1], level1[2], level1[3]])
    pygame.draw.rect(gameDisplay, green, [level2[0], level2[1], level2[2], level2[3]])
    pygame.draw.rect(gameDisplay, red, [position[0], position[1], position[2], position[3]])    

    # monster movements
    magnitude = 5
    for monster in monsters:
        #playerGlobalPosition = [position[0] + worldPosition[0], position[1] + worldPosition[1]]
        print 'in monster'
        print 'monster', monster
        print 'worldPosition', worldPosition
        print 'position', position
        characterPosition = [position[0] - worldPosition[0] - 20, position[1] - worldPosition[1] - 20]
        print 'characterPosition', characterPosition
        #isCloseBool = isClose(worldPosition, monster, 400)
        isCloseBool = isClose(characterPosition, monster, 200)
        print 'isClose:', isCloseBool
        if isCloseBool:
            print 'in isCloseBool'
            print 'worldPosition', worldPosition
            newMonster = moveCloser(monster, characterPosition, magnitude)
            print 'new monster', newMonster
            monster[0] = newMonster[0] 
            monster[1] = newMonster[1]
            pygame.draw.rect(gameDisplay, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [monster[0] + worldPosition[0], monster[1] + worldPosition[1], monster[2], monster[3]])
        else:
            pygame.draw.rect(gameDisplay, black, [monster[0] + worldPosition[0], monster[1] + worldPosition[1], monster[2], monster[3]])
            #pygame.draw.rect(gameDisplay, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [monster[0] + worldPosition[0], monster[1] + worldPosition[1], monster[2], monster[3]])
        #pygame.draw.rect(gameDisplay, black, [monster[0], monster[1], monster[2], monster[3]])

    # player animations
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
    gameDisplay.blit(platformerScore, (level1[0], level1[1]))

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
    if pressed[pygame.K_v]:
            score = 0
    if pressed[pygame.K_b]:
            score += 10
    
    # playerCube, landCube, and bullet Cube movements
    if pressed[pygame.K_w]:
        moveDirection = 'w'
        newPosition = position[:]
        newPosition[1] -= playerSpeed
        if col_detect(newPosition, wallCubes):
            pass
        elif position[1] <= 250:
            position[1] = 250
            worldPosition[1] += playerSpeed
            for cube in landCubes:
                cube[1] = ((cube[1] + playerSpeed + 1000) % 3000) - 1000
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
        elif position[1] >= 350:
            position[1] = 350
            worldPosition[1] -= playerSpeed
            for cube in landCubes:
                cube[1] = ((cube[1] - playerSpeed + 1000) % 3000) - 1000
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
        elif position[0] <= 300:
            position[0] = 300
            worldPosition[0] += playerSpeed
            for cube in landCubes:
                cube[0] = ((cube[0] + playerSpeed + 1000) % 3000) - 1000
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
        elif position[0] >= 500:
            position[0] = 500
            worldPosition[0] -= playerSpeed
            #for cube in backgroundCubes:
            #    cube[0] = ((cube[0] - playerSpeed + 1000) % 3000) - 1000
            for cube in landCubes:
                cube[0] = ((cube[0] - playerSpeed + 1000) % 3000) - 1000
        else:
            position[0] = position[0] + playerSpeed
            if not bullet_bool:
                bullet_pos[0] = bullet_pos[0] + playerSpeed
                bullet_pos[2] = 10
                bullet_pos[3] = 5
    # go to platformer level
    if score >= scoreRequirements[0] and col_detect(bullet_pos, level1):
        bullet_pos[1] = -2000
        tempPosition = dataArray[0][:]
        dataArray = platformer(pygame, [dataArray[0], score], gameDisplay)
        dataArray[0] = tempPosition
        score = dataArray[1]
        if score < 0:
            score = 0
            dataArray[1] = 0
    # go to threeD level
    if col_detect(bullet_pos, level2):
        bullet_pos[1] = -2000
        dataArray = threeD(pygame, [dataArray[0], score], gameDisplay)
        score = dataArray[1]
    pygame.display.update()
