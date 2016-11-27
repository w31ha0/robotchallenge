import time
import brickpi
from config import interface, motors


def turn(degrees):
    angleFor90Deg = float(3.288)
    # angleFor90Deg = float(14.40)
    angleToTurn = (degrees / 90) * angleFor90Deg
    interface.increaseMotorAngleReferences(motors[0:2], [angleToTurn, -angleToTurn], [6, -6])
    while not interface.motorAngleReferencesReached(motors[0:2]):
        time.sleep(0.1)
    print 'Turning finished'
