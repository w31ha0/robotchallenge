from config import interface, numberOfParticles, sonarToCenter, motors
from likelihood import math, calculate_likelihood
import sonic
from normal import *
import turn
import gostraight
from particleUpdate import updateRotation, update, getCurrentPosition
import math
import particleDataStructure as pds
import time


def mcl(oldParticles):
    sn = sonic.Sonic()
    z = sn.getSonar() + sonarToCenter
    if z == -1:
        print "Skipping MCL as sonar distance is unreliable"
        return tuple(oldParticles)
    newParticles = []
    for particle in oldParticles:
        likelihood = calculate_likelihood(particle[0], particle[1], particle[2], z)
        newWeight = likelihood * particle[3]
        newParticle = (particle[0], particle[1], particle[2], newWeight)
        newParticles.append(newParticle)
    normalisedParticles = normalisation(newParticles)
    resampledParticles = resampling(normalisedParticles)
    newParticles = resampledParticles
    return newParticles


def navigateToWayPoint(wx, wy, currentPosition, particles,sonic):
    Drawer = pds.Canvas()    
    _gostraight = gostraight.go()
    bottle_particles = []
    cx = currentPosition[0]
    cy = currentPosition[1]
    ctheta = math.radians(currentPosition[2])  # We store the theta in degree
    #Calculate the distance and Angle to turn    
    angle,distance = calculate_angle_distance(cx,cy,wx,wy,ctheta,currentPosition)
    #Let it rotate towards that position
    turn.turn(math.degrees(angle))
    particles = [updateRotation(particles[i], math.degrees(angle)) for i in range(numberOfParticles)]
    
    everymotion = 20.0
    stop_times = int(distance/everymotion)
    remain_distance = distance - stop_times*everymotion
    for i in range(stop_times): #Do this process 
        preAngle = interface.getMotorAngle(motors[0])[0]
        _gostraight.run(everymotion)
        aftAngle = interface.getMotorAngle(motors[0])[0]
        disMoved = abs((aftAngle-preAngle)/(math.pi * 0.124))
        particles = [update(particles[i], disMoved) for i in range(numberOfParticles)]
        particles = mcl(particles)
        bottle_particles.append(detect_bottle(sonic,getCurrentPosition(particles)))
        print bottle_particles
        #Drawer.drawParticles(particles)
        Drawer.drawParticles(bottle_particles)
        time.sleep(1)
        
    particles = moveToBottle(getCurrentPosition(particles),getBottlePosition(bottle_particles),particles)

    return particles


def detect_bottle(sonic,currentPosition):
    sonic.rotateSonar_152(math.pi/2.0,-1)
    readings,_dir = sonic.rotateSonar_152(math.pi,1)    
    sonic.rotateSonar_152(math.pi/2.0,-1)
    outlier_index = find_outliers(readings)
    bottle_direction = readings[outlier_index][0] #bottle_direction is in degrees
    bottle_distance = readings[outlier_index][1]
    dx = math.cos(math.radians(90-bottle_direction+currentPosition[2]))*bottle_distance
    dy = math.sin(math.radians(90-bottle_direction+currentPosition[2]))*bottle_distance
    return (currentPosition[0]+dx,currentPosition[1]-dy,0)

#Output the index of the outlier in the readings
def find_outliers(readings):
    outlier_indicator = []
    for index,value in enumerate(readings):
        if index>0 and index<(len(readings)-1):        
            outlier_indicator.append((readings[index-1][1]+readings[index+1][1]-2*value[1],index))
    return max(outlier_indicator,key=lambda item:item[0])[1]


def getBottlePosition(bottle_particles):
    sum_x = 0.0 
    sum_y = 0.0
    for item in bottle_particles:
        sum_x = sum_x + item[0]
        sum_y = sum_y + item[1]
    return (sum_x/len(bottle_particles),sum_y/len(bottle_particles))

def moveToBottle(currentPosition,bottlePosition,particles):
    cx = currentPosition[0]
    cy = currentPosition[1]
    ctheta = math.radians(currentPosition[2])  # We store the theta in degree
    wx = bottlePosition[0]
    wy = bottlePosition[1]
    angle,distance = calculate_angle_distance(cx,cy,wx,wy,ctheta,currentPosition)
    turn.turn(math.degrees(angle))
    particles = [updateRotation(particles[i], math.degrees(angle)) for i in range(numberOfParticles)]
    preAngle = interface.getMotorAngle(motors[0])[0]
    _gostraight = gostraight.go()
    _gostraight.run(distance)
    aftAngle = interface.getMotorAngle(motors[0])[0]
    disMoved = abs((aftAngle-preAngle)/(math.pi * 0.124))
    particles = [update(particles[i], disMoved) for i in range(numberOfParticles)]
    return particles
    



def calculate_angle_distance(cx,cy,wx,wy,ctheta,currentPosition):
    distance = math.hypot(wx - cx, wy - cy)  # This is the main distance
    print "navigating to " + str(wx) + "," + str(wy) + " from " + str(currentPosition)
    print "distance is " + str(distance)
    angle = (math.atan2(wy - cy, wx - cx)) - ctheta  # math.atan2 returns in radians
    print "angle before is " + str(angle)
    if abs(angle) >= math.pi:
        if angle > 0:
            angle = -((math.pi * 2) - angle)
        else:
            angle = -((-math.pi * 2) - angle)
    print "angle to turn is (in radians):" + str(angle)
    return angle,distance
