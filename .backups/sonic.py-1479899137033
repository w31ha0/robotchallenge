import brickpi
from config import interface, SensorPort, motors
import time


def getSonar():
    usReading = interface.getSensorValue(SensorPort)[0]
    return usReading


def rotateSonar(angleRad):
    interface.increaseMotorAngleReference(motors[2], angleRad)
    while not interface.motorAngleReferenceReached(motors[2]):
        time.sleep(0.1)
