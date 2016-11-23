from config import interface, touchPort
import time


class Bumper:
    

    def __init__(self):
        print "Instantiated bumper class"
        self.touched = False

    def getTouch(self):
        while True:
            result = [interface.getSensorValue(touchPort[0]), interface.getSensorValue(touchPort[1])]
            if result[0] or result[1]:
                self.touched = True
            else:
                self.touched = False
            time.sleep(0.5)
