import pdb

def col_detect(squareA, squareB):
    collision = False
    subCollision = False
    if isinstance(squareB, (list,)) and isinstance(squareB[0], (list,)):
        for square in squareB:
            if col_detect(squareA, square):
                subCollision = True
    xminA = squareA[0]
    xminB = squareB[0]
    yminA = squareA[1]
    yminB = squareB[1]
    xmaxA = squareA[0] + squareA[2]
    xmaxB = squareB[0] + squareB[2]
    ymaxA = squareA[1] + squareA[3]
    ymaxB = squareB[1] + squareB[3]
    if (xminB >= xminA and xminB <= xmaxA \
        or xmaxB >= xminA and xmaxB <= xmaxA) \
        and (yminB >= yminA and yminB <= ymaxA \
        or ymaxB >= yminA and ymaxB <= ymaxA):
            collision = True
    if (xminA >= xminB and xminA <= xmaxB \
        or xmaxA >= xminB and xmaxA <= xmaxB) \
        and (yminA >= yminB and yminA <= ymaxB \
        or ymaxA >= yminB and ymaxA <= ymaxB):
            collision = True
    return collision or subCollision

def platform_detect(squareA, squareArrayB):
    #squareA is the player, squareB is the platform
    return_value = False
    ytopBVal = -300
    #pdb.set_trace()
    for squareB in squareArrayB:
        for platform in squareB:
            ytopB = platform[1]
            ybotA = squareA[1] + squareA[3]
            xminB = platform[0]
            xminA = squareA[0]
            xmaxB = platform[0] + platform[2]
            xmaxA = squareA[0] + squareA[2]
            if ((ytopB >= ybotA and ytopB <= ybotA + 11) and ((xminB <= xminA and xmaxB >= xminA) or (xminB <= xmaxA and xmaxB >= xmaxA)\
                    or (xminA <= xminB and xmaxA >= xminB) or (xminA <= xmaxB and xmaxA >= xmaxB))):
                return_value = True
                ytopBVal = ytopB
    return [return_value, ytopBVal]
