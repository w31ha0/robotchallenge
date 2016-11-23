from config import interface, SensorPort, motors
import time
import math
import threading

class Sonic:
    sonicArr = []

    def __init__(self):
        print "Instantiated sonic class"
        self._stop = threading.Event()
        self.runningThread = True

    def getSonar(self):
        usReading = interface.getSensorValue(SensorPort)[0]
        return usReading

    def rotateSonar(self, angleRad):
        prevAngle = interface.getMotorAngle(motors[2])[0]
        interface.increaseMotorAngleReference(motors[2], angleRad, 1.5)
        t = threading.Thread(name='angleCheck', target=self.angleCheck(prevAngle))
        t.start()
        while not interface.motorAngleReferenceReached(motors[2]):
            time.sleep(0.01)
            
        print self.runningThread
        self.runningThread = False
        return self.sonicArr
    
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    
    def angleCheck(self, prevAngle):
        while self.runningThread:
            angle = interface.getMotorAngle(motors[2])[0]
            if math.degrees(abs(angle - prevAngle)) >= 4.5:
                print (angle - prevAngle) / math.pi * 180
                prevAngle = angle
                self.sonicArr.append(self.getSonar())
        print 'Thread Stopped'
        return 0

if __name__ == "__main__":
    sonicObj = Sonic()

    sonicArrr = sonicObj.rotateSonar(-1 * math.pi)

    print sonicArrr
