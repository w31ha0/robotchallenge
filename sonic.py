from config import interface, SensorPort, motors
import time
import math


class Sonic:
    sonicArr = []
    t = None

    def __init__(self):
        print "Instantiated sonic class"

    def getSonar(self):
        usReading = interface.getSensorValue(SensorPort)[0]
        return usReading

    def rotateSonar(self, angleRad):
        self.sonicArr = []
        prevAngle = interface.getMotorAngle(motors[2])[0]
        interface.increaseMotorAngleReference(motors[2], angleRad, 3.0)
        while not interface.motorAngleReferenceReached(motors[2]):
            angle = interface.getMotorAngle(motors[2])[0]
            if math.degrees(abs(angle - prevAngle)) >= 4.0:
                print (angle - prevAngle) / math.pi * 180
                prevAngle = angle
                self.sonicArr.append(self.getSonar())
            time.sleep(0.01)
        #print len(self.sonicArr)
        return self.sonicArr


if __name__ == "__main__":
    sonicObj = Sonic()

    sonicArrr = sonicObj.rotateSonar(2 * math.pi)
    # sonicArrr = sonicObj.rotateSonarLearning()
    print sonicArrr
