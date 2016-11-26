from config import *
import time


class Bumper:
    

    def __init__(self):
        print "Instantiated bumper class"
        self.touched = False
        print touch_detected
        #touch_detected = False
        

    def getTouch(self):
        while not touch_detected:
            result = [interface.getSensorValue(touchPort[0]), interface.getSensorValue(touchPort[1])]
            if result[0] or result[1]:
                #When detected a bump, break this loop, change the value in config file, later, when it start next path, restart this thread again
                #and change touch_detected in config file to false again.
                touch_detected = True
                self.touched = True
            else:
                self.touched = False
            time.sleep(0.5)
        return 0

    
def getTouch():
    from config import *
    while not touchDetected:
        result = [interface.getSensorValue(touchPort[0]), interface.getSensorValue(touchPort[1])]
        if result[0] or result[1]:
                #When detected a bump, break this loop, change the value in config file, later, when it start next path, restart this thread again
                #and change touch_detected in config file to false again.
            touchDetected = 1
        else:
            time.sleep(0.5)
    return 0