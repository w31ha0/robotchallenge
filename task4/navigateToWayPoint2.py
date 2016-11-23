import math
from likelihood import *
from sonic import *
from normal import *
from turn import *
from gostraight import *
from particleUpdate import *


def mcl(oldParticles):
    z = getSonar()
    if (z == -1):
        print "Skipping MCL as sonar distance is unreliable"
        return oldParticles
    newParticles = []
    for particle in oldParticles:
        likelihood = calculate_likelihood(particle[0], particle[1], particle[2], z)
        newWeight = likelihood * particle[3]
        newParticle = (particle[0], particle[1], particle[2], newWeight)
        newParticles.append(newParticle)
    normalisedParticles = normalisation(newParticles)
    resampledParticles = resampling(normalisedParticles)
    particles = resampledParticles
    return particles


def navigateToWayPoint(wx, wy, currentPosition, particles):
    cx = currentPosition[0]
    cy = currentPosition[1]
    ctheta = math.radians(currentPosition[2])  # We store the theta in degree

    distance = math.hypot(wx - cx, wy - cy)  # This is the main distance
    print "navigating to " + str(wx) + "," + str(wy) + " from " + str(currentPosition)
    print "distance is " + str(distance)
    angle = (math.atan2(wy - cy, wx - cx)) - ctheta  # math.atan2 returns in radians
    while (abs(angle) >= (math.pi * 2)):
        if (angle > 0):
            angle -= math.pi * 2
        else:
            angle += math.pi * 2
    print "angle to turn is " + str(angle)

    turn(math.degrees(angle))
    particles = [updateRotation(particles[i], math.degrees(angle)) for i in range(numberOfParticles)]
    print "particles after turning are " + str(particles)

    steps = int(distance / step)
    remainingDistance = distance % step

    gostraight = go()
    gostraight.run(distance)

    for i in range(1, steps + 1):
        gostraight.run(step)
        particles = [update(particles[i], distance) for i in range(numberOfParticles)]
        canvas.drawParticles(particles)
        mcl(particles)
        canvas.drawParticles(particles)

    angle = (math.atan2(wy - currentPosition[0], wx - cx)) - ctheta  # math.atan2 returns in radians

    gostraight.run(remainingDistance)
    particles = [update(particles[i], distance) for i in range(numberOfParticles)]

    # update particles
    particles = mcl(particles)

    return particles
