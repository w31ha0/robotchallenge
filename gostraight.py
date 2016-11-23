import time
from config import interface, motors


class go(object):
    def __init__(self):
        self.start = 1

    def run(self, length):
        angle = (length * 0.124) * 3.14159
        interface.increaseMotorAngleReferences(motors[0:2], [angle, angle])
        while not interface.motorAngleReferencesReached(motors[0:2]):
            time.sleep(0.1)
            
#testing
#gos = go()
#gos.run(10)
