import brickpi
from config import *
import time

def getSonar(self):
    usReadingArr = []
    usReading = interface.getSensorValue(SensorPort)[0]
    time.sleep(2)
    for counter in range(0, 10):
        if 5 < usReading < 21:
            usReadingArr.append(usReading)
        if 21 <= usReading <= 150:
            usReadingArr.append(usReading - 2)
    print usReadingArr
    if len(usReadingArr) == 0:
        return -1
    elif len(usReadingArr) == 1:
        return usReadingArr[0]
    else:
        avg = sum(usReadingArr) / len(usReadingArr)
        return avg