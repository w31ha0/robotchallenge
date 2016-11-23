import time
from config import interface, motors


class go(object):
    def __init__(self):
        self.start = 1

    def run(self, length):
        angle = -(length * 0.124) * 3.14159
        orgAngle = interface.getMotorAngles(motors)[0][0]
        interface.increaseMotorAngleReferences(motors, [angle, angle])
        while not interface.motorAngleReferencesReached(motors):
            motorAngles = interface.getMotorAngles(motors)
            time.sleep(0.1)
