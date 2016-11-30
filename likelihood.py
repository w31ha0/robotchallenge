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

def calculate_likelihood_2(x, y, theta, z):
    m = 1000
    for index, wall in enumerate(walls):
        distanceToWall = getDistanceToWall_2(wall[0][0], wall[0][1], wall[1][0], wall[1][1], x, y, theta)
        if distanceToWall is not None:
            if (distanceToWall < m): #Find the closest wall
                m = distanceToWall
    if m>255:
        m=255 # In order to compare it with the measure value
    likelihood = getLikelihoodProb(z, m)
    return likelihood

def calculate_likelihood_bottle(x,y,theta,z):
    m = 1000
    for index, wall in enumerate(walls):
        distanceToWall = getDistanceToWall_2(wall[0][0], wall[0][1], wall[1][0], wall[1][1], x, y, theta)
        if distanceToWall is not None:
            if (distanceToWall < m): #Find the closest wall
                m = distanceToWall
    if m>255:
        m=255 # In order to compare it with the measure value
    likelihood = getBottleLikelihoodProb(z, m)
    return likelihood

def getDistanceToWall_2(Ax,Ay,Bx,By,x,y,theta):
    radians = math.radians(theta)    
    if Ax==Bx: #Means it's a vertical line
        if ((-90<=theta<=90 or 270<=theta<=360 or -360<=theta<=-270) and (Ax>=x)) or ((90<=theta<=270 or -270<=theta<=-90) and (Ax<=x)): #Check the wall is in front of the robot        
            if theta == 90 or theta == 270 or theta == -90 or theta==-270 : #If vertical, there won't be any intersection
                return None #Return None
            else:#If there will be a intersection                        
                intersection_y = math.tan(radians)*Ax+(y-math.tan(radians)*x)
                if min(Ay,By)<=intersection_y<=max(Ay,By): #Means the intersection is on the line
                     return math.hypot(Ax - x,intersection_y-y) # This is the distance
                else: #Intersection is not on line segment
                    return None
        else:#The wall is at back of the robot
            return None
    
    if Ay==By:#Means it's a horizontal line
        if ((0<=theta<=180 or -360<=theta<=-180) and (Ay>=y)) or ((180<=theta<=360 or -180<=theta<=0) and (Ay<=y)):
            if theta==0 or theta==180 or theta==-180 or theta==360 or theta==-360:
                return None
            else:
                intersection_x = (Ay-y+math.tan(radians)*x)/math.tan(radians)
                if min(Ax,Bx)<=intersection_x<=max(Ax,Bx):
                    return math.hypot(intersection_x-x,Ay-y)
                else:
                    return None
        else:
            return None
        
        
def getBottleLikelihoodProb(z,m): 
    sd  =20.0
    #print 'z:',z
    #print 'm:',m
    
    if z>m:
     #   print 'prob:',0.01
        return 0.01
    elif (m-z)<10:
        return 0.01
    else:
      #  print 'prob:',math.exp(  ((z - m) * (z - m)) / (2 * sd * sd))
        return math.exp(((z - m) * (z - m)) / (2 * sd * sd))


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
   