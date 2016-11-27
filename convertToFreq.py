import place_rec_bits as prb
import os

index = 2
step = 10

signatures = prb.SignatureContainer()
s = [0] * (200/step)
filename = signatures.filenames[index]
if os.path.isfile(filename):
    f = open(filename, 'r')
    for line in f:
        linex = line[1:-2]
        #print "line is " + str(linex)
        currenttuple = tuple(map(float, linex.split(',')))
        currentAngle = currenttuple[0]
        currentDistance = currenttuple[1]
        for idx, freq in enumerate(s):
            #print "Comparing current Distance " + str(currentDistance) + " against " + str(step*(idx+1))
            if (step*(idx+1) > currentDistance):
                #print str(currentDistance) + " has been allocated to " + str(idx+1)
                s[idx] = freq+1
                break
    f.close()
    print str(s)
    filename = 'freqHistogram_{0:02d}.dat'.format(index)
    if os.path.isfile(filename):
        os.remove(filename)
    f = open(filename, 'w')
    for i in range(len(s)):
        string = str(s[i])+'\n'
        f.write(string)
    f.close()       
else:
    print "WARNING: Signature does not exist."
