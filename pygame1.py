import pygame 
import time


pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

position = [400, 300]
userInput = "no input"



gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('game_of_the_bloxx')


gameExit = False 

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
	gameDisplay.fill(black)
	pygame.draw.rect(gameDisplay, red, [position[0], position[1], 10, 10])

	time.sleep(.01)
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_w]:
		position[1] = position[1] - 10
	if pressed[pygame.K_s]:
		position[1] = position[1] + 10
	if pressed[pygame.K_a]:
		position[0] = position[0] - 10
	if pressed[pygame.K_d]:
		position[0] = position[0] + 10









#	if event.type == pygame.KEYDOWN:
#		if event.key == pygame.K_d:
#			position[0] = position[0] + 10
#		if event.key == pygame.K_a:
#			position[0] = position[0] - 10
#		if event.key == pygame.K_w:
#			position[1] = position[1] - 10
#		if event.key == pygame.K_s:
#			position[1] = position[1] + 10

	pygame.display.update()


