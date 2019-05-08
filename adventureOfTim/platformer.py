import time
import pdb
import pygame
from defsPygame1 import col_detect, platform_detect

def deleteBottomSquares(level3Platforms):
    i = 0
    length = len(level3Platforms)
    while(i < length):
        if (level3Platforms[i][1] > 600):
            level3Platforms.remove(level3Platforms[i])
            length -= 1
            continue
        i += 1
        


def platformer(pygame, dataArray, gameDisplay):
    platformerExit = False
    gravityVelocity = 10
    jumpTime = 0
    jumpRecover = 0
    jumpVelocity = 4
    platformVelocity = 4
    platformQuantity = 20
    level1Platforms = [[400, 500, 300, 10], [100, 450, 300, 10], [400, 400, 50, 10], [300, 350, 50, 10], [200, 300, 50, 10], [100, 250, 50, 10], \
            [0, 200, 50, 10], [100, 150, 50, 10], [200, 100, 50, 10], [300, 50, 50, 10]]
    level2Platforms = [[400, 500, 300, 10], [500, 450, 10, 10], [400, 400, 10, 10], [300, 350, 10, 10], [200, 300, 10, 10], [100, 250, 10, 10], \
            [0, 200, 10, 10], [100, 150, 10, 10], [200, 100, 10, 10], [300, 50, 10, 10]]
    level3Platforms = [[0, 500, 800, 10], [250, 400, 100, 10], [250, 300, 100, 10], [250, 200, 100, 10], [250, 100, 100, 10], [250, 0, 100, 10]]
    platforms_pos = [[400, 500, 300, 10], [100, 450, 300, 10], [400, 400, 50, 10], [300, 350, 50, 10], [200, 300, 50, 10], [100, 250, 50, 10], \
            [0, 200, 50, 10], [100, 150, 50, 10], [200, 100, 50, 10], [300, 50, 50, 10]]
    win_box = [500, 200, 20, 20]
    win_box_level2 = [400, 100, 10, 10]
    level = 1
    while not platformerExit:
        for event in pygame.event.get():
	        if event.type == pygame.QUIT:
                   platformerExit = True
        pressed = pygame.key.get_pressed()
        gameDisplay.fill((0, 50, 0))

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('score: ' + str(dataArray[1]), True, [100, 200, 255], [255, 200, 100])
        gameDisplay.blit(text, (0,0))
        pygame.draw.rect(gameDisplay, (255, 255, 0), [dataArray[0][0], dataArray[0][1], 20, 20])
        if level == 1:
            pygame.draw.rect(gameDisplay, (200, 0, 0), [win_box[0], win_box[1], win_box[2], win_box[3]])
        elif level ==2:
            pygame.draw.rect(gameDisplay, (200, 0, 0), [win_box_level2[0], win_box_level2[1], win_box_level2[2], win_box_level2[3]])
        elif level == 3:
            # delete level3Platforms that are past the bottom of the screen
            deleteBottomSquares(level3Platforms)
            print level3Platforms, platformQuantity
            if len(level3Platforms) < platformQuantity:
                while (len(level3Platforms) > platformQuantity):
                    level3Platforms.append([random.randint(0, 700), random.randint(-2000, -100), random.randint(20, 100), 10])

            if dataArray[0][1] < 200 and jumpTime > 0:
                #dataArray[0][1] += jumpTime
                jumpVelocity = 0
                for index, platform in enumerate(level3Platforms[:]):
                    level3Platforms[index][1] += platformVelocity
            elif dataArray[0][1] >= 200 or jumpTime <= 0:
                jumpVelocity = 4
            for platform in level3Platforms:
                pygame.draw.rect(gameDisplay, (200, 150, 0), platform)
        if (level == 1) or (level == 2):
            for plat_pos in platforms_pos: # draw platforms
                pygame.draw.rect(gameDisplay, (255, 100, 200), [plat_pos[0], plat_pos[1], plat_pos[2], plat_pos[3]])
        if jumpRecover > 0:
            jumpRecover -= 1
        if col_detect(dataArray[0], win_box) and level == 1:
            platforms_pos = level2Platforms
            dataArray[1] += 5
            level = 2
        elif col_detect(dataArray[0], win_box_level2) and level == 2:
            dataArray[1] += 10
            platforms_pos = level2Platforms
            #platformerExit = True
            level = 3
        if pressed[pygame.K_a]:
	     dataArray[0][0] -= 4
        if pressed[pygame.K_d]:
	     dataArray[0][0] += 4
        if pressed[pygame.K_s]:
            jumpTime = 0
        if (jumpTime > 0):
            dataArray[0][1] -= jumpVelocity
            jumpTime -= 1
        #elif (dataArray[0][1] >= 500):
        elif (level == 3 and platform_detect(dataArray[0], [level3Platforms])[0]):
            dataArray[0][1] = platform_detect(dataArray[0], [level3Platforms])[1] - dataArray[0][3]
            if pressed[pygame.K_w]:
                if jumpTime <= 0 and jumpRecover <= 0:
                    jumpTime = 20 + (dataArray[1] / 10)
                    jumpRecover = 60
        elif (level != 3 and platform_detect(dataArray[0], [platforms_pos])[0]):
            #dataArray[0] is the player 
            dataArray[0][1] = platform_detect(dataArray[0], [platforms_pos])[1] - dataArray[0][3]
            if pressed[pygame.K_w]:
                if jumpTime <= 0 and jumpRecover <= 0:
                    jumpTime = 20 + (dataArray[1] / 10)
                    jumpRecover = 60
        elif (dataArray[0][1] >= 600):
            platformerExit = True
            #threeD(pygame, dataArray)
        else:
            #gravity
            dataArray[0][1] += gravityVelocity
        time.sleep(.01)
        pygame.display.update()
    dataArray[1] -= 10
    if dataArray[1] < 0:
        dataArray[1] = 0
    return dataArray

