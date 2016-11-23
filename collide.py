import gostraight.py
import sonic.py
import navigateToWayPoint.py

def collide(currentPosition, nextPoint):
    distance = math.hypot(currentPosition[0] - nextPoint[0], currentPosition[1] - nextPoint[1])  # This is the main distance
    Angle_before = interface.getMotorAngle(0)[0]
    ob = go()
    ob.run(-10)
    Angle_after = interface.getMotorAngle(0)[0]
    d = (Angle_after - Angle_before) / (-math.pi * 0.124)
    print 'd:', d
    particles = [update(particles[i], d) for i in range(numberOfParticles)]
    
    turnToWayPoint(nextPoint[0], nextPoint[1], currentPosition, particles)
    #calculate distance from current to end 
    
    son = Sonic()
    reading = son.getSonar()
    if reading <= distance:
        
    
    
    # when bumped, move back 10 cm 
    # turn to next waypoint
    # if see something on sensor, turn left, then turn to look at waypoint, repeat if necessary
    
    