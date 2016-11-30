import particleUpdate as pu
import place_rec_bits as prb
from config import numberOfParticles, initialPosition
import navigateToWayPoint as nwp
import turn
import gostraight
import sonic

waypoint1 = (84, 30, 0)
waypointa = (157.5, 30, 0)
waypointab = (126, 30, 1)
waypointb = (126, 120, 0)
waypointbc = (126, 112, 1)
waypointc = (42, 80, 0)
waypointcd = (142, 80, 0)
waypointd = (42, 180, 0)
waypointde = (142, 80, 0)
waypointe = (42, 180, 0)
waypointef = (142, 80, 0)
waypointf = (42, 80, 0)

#waypoints = [waypointa, waypointab, waypointb, waypointbc, waypointc]
waypoints = [waypointa, waypointab, waypointb, waypointbc, waypointc, waypointcd, waypointd, waypointde, waypointe, waypointef, waypointf]

# canvas = pds.Canvas()
# mymap = pds.Map()
# pds.drawWall(mymap, canvas)

particles = [initialPosition for i in range(numberOfParticles)]
# canvas.drawParticles(particles)
signatures = prb.SignatureContainer()

# bumper = bumper.Bumper()
# bumperThread = threading.Thread(name='bumper', target=bumper.getTouch)
# bumperThread.start()

_sonnic = sonic.Sonic()
_gostraight = gostraight.go()

_dir = 1


def ConvertToHisto(readings):
    step = 10

    s = [0] * (200 / step)
    for currenttuple in readings:
        currentAngle = currenttuple[0]
        currentDistance = currenttuple[1]
        for idx, freq in enumerate(s):
            # print "Comparing current Distance " + str(currentDistance) + " against " + str(step*(idx+1))
            if (step * (idx + 1) > currentDistance):
                # print str(currentDistance) + " has been allocated to " + str(idx+1)
                s[idx] = freq + 1
                break

    return s


for index, waypoint in enumerate(waypoints):
    print "main 6666 curr position" + str(pu.getCurrentPosition(particles))
    particles,bumped = nwp.navigateToWayPoint(waypoint[0], waypoint[1], pu.getCurrentPosition(particles), particles)
    if bumped:
        continue
    if waypoint[2] is 0:
        #if index is 0:
            #nwp.wallCheck(_gostraight, _sonnic, _dir)
        # include bumped here, then subsequent action
        current_particles = pu.getCurrentPosition(particles)
        # ls = prb.LocationSignature()
        _dir, readings = prb.characterize_location_for_real(_sonnic, _dir)
        #print "Scanned " + str(readings)
        scannedHisto = ConvertToHisto(readings)
        #print "Got histo " + str(scannedHisto)
        # match, _dir = prb.recognize_location(signatures, _dir)
        match = signatures.read(index)
        histo_match = signatures.read_histogram(index)
        angle = prb.findAnomaly(readings, match)#, histo_match, scannedHisto)  # anomaly in absolute angle (degrees)
        #print 'Anomalous angle is at dsfsdfsdf: ', angle
        #print 'particlesTurnning is ', current_particles[2]
        toturn = angle - current_particles[2]
        turn.turn(-toturn)
        particles = [pu.updateRotation(particles[i], toturn) for i in range(numberOfParticles)]

        ob = gostraight.go()
        distance, angle = ob.run(80)
        particles = [pu.updateRotation(particles[i], angle) for i in range(numberOfParticles)]
        particles = [pu.update(particles[i], distance) for i in range(numberOfParticles)]

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
