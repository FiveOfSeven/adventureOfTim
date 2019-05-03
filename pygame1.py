import pygame 
import time
import copy
import math

# import Enemy
import sys
sys.path.insert(0, './gameClasses')
from Enemy import Enemy
from defsPygame1 import col_detect, platform_detect

pygame.init()

def moveSquare(squares, idx, amount):
    mySquares = copy.deepcopy(squares)
    for square in squares:
        for forIdx, point in enumerate(square):
            square[forIdx][idx] += amount

def perspectify(inSquare, spectator, color, squareSide):
    displayString =  "pygame.draw.polygon(gameDisplay, " + str(color) + ", ("
    displayBool = False
    pointArguments = 0;
    for index, point in enumerate(inSquare):
        # sub nothing = point; sub1 is where z = 0; sub2 is spectator
        # (x - x1)/(x2 - x1) = (y - y1)/(y2 - y1) = (z - z1)/(z2 - z1) = c 
        c = (float(point[2]) - 0) / (float(spectator[2]) - 0)
        # x - x1 = c * x2 - (c * x1)
        # -x1 = cx2 - cx1 - x
        # -x1 + cx1 = cx2 -x
        # x1(-1 + c) = cx2 -x
        # x1 = (cx2 - x) / (c - 1)
        if (c != 1):
            pointArguments += 1
            displayBool = True
            x1 = (c * float(spectator[0]) - float(point[0])) / (c - 1)
            y1 = (c * float(spectator[1]) - float(point[1])) / (c - 1)
            inSquare[index] = [x1, y1, inSquare[index][2]]
            displayString += "(" + str(x1) + ", " + str(y1) + "), "
    displayString += "))"
    if displayBool and pointArguments > 2:
        
        if (squareSide == "always"):
            #print "displayString: ", displayString
            exec(displayString)
        elif (squareSide == "right" and inSquare[0][0] < inSquare[1][0]):
            exec(displayString)
        elif (squareSide == "left" and inSquare[0][0] > inSquare[1][0]):
            exec(displayString)
        elif (squareSide == "top" and inSquare[0][1] > inSquare[1][1]):
            exec(displayString)
        elif (squareSide == "close" and inSquare[0][2] < spectator[2]):
            exec(displayString)
        elif (squareSide == "bottom" and inSquare[0][1] < inSquare[1][1]):
            exec(displayString)
        elif (squareSide == "far" and inSquare[0][2] > spectator[2]): 
            exec(displayString)
    return inSquare 

#square x, y, z, width, hight, depth; cube origin is at top left forward point
def cubeToPerspective(playerCube, spectator):
    perspectify([[playerCube[0], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]], \
            [playerCube[0], playerCube[1] + playerCube[4], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]]], spectator, [165, 119, 25], "bottom") #orange
    perspectify([[playerCube[0], playerCube[1], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2]], \
            [playerCube[0], playerCube[1] + playerCube[4], playerCube[2]]], spectator, [150, 200, 50], "far") #puke green
    perspectify([[playerCube[0] + playerCube[3], playerCube[1], playerCube[2] + playerCube[5]], \
            [playerCube[0] + playerCube[3], playerCube[1], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]]], spectator, [50, 100, 255], "right") #blue
    perspectify([[playerCube[0], playerCube[1], playerCube[2] + playerCube[5]], \
            [playerCube[0], playerCube[1], playerCube[2]], \
            [playerCube[0], playerCube[1] + playerCube[4], playerCube[2]], \
            [playerCube[0], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]]], spectator, [100, 20, 255], "left") #purple
    perspectify([[playerCube[0], playerCube[1], playerCube[2] + playerCube[5]], \
            [playerCube[0], playerCube[1], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1], playerCube[2] + playerCube[5]]], spectator, [50, 200, 100], "top") #light green
    perspectify([[playerCube[0], playerCube[1], playerCube[2] + playerCube[5]], \
            [playerCube[0] + playerCube[3], playerCube[1], playerCube[2] + playerCube[5]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]], \
            [playerCube[0], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]]], spectator, [50, 0, 150], "close") #dark blue

def threeD(pygame, dataArray):
    threeDExit = False
    spectator = [400, 250, 50]
    #square x, y, z, width, hight, depth; cube origin is at top left forward point
    playerCube = [325, 400, -75, 100, 100, 50]
    enemy1Cube = [325, 400, -300, 100, 100, 50]
    allCubes = [playerCube, enemy1Cube]
    # 4 points of square
    dSquare1 = [[350, 500, -50], [450, 500, -50], [450, 600, -50], [350, 600, -50]]
    dSquare2 = [[350, 500, -100], [450, 500, -100], [450, 600, -100], [350, 600, -100]]
    dSquare3 = [[450, 500, -50], [450, 500, -100], [450, 600, -100], [450, 600, -50]]
    dSquare4 = [[350, 500, -50], [350, 500, -100], [350, 600, -100], [350, 600, -50]]
    dSquare5 = [[350, 500, -50], [350, 500, -100], [450, 500, -100], [450, 500, -50]]
    dSquare6 = [[350, 600, -50], [350, 600, -100], [450, 600, -100], [450, 600, -50]]
    dSquare = [dSquare1, dSquare2, dSquare3, dSquare4, dSquare5, dSquare6]
    ppSquare = [[350, 500, -10], [450, 500, -10], [450, 600, -10], [350, 600, -10]]
    leftRail = [[0, 400, 0], [0, 400, -3000], [0, 600, -3000], [0, 600, 0]]
    rightRail = [[800, 400, 0], [800, 400, -3000], [800, 600, -3000], [800, 600, 0]]
    moveRecover = 0
    moveAmount = 10
    circleT = 0
    while not threeDExit:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
                threeDExit = True
	pressed = pygame.key.get_pressed()
	gameDisplay.fill((100, 100, 100))

        # Components of perspective
        # 3d line math: https://brilliant.org/wiki/3d-coordinate-geometry-equation-of-a-line/
        # Get the picture plane square (ppSquare) of a square in the distance (dSquare)
        # x, y, z; positive: x, right; y, down; z, backwards away from screen;
        # x is the x value of dSquare, and x1 is the x value of spectator
        # Ax + By + Cz = D
        # two-point form:
        
        # 3 dimensional line:
        # (x - x1)/(x2 - x1) = (y - y1)/(y2 - y1) = (z - z1)/(z2 - z1) = c 
        if pressed[pygame.K_q]:
            spectator[0] -= 10
        if pressed[pygame.K_t]:
            # Equation of the Circle
            # a and b is the origin of the spectator (circle)
            # (x - a)^2 + (y - b)^2 = r^2
            # parametric form
            # x = a + r((1 - t^2) / (1 + t^2))
            # y = b + r(2t / (1 + t^2))
            circleT += 0.1
            spectator[0] = 400 + 1000 * (1 - (circleT * circleT) / (1 + (circleT * circleT)))
            spectator[1] = 250 + 1000 * ((2 * circleT) / (1 + (circleT * circleT)))
        if pressed[pygame.K_e]:
            spectator[0] += 10
        if pressed[pygame.K_r]:
            circleT -= 0.1
            spectator[0] = 400 + 1000 * (1 - (circleT * circleT) / (1 + (circleT * circleT)))
            spectator[1] = 250 + 1000 * ((2 * circleT) / (1 + (circleT * circleT)))
        if abs(ppSquare[0][0]) > 10000: 
            threeDExit = True 
        if pressed[pygame.K_w] and ((spectator[1] + 0.3) <= ppSquare[0][1] or (spectator[1] - 0.3) >= ppSquare[0][1]):
            moveSquare(dSquare, 2, -moveAmount)
            playerCube[2] -= moveAmount
	if pressed[pygame.K_s]:
            moveSquare(dSquare, 2, moveAmount)
            playerCube[2] += moveAmount
	if pressed[pygame.K_a] and (dSquare1[0][0] >= 50):
            moveSquare(dSquare, 0, -moveAmount)
            playerCube[0] -= moveAmount
	if pressed[pygame.K_d] and (dSquare1[0][0] <= 700):
            moveSquare(dSquare, 0, moveAmount)
            playerCube[0] += moveAmount
	if pressed[pygame.K_k] and (dSquare1[0][1] >= 0):
            moveSquare(dSquare, 1, -moveAmount)
            playerCube[1] -= moveAmount
	if pressed[pygame.K_j] and (dSquare1[0][1] <= 700):
            moveSquare(dSquare, 1, moveAmount)
            playerCube[1] += moveAmount
        if pressed[pygame.K_z]:
            dSquare1[0][1] += 10
        if dSquare1[0][2] <= -1000:
            threeDExit = True
        perspectify(copy.deepcopy(leftRail), spectator, [255, 0, 0], "always")
        perspectify(copy.deepcopy(rightRail), spectator, [255, 0, 0], "always")
        #perspectify(copy.deepcopy(dSquare6), spectator, [165, 119, 25], "bottom") #orange
        #perspectify(copy.deepcopy(dSquare2), spectator, [150, 200, 50], "far") #puke green
        #perspectify(copy.deepcopy(dSquare3), spectator, [50, 100, 255], "right") #blue
        #perspectify(copy.deepcopy(dSquare4), spectator, [100, 20, 255], "left") #purple
        #perspectify(copy.deepcopy(dSquare5), spectator, [50, 200, 100], "top") #light green
        #perspectify(copy.deepcopy(dSquare1), spectator, [50, 0, 150], "close") #dark blue

        # 3d line distance pythagorean therom
        cubeDistances = []
        for index, cube in enumerate(allCubes):
            # d = sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2); spectator = 1; CubePoint = 2
            distance = math.sqrt((cube[0] - spectator[0]) ** 2 + (cube[1] - spectator[1]) ** 2 + (cube[2] - spectator[2]) ** 2)
            cubeDistances.append(distance)
        # sort distances
        print("sorting")
        for index1, distance1 in enumerate(cubeDistances):
            smallestDistance = distance1
            forIndex = 0
            for index2, distance2 in enumerate(cubeDistances[index1:]):
                print ("distance2: ", distance2)
                print ("smallestDistance: ", smallestDistance)
                if distance2 < smallestDistance:
                    smallestDistance = distance2
                    print ("index1: ", index1)
                    print ("index2: ", index2)
                    forIndex = index2
            print (cubeDistances)
            print("for index: ", forIndex)
            print("index1: ", index1)
            print("cube for index: ", cubeDistances[forIndex])
            print("cube index1: ", cubeDistances[index1])
            print("allCubes1: ", allCubes)
            if (cubeDistances[forIndex] > cubeDistances[index1]):
                cubeDistances[forIndex] = cubeDistances[index1]
                cubeDistances[index1] = smallestDistance
                temp = copy.deepcopy(allCubes[forIndex])
                #allCubes[forIndex] = copy.deepcopy(allCubes[index1])
                allCubes[index1] = copy.deepcopy(temp)
                print ("cube2: ", cubeDistances)
            print("allCubes2: ", allCubes)
        for cube in allCubes:
            cubeToPerspective(cube, spectator)
            
                    
                
            
        
        #cubeToPerspective(enemy1Cube, spectator)
        #cubeToPerspective(playerCube, spectator)

        #pygame.draw.polygon(gameDisplay, [50, 0, 150], ((350, 700), (100, 50), (100, 100), (50, 100)))
        #pygame.draw.polygon(gameDisplay, [50, 0, 150], ((ppSquare[0][0], ppSquare[0][1]), (ppSquare[1][0], \
        #ppSquare[1][1]), (ppSquare[2][0], ppSquare[2][1]), (ppSquare[3][0], ppSquare[3][1])))
	time.sleep(.01)
	pygame.display.update()


def platformer(pygame, dataArray):
    platformerExit = False
    jumpVelocity = 0
    jumpRecover = 0
    level1Platforms = [[400, 500, 300, 10], [100, 450, 300, 10], [400, 400, 50, 10], [300, 350, 50, 10], [200, 300, 50, 10], [100, 250, 50, 10], \
            [0, 200, 50, 10], [100, 150, 50, 10], [200, 100, 50, 10], [300, 50, 50, 10]]
    level2Platforms = [[400, 500, 300, 10], [500, 450, 10, 10], [400, 400, 10, 10], [300, 350, 10, 10], [200, 300, 10, 10], [100, 250, 10, 10], \
            [0, 200, 10, 10], [100, 150, 10, 10], [200, 100, 10, 10], [300, 50, 10, 10]]
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
        pygame.draw.rect(gameDisplay, (255, 255, 0), [dataArray[0][0], dataArray[0][1], 20, 20])
        if level == 1:
            pygame.draw.rect(gameDisplay, (200, 0, 0), [win_box[0], win_box[1], win_box[2], win_box[3]])
        elif level ==2:
            pygame.draw.rect(gameDisplay, (200, 0, 0), [win_box_level2[0], win_box_level2[1], win_box_level2[2], win_box_level2[3]])
        for plat_pos in platforms_pos: # draw platforms
            pygame.draw.rect(gameDisplay, (255, 100, 200), [plat_pos[0], plat_pos[1], plat_pos[2], plat_pos[3]])
        if jumpRecover > 0:
            jumpRecover -= 1
        if col_detect(dataArray[0], win_box) and level == 1:
            platforms_pos = level2Platforms
            level = 2
        elif col_detect(dataArray[0], win_box_level2) and level == 2:
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
            threeD(pygame, dataArray)
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
            #enemy_pos[0] = enemy_pos[0] + 100
            #enemy_pos[1] = enemy_pos[1] + 100
	    bullet_pos[1] = -2000
            platformer(pygame, [position])
	pygame.display.update()
