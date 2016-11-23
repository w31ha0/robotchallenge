import random
from config import *
import numpy as np


def getRandomX():
    return random.gauss(mean_x, sd_x)


def getRandomY():
    return random.gauss(mean_y, sd_y)


def getRandomTheta_f():
    return random.gauss(mean_theta, sd_theta)


def getRandomTheta_g():
    return random.gauss(mean_theta_g, sd_theta_g)


def update(particle, D):
    e = getRandomX()
    new_x = particle[0] + (D + e) * np.cos(np.deg2rad(particle[2]))
    new_y = particle[1] + (D + e) * np.sin(np.deg2rad(particle[2]))
    new_theta = particle[2] + getRandomTheta_f()
    return (new_x, new_y, new_theta, particle[3])


def updateRotation(particle, increment_theta):
    new_theta = particle[2] + increment_theta + getRandomTheta_g()
    return (particle[0], particle[1], new_theta, particle[3])


def getCurrentPosition(particles):
    ave_x, ave_y, ave_theta = 0, 0, 0
    for particle in particles:
        ave_x += particle[0] * particle[3]
        ave_y += particle[1] * particle[3]
        ave_theta += particle[2] * particle[3]
    return (ave_x, ave_y, ave_theta)


    # testcase = ((1,0,0,0.25),(0,1,0,0.25),(0,0,1,0.25))
    # print str(getCurrentPosition(testcase)) this is fine