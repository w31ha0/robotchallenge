import place_rec_bits as prb
import os

index = 0
step = 5

signatures = prb.SignatureContainer()
s = [0] * (255/step)
filename = signatures.filenames[index]
if os.path.isfile(filename):
    f = open(filename, 'r')
    for line in f:
        linex = line[1:-2]
        print "line is " + str(linex)
        currenttuple = tuple(map(float, linex.split(',')))
        currentAngle = currenttuple[0]
        currentDistance = currenttuple[1]
        for idx, freq in enumerate(s):
            #print "Comparing current Distance " + str(currentDistance) + " against " + str(step*(idx+1))
            if (step*(idx+1) > currentDistance):
                print str(currentDistance) + " has been allocated to " + str(idx+1)
                s[idx] = freq+1
                break
    f.close()
    print str(s)
else:
    print "WARNING: Signature does not exist."
