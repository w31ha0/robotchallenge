import particleUpdate as pu
#import place_rec_bits as prb
from config import numberOfParticles, initialPosition
import navigateToWayPoint2 as nwp
import turn
import gostraight
import sonic
import particleDataStructure as pds

waypoint1 = (84, 30, 0)
waypointa = (157.5, 30, 0)
waypointab = (126, 30, 1)
waypointb = (126, 120, 0)
waypointbc = (126, 112, 1)
waypointc = (42, 80, 0)

waypoints = [waypointa, waypointb, waypointc]

canvas = pds.Canvas()
mymap = pds.Map()
pds.drawWall(mymap, canvas)

particles = [initialPosition for i in range(numberOfParticles)]
canvas.drawParticles(particles)

_sonnic = sonic.Sonic()

_dir = 1

for index, waypoint in enumerate(waypoints):
    particles = nwp.navigateToWayPoint(waypoint[0], waypoint[1], pu.getCurrentPosition(particles), particles,_sonnic)

nwp.navigateToWayPoint(waypoint1[0], waypoint1[1], pu.getCurrentPosition(particles), particles,_sonnic)

# at each waypoint do a scan
# go to new location with detected object
# bump
# go to next waypoint
# repeat till last object is bumped
# go back to waypoint 1
