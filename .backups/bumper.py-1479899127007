from config import interface, touchPort
import time

def getTouch():
    result = [interface.getSensorValue(touchPort[0]), interface.getSensorValue(touchPort[1])]
    time.sleep(0.5)
    if result[0] or result[1]:
        return True
    else:
        return False
