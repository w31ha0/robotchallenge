from config import interface, numberOfParticles, sonarToCenter, motors
from likelihood import math, calculate_likelihood, calculate_likelihood_bottle,calculate_likelihood_2
import sonic
from normal import *
import turn
import gostraight
from particleUpdate import updateRotation, update, getCurrentPosition
import math
import particleDataStructure as pds
import time
import numpy as np
import re
import operator

rangea = (105,210,0,84)
rangeb = (84,168,84,210)
rangec = (0,84,50,168)
_range = [rangea,rangeb,rangec]

def mcl(oldParticles):
    sn = sonic.Sonic()
    z = sn.getSonar() + sonarToCenter
    if z == -1:
        print "Skipping MCL as sonar distance is unreliable"
        return tuple(oldParticles)
    newParticles = []
    for particle in oldParticles:
        likelihood = calculate_likelihood_2(particle[0], particle[1], particle[2], z)
        newWeight = likelihood * particle[3]
        newParticle = (particle[0], particle[1], particle[2], newWeight)
        newParticles.append(newParticle)
    normalisedParticles = normalisation(newParticles)
    resampledParticles = resampling(normalisedParticles)
    newParticles = resampledParticles
    return newParticles


def navigateToWayPoint(wx, wy, currentPosition, particles,sonic,range_index):
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
    bottle_particles = []
    for index in range(stop_times): #Every 20 cm, stop and search for the bottle 
        preAngle = interface.getMotorAngle(motors[0])[0]
        _gostraight.run(everymotion)
        aftAngle = interface.getMotorAngle(motors[0])[0]
        disMoved = abs((aftAngle-preAngle)/(math.pi * 0.124))
        particles = [update(particles[i], disMoved) for i in range(numberOfParticles)]
        particles = mcl(particles)
        Drawer.drawParticles(particles)
        if index>=1:
            #bottle_particles.append(detect_bottle_2(sonic,getCurrentPosition(particles),bottle_particles))
            bottle_particles = detect_bottle(sonic,getCurrentPosition(particles),bottle_particles,range_index)
            if bottle_particles:
                print 'Bottle_position:',bottle_particles
        print 'current_Position:',getCurrentPosition(particles)
        
        #Drawer.drawParticles(bottle_particles)
        
    #sorted_d = fuse_information(bottle_particles,range_index)

    #    particles = moveToBottle(getCurrentPosition(particles),getBottlePosition_2(sorted_d),particles)
    particles = moveToBottle_2(getCurrentPosition(particles),getBottlePosition(bottle_particles),particles)
    return particles

def detect_bottle_2(sonic,currentPosition,bottle_Position):#(bottle_x,bottle_y,prob)
    sonic.rotateSonar_15(math.pi/2.0,-1)  #-1 is clockwise and 1 is counterclockwise
    readings,_dir = sonic.rotateSonar_15(math.pi,1)    
    sonic.rotateSonar_15(math.pi/2.0,-1)
    directionPro = find_bottlePositionProb(readings,currentPosition)
     
    for index,value in enumerate(readings):    
        bottle_direction = value[0] #bottle_direction is in degrees
        bottle_distance = value[1]  #Distance it measured
        dx = math.cos(math.radians(-90+bottle_direction+currentPosition[2]))*bottle_distance
        dy = math.sin(math.radians(-90+bottle_direction+currentPosition[2]))*bottle_distance
        bottle_Position.append((currentPosition[0]+dx,currentPosition[1]+dy,directionPro[index]))
    return max(bottle_Position,key=lambda item:item[2])
    #return bottle_Position

#Output the probability of the bottle appear at each direction
def find_bottlePositionProb(readings,currentPosition):
    ctheta = currentPosition[2] #In degrees
    prob = []    
    for index,value in enumerate(readings):
        #print ctheta + value[0] - 90  #This is the sonic direction
        prob.append(calculate_likelihood_bottle(currentPosition[0],currentPosition[1],ctheta-90+value[0],value[1]))
    #prob = np.divide(prob,sum(prob)) #Normalize
    return prob



def moveToBottle_2(currentPosition,bottlePosition,particles):
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
    distance,angle = _gostraight.run(30)
    aftAngle = interface.getMotorAngle(motors[0])[0]
    disMoved = abs((aftAngle-preAngle)/(math.pi * 0.124))
    particles = [update(particles[i], disMoved) for i in range(numberOfParticles)]
    particles = [updateRotation(particles[i], angle) for i in range(numberOfParticles)]
    return particles

def detect_bottle(sonic,currentPosition,bottle_particles,range_index):
    sonic.rotateSonar_15(math.pi/2.0,-1)
    readings,_dir = sonic.rotateSonar_15(math.pi,1)    
    sonic.rotateSonar_15(math.pi/2.0,-1)
    output =  find_closest(readings,currentPosition,range_index)
    bottle_particles.append(output)
    return bottle_particles

def find_closest(readings,currentPosition,range_index):
    i = range_index
    closest = 255
    bottle_Position = []
    for index,value in enumerate(readings):    
        bottle_direction = value[0] #bottle_direction is in degrees
        bottle_distance = value[1]  #Distance it measured
        dx = math.cos(math.radians(-90+bottle_direction+currentPosition[2]))*bottle_distance
        dy = math.sin(math.radians(-90+bottle_direction+currentPosition[2]))*bottle_distance
        bottle_Position.append((currentPosition[0]+dx,currentPosition[1]+dy,bottle_distance,bottle_direction))
    
    for index,value in enumerate(bottle_Position):
        if value[0]>_range[i][0]+12 and value[0]<_range[i][1]-12 and value[1]>_range[i][2]+12 and value[1]<_range[i][3]-12: #If it's inside the range
            if value[2]<closest: # Find the closest
                output = value
                closest=value[2]
    return output

def getBottlePosition_2(sorted_d):
    #Take the first 5 possible position and take their center
    sum_x = 0.0
    sum_y = 0.0
    sum_p = 0.0    
    for index in range(0,1):
        if sorted_d[index]:
            if sorted_d[index][1]>0.04:
                tmp = sorted_d[index][0]
                sum_x = sum_x + int(re.split('[,]',tmp)[0])*sorted_d[index][1]
                sum_y = sum_y + int(re.split('[,]',tmp)[1])*sorted_d[index][1]                                    
                sum_p = sum_p + sorted_d[index][1]
    #print 'The bottle Position is:',(sum_x/sum_p,sum_y/sum_p)        
    #return (sum_x/sum_p,sum_y/sum_p)            
    return (int(re.split('[,]',sorted_d[0][0])[0])*1.0,int(re.split('[,]',sorted_d[0][0])[1])*1.0)
    #return max(bottle_particles,key=lambda item:item[2])[0:2]

def fuse_information(bottle_particles,range_index):#(currentPosition[0]+dx,currentPosition[1]+dy,bottle_distance,bottle_direction)
    print bottle_particles
    i = range_index    
    d = {} #Create a dictionary to store all possible obstacle points 
    for index,value in enumerate(bottle_particles):
        if value[0]>_range[i][0] and value[0]<_range[i][1] and value[1]>_range[i][2] and value[1]<_range[i][3]:#Add some conditions to shrink the possible range    
            key = repr(int(round(value[0])))+','+repr(int(round(value[1]))) 
            if key in d:
                d[key] = d[key]+1
            else:
                d[key] = value[2]
   
    #Normalize the possibility
    factor=1.0/sum(d.itervalues())
    for k in d:
          d[k] = d[k]*factor
    #sorted_x will be a list of tuples sorted by the possibility e.g. ('137,12',0.123123)
    sorted_d = sorted(d.items(), key=operator.itemgetter(1),reverse = True)
    print sorted_d
    return sorted_d

        





#Output the index of the outlier in the readings
def find_outliers(readings):
    outlier_indicator = []
    for index,value in enumerate(readings):
        if index>0 and index<(len(readings)-1):        
            outlier_indicator.append((readings[index-1][1]+readings[index+1][1]-2*value[1],index))
    return max(outlier_indicator,key=lambda item:item[0])[1]


def getBottlePosition(bottle_particles): #(currentPosition[0]+dx,currentPosition[1]+dy,bottle_distance,bottle_direction)
    for item in bottle_particles:
        output = item
    #sum_x = 0.0 
    #sum_y = 0.0
    #for item in bottle_particles:
    #    sum_x = sum_x + item[0]
    #    sum_y = sum_y + item[1]
#    return (sum_x/len(bottle_particles),sum_y/len(bottle_particles))
    return output
    
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
    _gostraight.run(30)
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
