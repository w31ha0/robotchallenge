import numpy as np

def findAnomaly(readings, match):
    threshold = 10
    differingIndices = []

    if len(match.sig) > len(readings):
        lengthX = len(readings)
    else:
        lengthX = len(match.sig)
    for i in range(lengthX - 1):
        tmp_match = match
        oldDistance = []
        currentAngle = int(readings[i][0])
        currentDistance = readings[i][1]
        for theta in [0]:
            # for theta in [4,0,-4]:
            oldDistance.append(getSavedDistance(currentAngle - theta, tmp_match)[0])
            # if getSavedDistance(currentAngle - theta, match)[1] is False:
            #    pass
            # else:
            #    pass
            # match.sig = getSavedDistance(currentAngle-theta, match)[1]
        difference = min([old - currentDistance for old in oldDistance])
        if difference > threshold:
            differingIndices.append((currentAngle, currentDistance, difference))
    print "Anomalies: " + str(differingIndices)

    filteredIndices = []
    tmp = []
    for index, item in enumerate(differingIndices):
        if abs(item[0] - differingIndices[index - 1][0]) <= 7.0:
            tmp.append((item)
            if (differingIndices[index - 1][0], differingIndices[index - 1][1], differingIndices[index - 1][2]) not in tmp:
                tmp.append((differingIndices[index - 1][0], differingIndices[index - 1][1], differingIndices[index - 1][2])) 
        else:
            if tmp != []:
                for j in tmp:
                    totalAngle += j[0]
                    totalDifference += j[1]
                spreadDistance = np.std([i[1] for i in tmp])
                gathered = (totalAngle/len(tmp), spreadDistance, totalDifference)
                filterIndices.append((gathered, tuple(tmp)))
                tmp = []
    if tmp != []:
        for j in tmp:
            for j in tmp:
                totalAngle += j[0]
                totalDifference += j[1]
            spreadDistance = np.std([i[1] for i in tmp])
            gathered = (totalAngle/len(tmp), spreadDistance, totalDifference)
            filterIndices.append((gathered, tuple(tmp))
            tmp = []
    
            
    tmpdiff = [error[0][2] for error in filteredIndices]
    bestAngle1 = filteredIndices[tmpdiff.index(max(tmpdiff))][0][0]
    
    tmpspread = [spread[0][1] for spread in filteredIndices]
    bestAngle2 = filteredIndices[tmpspread.index(min(tmpspread))][0][0]

    print "best angle by tmpspread" + str(filteredIndices[tmpspread.index(min(tmpspread))][0][0])   
    print "best angle by tmpdiff" + str(filteredIndices[tmpdiff.index(max(tmpdiff))][0][0])
    return bestAngle1
            
a = [(22,1), (26,2), (31,2), (35,1), (39,2), (45,6), (51,10), (57,20), (62,5), (205,1), (231,5),(235,10),(240,5)]

findAnomaly(a)

def findAnomaly2(readings, match):
    threshold = 10
    differingIndices = []

    if len(match.sig) > len(readings):
        lengthX = len(readings)
    else:
        lengthX = len(match.sig)
    for i in range(lengthX - 1):
        tmp_match = match
        oldDistance = []
        currentAngle = int(readings[i][0])
        currentDistance = readings[i][1]
        for theta in [0]:
            # for theta in [4,0,-4]:
            oldDistance.append(getSavedDistance(currentAngle - theta, tmp_match)[0])
            # if getSavedDistance(currentAngle - theta, match)[1] is False:
            #    pass
            # else:
            #    pass
            # match.sig = getSavedDistance(currentAngle-theta, match)[1]
        difference = min([old - currentDistance for old in oldDistance])
        if difference > threshold:
            differingIndices.append((currentAngle, difference))
    print "Anomalies: " + str(differingIndices)

    filteredIndices = []
    tmp = []
    for index, item in enumerate(differingIndices):
        if abs(item[0] - differingIndices[index - 1][0]) <= 7.0:
            tmp.append(((item[0] + differingIndices[index - 1][0]) / 2.0, differingIndices[index - 1][1]))
        else:
            if tmp != []:
                filteredIndices.append((np.median([pair[0] for pair in tmp]), sum([pair[1] for pair in tmp])))
                tmp = []
    if tmp != []:
        filteredIndices.append((np.median([pair[0] for pair in tmp]), sum([pair[1] for pair in tmp])))
        tmp = []
    tmp2 = [error[1] for error in filteredIndices]

    print filteredIndices[tmp2.index(max(tmp2))][0]
    return filteredIndices[tmp2.index(max(tmp2))][0]