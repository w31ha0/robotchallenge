from place_rec_bits import *
from turn import *
import particleUpdate as pu
from config import *
import navigateToWayPoint as nwp

waypoint1 = (84,30)
waypointa = (157.5,30)
waypointb = (126,147)
waypointc = (42,112)

waypoints = [waypointa,waypointb,waypointc]

signatures = SignatureContainer(5)
signatures.delete_loc_files()
particles = [initialPosition for i in range(numberOfParticles)]

for waypoint in waypoints:
        nwp.navigateToWayPoint(waypoint[0],waypoint[1] , pu.getCurrentPosition(particles), particles)
        turn(-pu.getCurrentPosition(particles)[2])
        learn_location(signatures)
