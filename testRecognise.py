from place_rec_bits import *
from turn import *
import particleUpdate as pu
from config import *
import navigateToWayPoint as nwp

waypoint1 = (84,30)
waypointa = (157.5,30)
waypointb = (126,120)
waypointc = (42,80)

waypoints = [waypointa,waypointb,waypointc]

signatures = SignatureContainer(5)
particles = [initialPosition for i in range(numberOfParticles)]

for waypoint in waypoints:
        particles = nwp.navigateToWayPoint(waypoint[0],waypoint[1] , pu.getCurrentPosition(particles), particles)
        angleAlign = -pu.getCurrentPosition(particles)[2]
        turn(angleAlign)
        particles = [pu.updateRotation(particles[i], angleAlign) for i in range(numberOfParticles)]
        recognize_location(signatures)
