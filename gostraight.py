import time
from config import interface, motors, touchDetected, SensorPort, touchPort
import threading 
import bumper
import math

class go(object):
    def __init__(self):
        self.start = 1
        self.touchDetected = False
        
    def run(self, length):
        angle = (length * 0.124) * 3.14159 * (100.0/108.0)
        interface.increaseMotorAngleReferences(motors[0:2], [angle, angle], [8,8])
        print SensorPort
        # Either it reached the destination or it hit something, it will stop
        while not interface.motorAngleReferencesReached(motors[0:2]) and not self.touchDetected:  
            result = [interface.getSensorValue(touchPort[0])[0], interface.getSensorValue(touchPort[1])[0]]
            if sum(result)>0:
                self.touchDetected = True
            print result
            time.sleep(0.1)
        if (self.touchDetected ==True ):
            #Stop all the motors
            #angle = interface.getMotorAngle(motors[0])[0]
            #interface.setAngleReference(motors[0],angle,0.0)
            #angle = interface.getMotorAngle(motors[1])[0]
            #interface.setAngleReference(motors[1],angle,0.0)
            print 'bumped!'
            self.touchDetected = False
            #Do something

            

            
#testing

gos = go()
gos.run(60)
