from config import interface, SensorPort, motors
import time
import math
from collections import Counter


class Sonic:
    sonicArr = []
    t = None

    def __init__(self):
        print "Instantiated sonic class"

    def getSonar(self):
        usReadingArr = []
        for i in range(0, 3):
            usReadingArr.append(interface.getSensorValue(SensorPort)[0])
            b = Counter(usReadingArr)
        return b.most_common(1)[0][0]

    def rotateSonar(self, angleRad, _dir):
        self.sonicArr = []
        originalAngle = interface.getMotorAngle(motors[2])[0]
        prevAngle = interface.getMotorAngle(motors[2])[0]
        interface.increaseMotorAngleReference(motors[2], _dir * angleRad, 3.0)
        while not interface.motorAngleReferenceReached(motors[2]):
            angle = interface.getMotorAngle(motors[2])[0]
            if math.degrees(abs(angle - prevAngle)) >= 4.0:
                # print (angle - prevAngle) / math.pi * 180
                prevAngle = angle
                self.sonicArr.append((abs(math.degrees(angle - originalAngle)), self.getSonar()))
            time.sleep(0.0001)
        # print len(self.sonicArr)
        return self.sonicArr, _dir


if __name__ == "__main__":
    sonicObj = Sonic()

    _dir = -1
    sonicArrr, _dir = sonicObj.rotateSonar(2 * math.pi, _dir)
    # sonicArrr = sonicObj.rotateSonarLearning()
    print sonicArrr
