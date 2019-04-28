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

