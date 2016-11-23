import brickpi
import math
import particleDataStructure as pds
from config import *
import particleUpdate as pu
from navigateToWayPoint import *

waypoint1 = (84, 30)
waypoint2 = (180, 30)
waypoint3 = (180, 54)
waypoint4 = (138, 54)
waypoint5 = (138, 168)
waypoint6 = (114, 168)
waypoint7 = (114, 84)
waypoint8 = (84, 84)
waypoint9 = (84, 30)

waypoints = [waypoint2, waypoint3, waypoint4, waypoint5, waypoint6, waypoint7, waypoint8, waypoint9]

canvas = pds.Canvas()
mymap = pds.Map()
pds.drawWall(mymap, canvas)

particles = [initialPosition for i in range(numberOfParticles)]
canvas.drawParticles(particles)

for waypoint in waypoints:
    navigateToWayPoint(waypoint, particles, pu.getCurrentPosition(particles), particles)
