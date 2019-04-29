import pygame 
import time

# import Enemy
import sys
sys.path.insert(0, './gameClasses')
from Enemy import Enemy
from defsPygame1 import col_detect, platform_detect

pygame.init()

def platformer(pygame, dataArray):
    print("hello platformer")
    platformerExit = False
    jumpVelocity = 0
    jumpRecover = 0
    platforms_pos = [[400, 500, 300, 10], [100, 450, 300, 10], [400, 400, 50, 10], [300, 350, 50, 10], [200, 300, 50, 10], [100, 250, 50, 10], \
            [0, 200, 50, 10], [100, 150, 50, 10], [200, 100, 50, 10], [300, 50, 50, 10]]
    win_box = [500, 200, 20, 20]
    while not platformerExit:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        gameExit = True
                platformerExit = True
	pressed = pygame.key.get_pressed()
	gameDisplay.fill((0, 50, 0))
        pygame.draw.rect(gameDisplay, (255, 255, 0), [dataArray[0][0], dataArray[0][1], 20, 20])
        pygame.draw.rect(gameDisplay, (50, 0, 0), [win_box[0], win_box[1], win_box[2], win_box[3]])
        for plat_pos in platforms_pos: # draw platforms
            pygame.draw.rect(gameDisplay, (255, 100, 200), [plat_pos[0], plat_pos[1], plat_pos[2], plat_pos[3]])
        if jumpRecover > 0:
            jumpRecover -= 1
        if col_detect(dataArray[0], win_box):
            platformerExit = True
	if pressed[pygame.K_a]:
	    dataArray[0][0] -= 4
	if pressed[pygame.K_d]:
	    dataArray[0][0] += 4
        if (jumpVelocity > 0):
            dataArray[0][1] -= 4
            jumpVelocity -= 1
        #elif (dataArray[0][1] >= 500):
        elif (platform_detect(dataArray[0], platforms_pos)[0]):
            dataArray[0][1] = platform_detect(dataArray[0], platforms_pos)[1] - dataArray[0][3]
	    if pressed[pygame.K_w]:
                if jumpVelocity <= 0 and jumpRecover <= 0:
                    jumpVelocity = 20
                    jumpRecover = 60
        elif (dataArray[0][1] >= 600):
            platformerExit = True
        else:
            dataArray[0][1] += 10
	time.sleep(.01)
	pygame.display.update()

        

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
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('game_of_the_bloxx')

#delete this comment
gameExit = False

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
	gameDisplay.fill(black)
        pygame.draw.rect(gameDisplay, pink, [bullet_pos[0], bullet_pos[1], bullet_pos[2], bullet_pos[3]]) 
        pygame.draw.rect(gameDisplay, green, [enemy_pos[0], enemy_pos[1], enemy_pos[2], enemy_pos[3]])
	pygame.draw.rect(gameDisplay, red, [position[0], position[1], position[2], position[3]])	
	pygame.draw.rect(gameDisplay, white, [position[0] + 20, position[1], 10, 10])
	pygame.draw.rect(gameDisplay, green, [position[0] + 10, position[1] - 30, 10, 20])
	time.sleep(.01)
	#time.sleep(.1)
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
	if pressed[pygame.K_w]:
		position[1] = position[1] - 10
        if position[1] <= 30:
            position[1] = 30
	if pressed[pygame.K_s]:
		position[1] = position[1] + 10
        if position[1] >= 590:
            position[1] = 590
	if pressed[pygame.K_a]:
		position[0] = position[0] - 10
	if position[0] <= 0:
		position[0] = 0
	if pressed[pygame.K_d]:
		position[0] = position[0] + 10
	if position[0] >= 770:
		position[0] = 770
        if col_detect(bullet_pos, enemy_pos):
            print("collision detected")
            enemy_pos[0] = enemy_pos[0] + 100
            enemy_pos[1] = enemy_pos[1] + 100
            platformer(pygame, [position])
	pygame.display.update()
