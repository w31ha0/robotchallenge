import math

pt_o = (0, 0)
pt_a = (0, 168)
pt_b = (84, 168)
pt_c = (84, 126)
pt_d = (84, 210)
pt_e = (168, 210)
pt_f = (168, 84)
pt_g = (210, 84)
pt_h = (210, 0)

wall_a = (pt_o, pt_a)
wall_b = (pt_a, pt_b)
wall_c = (pt_b, pt_c)
wall_d = (pt_d, pt_e)
wall_e = (pt_e, pt_f)
wall_f = (pt_f, pt_g)
wall_g = (pt_g, pt_h)
wall_h = (pt_h, pt_o)

walls = [wall_a, wall_b, wall_c, wall_d, wall_e, wall_f, wall_g, wall_h]


def calculate_likelihood(x, y, theta, z):
    m = 0
    prevDeviation = 1000
    for index, wall in enumerate(walls):
        distanceToWall = getDistanceToWall(wall[0][0], wall[0][1], wall[1][0], wall[1][1], x, y, theta)
        deviation = abs(distanceToWall - z)
        if (deviation < prevDeviation):
            m = abs(distanceToWall)
    # print "m is " + str(m)
    # print "z is " + str(z)
    likelihood = getLikelihoodProb(z, m)
    # print "likehood is " + str(likelihood)
    return likelihood


def getDistanceToWall(Ax, Ay, Bx, By, x, y, theta):
    theta_radians = math.radians(theta)
    beta = math.acos(
        (math.cos(theta_radians) * (Ay - By) + math.sin(theta_radians) * (Bx - Ax)) / math.hypot(Ay - By, Bx - Ax))
    if (beta > math.radians(45)):
        return 1000
    else:
        return ((By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)) / (
        (By - Ay) * math.cos(math.radians(theta)) - (Bx - Ax) * math.sin(math.radians(theta)))


def getLikelihoodProb(z, m):
    sd = 3.0
    return math.exp((-(z - m) * (z - m)) / 2 * sd * sd)
   