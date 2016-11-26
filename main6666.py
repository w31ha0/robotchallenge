import math
import particleDataStructure as pds
import particleUpdate as pu
import place_rec_bits as prb
from config import *
import navigateToWayPoint as nwp
import threading
import bumper
import turn
import gostraight

waypoint1 = (84, 30)
waypointa = (157.5, 30)
waypointb = (126, 147)
waypointc = (42, 112)

waypoints = [waypointa, waypointb, waypointc]

canvas = pds.Canvas()
mymap = pds.Map()
pds.drawWall(mymap, canvas)

particles = [initialPosition for i in range(numberOfParticles)]
canvas.drawParticles(particles)
signatures = prb.SignatureContainer()

#bumper = bumper.Bumper()
#bumperThread = threading.Thread(name='bumper', target=bumper.getTouch)
#bumperThread.start()

_dir = 1

for index, waypoint in enumerate(waypoints):
    particles = nwp.navigateToWayPoint(waypoint[0], waypoint[1], pu.getCurrentPosition(particles), particles)
    # include bumped here, then subsequent action
    current_particles = pu.getCurrentPosition(particles)
    ls = prb.LocationSignature()
    _dir,readings = prb.characterize_location_for_real(ls, _dir)
    print "Scanned " + str(readings)
    #match, _dir = prb.recognize_location(signatures, _dir)
    match = signatures.read(index)
    angle = prb.findAnomaly(readings, match)  # anomaly in absolute angle (degrees)
    toturn = angle - current_particles[2]
    turn.turn(math.degrees(toturn))
    particles = [pu.updateRotation(particles[i], math.degrees(toturn)) for i in range(numberOfParticles)]

    ob = gostraight.go()
    dist = 0
    ob.run(1)
    dist += 1
    ob.run(-dist)

    nwp.navigateToWayPoint(waypoint1[0], waypoint1[1], pu.getCurrentPosition(particles), particles)




    # waypointofobject = getLocationOfObject(pu.getCurrentPosition(particles), angle)
    # nwp.navigateToWayPoint(waypointofobject[0], waypointofobject[1], pu.getCurrentPosition(particles), particles)
    # when hit a bump, break

nwp.navigateToWayPoint(waypoint1[0], waypoint1[1], pu.getCurrentPosition(particles), particles)

# at each waypoint do a scan
# go to new location with detected object
# bump
# go to next waypoint
# repeat till last object is bumped
# go back to waypoint 1
