from place_rec_bits import *
from config import *
import math
import sonic
import particleDataStructure as pds

waypoint1 = (84, 30)
waypoint2 = (180, 30)
waypoint3 = (180, 54)
waypoint4 = (138, 54)
waypoint5 = (138, 168)

waypoints = [waypoint1, waypoint2, waypoint3, waypoint4, waypoint5]

signatures = SignatureContainer(5)
signatures.delete_loc_files()