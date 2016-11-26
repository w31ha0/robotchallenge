def findAnomaly(readings, match):
    threshold = 10
    differingIndices = []
    for i in range(len(readings)):
        currentAngle = int(readings[i][0])
        currentDistance = readings[i][1]
        oldDistance,match = getSavedDistance(currentAngle,match)
        difference = oldDistance-currentDistance
        if difference > threshold:
            differingIndices.append(currentAngle)
    print "Anomalies: " + str(differingIndices)
    filteredIndices = []
    count = 0
    for index, item in enumerate(differingIndices):
        if item - differingIndices[index-1] <= 8.0:
            filteredIndices.append((item + differeningIndices[index - 1])/2)
            count = count + 1
        else:
            count = 0
        if count == 2:
            break
    sum = 0
    for j in range(len(filteredIndices)):
        sum = sum + j
    median = sum/len(filteredIndices)
    return filteredIndices[median]

