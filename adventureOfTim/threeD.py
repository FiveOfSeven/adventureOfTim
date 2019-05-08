import pygame
import copy
import math
import time

def cubeCollision(cube1, cube2):
    xmin1 = cube1[0]
    xmax1 = cube1[0] + cube1[3]
    ymin1 = cube1[1]
    ymax1 = cube1[1] + cube1[4]
    zmin1 = cube1[2] 
    zmax1 = cube1[2] + cube1[5]
    xmin2 = cube2[0]
    xmax2 = cube2[0] + cube2[3]
    ymin2 = cube2[1]
    ymax2 = cube2[1] + cube2[4]
    zmin2 = cube2[2] 
    zmax2 = cube2[2] + cube2[5]
    collision = False
    if (xmin2 >= xmin1 and xmin2 <= xmax1 \
            or xmax2 >= xmin1 and xmax2 <= xmax1 \
            or xmin1 >= xmin2 and xmin1 <= xmax2 \
            or xmax1 >= xmin2 and xmax1 <= xmax2) \
            and (ymin2 >= ymin1 and ymin2 <= ymax1 \
            or ymax2 >= ymin1 and ymax2 <= ymax1 \
            or ymin1 >= ymin2 and ymin1 <= ymax2 \
            or ymax1 >= ymin2 and ymax1 <= ymax2) \
            and (zmin2 >= zmin1 and zmin2 <= zmax1 \
            or zmax2 >= zmin1 and zmax2 <= zmax1 \
            or zmin1 >= zmin2 and zmin1 <= zmax2 \
            or zmax1 >= zmin2 and zmax1 <= zmax2):
                collision = True
    return collision

def perspectify(inSquare, spectator, color, squareSide, gameDisplay):
    displayString =  "pygame.draw.polygon(gameDisplay, " + str(color) + ", ("
    displayBool = False
    pointArguments = 0
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
def cubeToPerspective(playerCube, spectator, gameDisplay):
    perspectify([[playerCube[0], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]], \
            [playerCube[0], playerCube[1] + playerCube[4], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]]], spectator, [165, 119, 25], "bottom", gameDisplay) #orange
    perspectify([[playerCube[0], playerCube[1], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2]], \
            [playerCube[0], playerCube[1] + playerCube[4], playerCube[2]]], spectator, [150, 200, 50], "far", gameDisplay) #puke green
    perspectify([[playerCube[0] + playerCube[3], playerCube[1], playerCube[2] + playerCube[5]], \
            [playerCube[0] + playerCube[3], playerCube[1], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]]], spectator, [50, 100, 255], "right", gameDisplay) #blue
    perspectify([[playerCube[0], playerCube[1], playerCube[2] + playerCube[5]], \
            [playerCube[0], playerCube[1], playerCube[2]], \
            [playerCube[0], playerCube[1] + playerCube[4], playerCube[2]], \
            [playerCube[0], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]]], spectator, [100, 20, 255], "left", gameDisplay) #purple
    perspectify([[playerCube[0], playerCube[1], playerCube[2] + playerCube[5]], \
            [playerCube[0], playerCube[1], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1], playerCube[2]], \
            [playerCube[0] + playerCube[3], playerCube[1], playerCube[2] + playerCube[5]]], spectator, [50, 200, 100], "top", gameDisplay) #light green
    perspectify([[playerCube[0], playerCube[1], playerCube[2] + playerCube[5]], \
            [playerCube[0] + playerCube[3], playerCube[1], playerCube[2] + playerCube[5]], \
            [playerCube[0] + playerCube[3], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]], \
            [playerCube[0], playerCube[1] + playerCube[4], playerCube[2] + playerCube[5]]], spectator, [50, 0, 150], "close", gameDisplay) #dark blue

def updateBullets(inactiveBulletCubes, activeBulletCubes, score, bulletStartPosition):
    # fibonacci function to determine the number of bullets
    # http://www.maths.surrey.ac.uk/hosted-sites/R.Knott/Fibonacci/fibFormula.html
    # n = fibonacci index (1, 2, 3, 4, 5, 6...) = bullets; Fib(n) = fib number (1, 2, 3, 5, 8...) = score
    # Fib(n) = (((1.618034^n) - (0.618034^n)) / (2.236068))
    # (1.618034^n) - (0.618034^n) = 2.236068 * score
    # (1.618034^n) - (1.618034^(-1 * n)) = 2.236068 * score
    # 6.1 calculater Nearest Fibonacci Number <= n calculator
    # i = fib index; n = fib number (score)
    # i = (log(n) + (log(5) / 2)) / (log(1.618034)
    if score <= 0:
        fibI = 1
    else:
        fibI = math.floor((math.log(score) + (math.log(5) / 2)) / (math.log(1.618034)) + 0.1)
        fibI = fibI / 3
    totalBullets = len(inactiveBulletCubes) + len(activeBulletCubes)
    if (totalBullets < fibI):
        inactiveBulletCubes.append(bulletStartPosition[:])
        inactiveBulletCubes[-1][0] = bulletStartPosition[:][0] + (len(inactiveBulletCubes) * 20)
        #time.sleep(5)
        #add a bullet to inactiveBulletCubes
    

#dataArray: position, score
def threeD(pygame, dataArray, gameDisplay):
    threeDExit = False
    spectator = [400, 250, 50]
    #square x, y, z, width, hight, depth; cube origin is at top left forward point
    playerCube = [325, 400, -75, 20, 20, 5]
    enemy1Cube = [325, 400, -300, 100, 100, 50]
    #square x, y, z, width, hight, depth, bulletIsActiveBool, airTime
    inactiveBulletCubes = []
    activeBulletCubes = []
    allCubes = [playerCube, enemy1Cube]
    # 4 points of square
    ppSquare = [[350, 500, -10], [450, 500, -10], [450, 600, -10], [350, 600, -10]]
    leftRail = [[0, 400, 0], [0, 400, -3000], [0, 600, -3000], [0, 600, 0]]
    rightRail = [[800, 400, 0], [800, 400, -3000], [800, 600, -3000], [800, 600, 0]]
    moveRecover = 0
    moveAmount = 10
    circleT = 0
    playerDead = False
    playerStartPosition = [325, 400, -75]
    bulletStartPosition = [-100, 200, -300, 10, 10, 10, 0]
    score = dataArray[1]
    shotCooldownStart = 10
    shotCooldown = 0
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

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('score: ' + str(score), True, [100, 200, 255], [255, 200, 100])
        gameDisplay.blit(text, (0,0))


        # add bullets
        if score >= 0:
            updateBullets(inactiveBulletCubes, activeBulletCubes, score, bulletStartPosition)
            


        # enemy movement
        if enemy1Cube[2] < -75:
            enemy1Cube[2] += 1
        else:
            enemy1Cube[0] = random.randint(0,700)
            enemy1Cube[1] = random.randint(0,500)
            enemy1Cube[2] = random.randint(-1000,500)
            score -= 10
            if score < 0:
                score = 0
            #threeDExit = True

        # bullet movement
        for index, bullet in reversed(list(enumerate(activeBulletCubes[:]))):
            bullet[6] += 1
            bullet[2] -= 5
            if bullet[6] > 200:
                del activeBulletCubes[index]
            if cubeCollision(bullet, enemy1Cube):
                enemy1Cube[0] = random.randint(0,700)
                enemy1Cube[1] = random.randint(0,500)
                enemy1Cube[2] = random.randint(-1000,-300)
                score += 1


        # shot cooldown
        if shotCooldown > 0:
            shotCooldown -= 1
        if pressed[pygame.K_SPACE] and shotCooldown <= 0 and len(inactiveBulletCubes) > 0:
            activeBulletCubes.append(bulletStartPosition[:])
            del inactiveBulletCubes[-1]
            activeBulletCubes[-1][0] = playerCube[0] + (playerCube[3] / 2) - (activeBulletCubes[-1][3] / 2)
            activeBulletCubes[-1][1] = playerCube[1] + (playerCube[4] / 2) - (activeBulletCubes[-1][4] / 2)
            activeBulletCubes[-1][2] = playerCube[2] + (playerCube[5] / 2) - (activeBulletCubes[-1][5] / 2)
            shotCooldown = shotCooldownStart
        #if pressed[pygame.K_q]:
        #    spectator[0] -= 10
        #if pressed[pygame.K_t]:
        #    # Equation of the Circle
        #    # a and b is the origin of the spectator (circle)
        #    # (x - a)^2 + (y - b)^2 = r^2
        #    # parametric form
        #    # x = a + r((1 - t^2) / (1 + t^2))
        #    # y = b + r(2t / (1 + t^2))
        #    circleT += 0.1
        #    spectator[0] = 400 + 1000 * (1 - (circleT * circleT) / (1 + (circleT * circleT)))
        #    spectator[1] = 250 + 1000 * ((2 * circleT) / (1 + (circleT * circleT)))
        ##if pressed[pygame.K_e]:
        ##    spectator[0] += 10
        #if pressed[pygame.K_r]:
        #    circleT -= 0.1
        #    spectator[0] = 400 + 1000 * (1 - (circleT * circleT) / (1 + (circleT * circleT)))
        #    spectator[1] = 250 + 1000 * ((2 * circleT) / (1 + (circleT * circleT)))
        if abs(ppSquare[0][0]) > 10000: 
            threeDExit = True 
        if pressed[pygame.K_k] and ((spectator[1] + 0.3) <= ppSquare[0][1] or (spectator[1] - 0.3) >= ppSquare[0][1]):
            playerCube[2] -= moveAmount
            if cubeCollision(playerCube, enemy1Cube):
                playerCube[0] = playerStartPosition[0]
                playerCube[1] = playerStartPosition[1]
                playerCube[2] = playerStartPosition[2]
        if pressed[pygame.K_j] and playerCube[2] < -50:
            playerCube[2] += moveAmount
            if cubeCollision(playerCube, enemy1Cube):
                playerCube[0] = playerStartPosition[0]
                playerCube[1] = playerStartPosition[1]
                playerCube[2] = playerStartPosition[2]
        if pressed[pygame.K_a] and (playerCube[0] >= 50):
            playerCube[0] -= moveAmount
            if cubeCollision(playerCube, enemy1Cube):
                playerCube[0] = playerStartPosition[0]
                playerCube[1] = playerStartPosition[1]
                playerCube[2] = playerStartPosition[2]
        if pressed[pygame.K_d] and (playerCube[0] <= 700):
            playerCube[0] += moveAmount
            if cubeCollision(playerCube, enemy1Cube):
                playerCube[0] = playerStartPosition[0]
                playerCube[1] = playerStartPosition[1]
                playerCube[2] = playerStartPosition[2]
        if pressed[pygame.K_w] and (playerCube[1] >= 0):
            playerCube[1] -= moveAmount
            if cubeCollision(playerCube, enemy1Cube):
                playerCube[0] = playerStartPosition[0]
                playerCube[1] = playerStartPosition[1]
                playerCube[2] = playerStartPosition[2]
        if pressed[pygame.K_s] and (playerCube[1] <= 700):
            playerCube[1] += moveAmount
            if cubeCollision(playerCube, enemy1Cube):
                playerCube[0] = playerStartPosition[0]
                playerCube[1] = playerStartPosition[1]
                playerCube[2] = playerStartPosition[2]
        if playerCube[2] <= -1000 or playerDead == True:
            threeDExit = True
        perspectify(copy.deepcopy(leftRail), spectator, [255, 0, 0], "always", gameDisplay)
        perspectify(copy.deepcopy(rightRail), spectator, [255, 0, 0], "always", gameDisplay)
        for bullet in inactiveBulletCubes:
            cubeToPerspective(bullet, spectator, gameDisplay)

        # delete, then append active bullets to allCubes
        allCubes = allCubes[0:2]
        for cube in activeBulletCubes:
            allCubes.append(cube[:])

        # 3d line distance pythagorean therom
        cubeDistances = []
        for index, cube in enumerate(allCubes):
            # d = sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2); spectator = 1; CubePoint = 2
            distance = math.sqrt((cube[0] - spectator[0]) ** 2 + (cube[1] - spectator[1]) ** 2 + (cube[2] - spectator[2]) ** 2)
            cubeDistances.append(distance)
        # sort distances
        indexArray = range(0, len(cubeDistances))
        for index1, distance1 in enumerate(cubeDistances):
            largestDistance = distance1
            forIndex = 0
            for index2, distance2 in enumerate(cubeDistances[index1 + 1:]):
                if distance2 > largestDistance:
                    largestDistance = distance2
                    forIndex = index2 + index1 + 1
                if (cubeDistances[forIndex] > cubeDistances[index1]):
                    distanceTemp = cubeDistances[forIndex]
                    cubeDistances[forIndex] = cubeDistances[index1]
                    cubeDistances[index1] = distanceTemp
                    indexTemp = indexArray[forIndex]
                    indexArray[forIndex] = indexArray[index1]
                    indexArray[index1] = indexTemp
        #display cubes
        for index in indexArray:
            cubeToPerspective(allCubes[index], spectator, gameDisplay)


        #cubeToPerspective(enemy1Cube, spectator, gameDisplay)
        #cubeToPerspective(playerCube, spectator, gameDisplay)

        #pygame.draw.polygon(gameDisplay, [50, 0, 150], ((350, 700), (100, 50), (100, 100), (50, 100)))
        #pygame.draw.polygon(gameDisplay, [50, 0, 150], ((ppSquare[0][0], ppSquare[0][1]), (ppSquare[1][0], \
        #ppSquare[1][1]), (ppSquare[2][0], ppSquare[2][1]), (ppSquare[3][0], ppSquare[3][1])))
        time.sleep(.01)
        #pdb.set_trace()
        pygame.display.update()
    score -= 10
    if score < 0:
        score = 0
    return [dataArray[0], score]