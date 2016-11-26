import time
from config import interface, motors, touchDetected, SensorPort, touchPort
import threading 
import bumper
import math
from particleUpdate import updateRotation, update
import turn

class go(object):
    def __init__(self):
        self.start = 1
        self.touchDetected = False
        self.straightDistance = 0.0
        self.initAngle = 0.0
        
    def run(self, length):
        angle = (length * 0.124) * 3.14159 * (100.0/108.0)
        self.initAngle = interface.getMotorAngle(motors[0])[0]
        interface.increaseMotorAngleReferences(motors[0:2], [angle, angle], [8,8])
        # Either it reached the destination or it hit something, it will stop
        while not interface.motorAngleReferencesReached(motors[0:2]) and not self.touchDetected:  
            result = [interface.getSensorValue(touchPort[0])[0], interface.getSensorValue(touchPort[1])[0]]
            print result
            if sum(result)>0:
                print sum(result)
                self.touchDetected = True
            time.sleep(0.01)
        #interface.setMotorAngleReference(motors[0],interface.getMotorAngle(motors[0])[0])
        #interface.setMotorAngleReference(motors[1],interface.getMotorAngle(motors[1])[0])
        if (self.touchDetected):
            print 'bumped!'
            self.goback(10)
            return [self.straightDistance,90]
        else:
            self.straightDistance  = (interface.getMotorAngle(motors[0])[0]-self.initAngle)/(100.0/108.0)/3.14159/0.124
            return [self.straightDistance,0]
            
            #Do something
    
    def goback(self,length):
        #angle1 = -(length * 0.124) * 3.14159 * (100.0/108.0)+interface.getMotorAngle(motors[0])[0]
        #angle2 = -(length * 0.124) * 3.14159 * (100.0/108.0)+interface.getMotorAngle(motors[1])[0]
        #interface.setMotorAngleReferences(motors[0:2],[angle1,angle2],[6,6])
        angle = (length * 0.124) * 3.14159 * (100.0/108.0)
        interface.increaseMotorAngleReferences(motors[0:2], [-angle, -angle], [6,6])
        #interface.setMotorRotationSpeedReferences(motors[0:2],[-5,-5])
        #preA = interface.getMotorAngle(motors[0])[0]
        #while interface.getMotorAngle(motors[0])[0]-preA < 8:
        #    time.sleep(0.01)
        while not interface.motorAngleReferencesReached(motors[0:2]):
            time.sleep(0.1)            

        self.straightDistance  = (interface.getMotorAngle(motors[0])[0]-self.initAngle)/(100.0/108.0)/3.14159/0.124
       
        turn.turn(90)        
        self.touchDetected = False
        return 0
            

            
#testing
go1 = go()
print go1.run(60)
