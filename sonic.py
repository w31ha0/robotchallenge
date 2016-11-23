from config import interface, SensorPort, motors
import time
import math
import threading

class Sonic:
    sonicArr = []

    def __init__(self):
        print "Instantiated sonic class"

    def getSonar(self):
        usReading = interface.getSensorValue(SensorPort)[0]
        return usReading

    def rotateSonar(self, angleRad):
        prevAngle = interface.getMotorAngle(motors[2])[0]
        interface.increaseMotorAngleReference(motors[2], angleRad, 1.5)
        t = threading.Thread(name='angleCheck', target=self.angleCheck)
        t.start()
        while not interface.motorAngleReferenceReached(motors[2]):
            time.sleep(0.001)
        t.stop()
        return self.sonicArr
    
    def angleCheck():
        while True:
            angle = interface.getMotorAngle(motors[2])[0]
            if math.degrees(abs(angle - prevAngle)) >= 5:
                print (angle - prevAngle) / math.pi * 180
                prevAngle = angle
                self.sonicArr.append(self.getSonar())


sonicObj = Sonic()

sonicArrr = sonicObj.rotateSonar(-2 * math.pi)

print sonicArrr
