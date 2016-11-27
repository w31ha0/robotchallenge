import particleUpdate as pu
import place_rec_bits as prb
from config import numberOfParticles, initialPosition
import navigateToWayPoint as nwp
import turn as turn
import gostraight
import sonic

lengthOfPi = 10

waypoint1 = (84, 30, 0)
waypointa = (157.5, 30, 0)
waypointab = (126, 30, 1)
waypointb = (126, 120, 0)
waypointbc = (126, 112, 1)
waypointc = (42, 80, 0)

waypoints = [waypointa, waypointab, waypointb, waypointbc, waypointc]
ob = gostraight.go()
dir = 1
row = 1
noOfRows = 4
halfDistance = 100

while (1):
    distance = ob.run(800)
    if (row == noOfRows):
        ob.goback(halfDistance-20)
    turn.turn(90*dir)
    ob.run(lengthOfPi)
    turn.turn(-90*dir)
    ob.run(20)
    turn.turn(180)
    dir*=-1
    row += 1

# at each waypoint do a scan
# go to new location with detected object
# bump
# go to next waypoint
# repeat till last object is bumped
# go back to waypoint 1
