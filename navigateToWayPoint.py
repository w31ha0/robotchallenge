from config import interface, numberOfParticles, sonarToCenter
from likelihood import math, calculate_likelihood
import sonic
from normal import *
import turn
import gostraight
from particleUpdate import updateRotation, update
import operator
import numpy as np


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


def navigateToWayPoint(wx, wy, currentPosition, particles):
    cx = currentPosition[0]
    cy = currentPosition[1]
    ctheta = math.radians(currentPosition[2])  # We store the theta in degree

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
    print "angle to turn is " + str(angle)

    if abs(math.degrees(angle) - 90) < 8:
        turn.turn(90)
        particles = [updateRotation(particles[i], 90) for i in range(numberOfParticles)]
    elif abs(math.degrees(angle) + 90) < 8:
        turn.turn(-90)
        particles = [updateRotation(particles[i], -90) for i in range(numberOfParticles)]
    else:
        turn.turn(math.degrees(angle))
        particles = [updateRotation(particles[i], math.degrees(angle)) for i in range(numberOfParticles)]

    Angle_before = interface.getMotorAngle(0)[0]

    _gostraight = gostraight.go()
    distanceMoved = _gostraight.run(distance)
    print "dist moved: " + str(distanceMoved)
    if distanceMoved[1] is 90:
        particles = [update(particles[i], distanceMoved[0]) for i in range(numberOfParticles)]
        return particles,True
    else:
        Angle_after = interface.getMotorAngle(0)[0]
        d = (Angle_after - Angle_before) / (-math.pi * 0.124)
        d = abs(d)
        print 'd:', d
        particles = [update(particles[i], d) for i in range(numberOfParticles)]
        # print "Particles are now " + str(particles)
        # update particles
        # particles = mcl(particles)
        # print "Current Position is " + str(currentPosition)
        return particles,False


def turnToWayPoint(wx, wy, currentPosition, particles):
    cx = currentPosition[0]
    cy = currentPosition[1]
    ctheta = math.radians(currentPosition[2])  # We store the theta in degree

    distance = math.hypot(wx - cx, wy - cy)  # This is the main distance
    print "navigating to " + str(wx) + "," + str(wy) + " from " + str(currentPosition)
    print "distance is " + str(distance)
    angle = (math.atan2(wy - cy, wx - cx)) - ctheta  # math.atan2 returns in radians
    if abs(angle) >= math.pi:
        if angle > 0:
            angle = -((math.pi * 2) - angle)
        else:
            angle = -((-math.pi * 2) - angle)
    print "angle to turn is " + str(angle)

    if abs(math.degrees(angle) - 90) < 8:
        turn.turn(90)
        particles = [updateRotation(particles[i], 90) for i in range(numberOfParticles)]
    elif abs(math.degrees(angle) + 90) < 8:
        turn.turn(-90)
        particles = [updateRotation(particles[i], -90) for i in range(numberOfParticles)]
    else:
        turn.turn(math.degrees(angle))
        particles = [updateRotation(particles[i], math.degrees(angle)) for i in range(numberOfParticles)]

    # Angle_before = interface.getMotorAngle(0)[0]

    # _gostraight = gostraight.go()
    # _gostraight.run(distance)
    # Angle_after = interface.getMotorAngle(0)[0]
    # d = (Angle_after - Angle_before) / (-math.pi * 0.124)
    # print 'd:', d
    # particles = [update(particles[i], d) for i in range(numberOfParticles)]

    # update particles
    particles = mcl(particles)

    return particles


def wallCheck(go, _sonnic, _dir):
    sonicArr = []
    sonicArrAngle = []
    sonicArr, _dir = _sonnic.rotateSonar(-3 * math.pi / 4, _dir)
    _dir *= -1
    zipped = zip(*sonicArr)
    min_dist = min(zipped[1])
    for son in sonicArr:
        if son[1] <= min_dist:
            sonicArrAngle.append(son[0])
    print str(sonicArr)
    minAngle = np.median(sonicArrAngle)
    print "mina angle is " + str(minAngle)
    angleToTurn = - (90 - minAngle)  # in degrees
    print "going to turn angle is " + str(-angleToTurn)
    turn.turn(-angleToTurn + 90)

    distanceToMove = 30 - min_dist
    go.run(distanceToMove)
    print 'going to move distance: ', distanceToMove

    turn.turn(-90)
    _dir = _sonnic.rotateSonar(-3 * math.pi / 4, _dir)
