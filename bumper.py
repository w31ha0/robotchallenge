import brickpi
from config import interface, touchPort


def getTouch:
    result = interface.getSensorValue(touchPort)
    if result:
        touched = result[0]
        return True
    else:
        return False