import pygame 
import time

def col_detect(squareA, squareB):
    xminA = squareA[0]
    xminB = squareB[0]
    yminA = squareA[1]
    yminB = squareB[1]
    xmaxA = squareA[0] + squareA[2]
    xmaxB = squareB[0] + squareB[2]
    ymaxA = squareA[1] + squareA[3]
    ymaxB = squareB[1] + squareB[3]
    return_value = False
    #print (xminA, xmaxA, yminA, ymaxA, xminB, xmaxB, yminB, ymaxB)
    if (xminB >= xminA and xminB <= xmaxA) or (xmaxB >= xminA and xmaxB <= xmaxA):
        #print("1")
        if yminB >= yminA and yminB <= ymaxA or ymaxB >= yminA and ymaxB <= ymaxA:
            #print("2")
            return_value = True
    if xminA >= xminB and xminA <= xmaxB or xmaxA >= xminB and xmaxA <= xmaxB:
        #print("3")
        if yminA >= yminB and yminA <= ymaxB or ymaxA >= yminB and ymaxA <= ymaxB:
            #print("4")
            return_value = True
    return return_value 



 






pygame.init()





pink = (255, 100, 100)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 255, 0)
position = [400, 300]
userInput = "no input"
bullet_pos = [position[0] + 10, position[1] - 30, 5, 10]
bullet_bool = False
bullet_time = 80
enemy_pos = [400, 100, 30, 30]
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('game_of_the_bloxx')


gameExit = False

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
	gameDisplay.fill(black)
	pygame.draw.rect(gameDisplay, red, [position[0], position[1], 10, 10])	
	pygame.draw.rect(gameDisplay, white, [position[0] + 20, position[1], 10, 10])
	pygame.draw.rect(gameDisplay, green, [position[0] + 10, position[1] - 30, 10, 20])
        pygame.draw.rect(gameDisplay, green, [enemy_pos[0], enemy_pos[1], enemy_pos[2], enemy_pos[3]])
        pygame.draw.rect(gameDisplay, pink, [bullet_pos[0], bullet_pos[1], bullet_pos[2], bullet_pos[3]]) 
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






	pygame.display.update()


