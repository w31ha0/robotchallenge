#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import os
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


# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self, no_bins=360):
        self.sig = [0] * no_bins

    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]


# --------------------- File management class ---------------
class SignatureContainer():
    def __init__(self, size=5):
        self.size = size  # max number of signatures that can be stored
        self.filenames = []

        # Fills the filenames variable with names like loc_%%.dat
        # where %% are 2 digits (00, 01, 02...) indicating the location number.
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are
    # used, it returns -1
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1

        if (n >= self.size):
            return -1
        else:
            return n

    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print "STATUS:  All signature files removed."
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])

    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)

        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close()

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(s)
            f.close()
        else:
            print "WARNING: Signature does not exist."

        return ls


def rotateSonar(angleRad):
    interface.increaseMotorAngleReference(motors[2], angleRad)
    while not interface.motorAngleReferenceReached(motors[2]):
        time.sleep(0.1)


# FILL IN: spin robot or sonar to capture a signature and store it in ls
def characterize_location(ls):
    dir = 1
    print "TODO:    You should implement the function that captures a signature."

    fs = open("directionCheck", 'r+')
    x = fs.read()
    fs.close()
    fw = open("directionCheck", 'w+')
    print "hahaha " + x
    if x == "1":
        dir = 1
        fw.write("-1")
    elif x == "-1":
        dir = -1
        fw.write("1")
    fw.close()

    for i in range(len(ls.sig)):
        ls.sig[i] = sonic.getSonar() + sonarToCenter
        rotateSonar(dir * 1.0 / 180 * math.pi)
        # print ls.sig[i]


# FILL IN: compare two signatures
def compare_signatures(ls1, ls2):
    dist = 0
    print "TODO:    You should implement the function that compares two signatures."
    for i in range(len(ls1.sig)):
        diff = abs(ls1.sig[i] - ls2.sig[i])
        dist += diff

    return dist


# This function characterizes the current location, and stores the obtained
# signature into the next available file.
def learn_location():
    ls = LocationSignature()
    characterize_location(ls)
    idx = signatures.get_free_index()
    if idx == -1:  # run out of signature files
        print "\nWARNING:"
        print "No signature file is available. NOTHING NEW will be learned and stored."
        print "Please remove some loc_%%.dat files.\n"
        return

    signatures.save(ls, idx)
    print "STATUS:  Location " + str(idx) + " learned and saved."


# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen
def recognize_location():
    ls_obs = LocationSignature()
    characterize_location(ls_obs)
    currentBestMatch = LocationSignature()
    matchedIndex = 0

    # FILL IN: COMPARE ls_read with ls_obs and find the best match
    for idx in range(signatures.size):
        prevDist = 10000000000
        print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
        ls_read = signatures.read(idx)
        dist = compare_signaturesForFrequencyHistogram(ls_obs, ls_read)
        print "distance for signature " + str(idx) + " is " + str(dist)
    if dist < prevDist:
        currentBestMatch = ls_read
        matchedIndex = idx
    print "Found match " + str(matchedIndex) + " in file " + str(signatures.filenames[matchedIndex])
    return currentBestMatch


def compare_signaturesForFrequencyHistogram(ls1, ls2):
    dist = 0
    histogram1 = getDepthFrequencyHistogram(ls1.sig)
    histogram2 = getDepthFrequencyHistogram(ls2.sig)
    for i in range(len(histogram1)):
        dist += abs(histogram1[i] - histogram2[i])
    return dist


def getDepthFrequencyHistogram(arrayOfDepths):
    step = 5
    sizeOfHistogram = 260 / 5
    histogram = [0] * sizeOfHistogram
    for depth in arrayOfDepths:
        index = int(depth / step) - 1
        # print "index is " + str(index) + " while depth is " + str(depth)
        histogram[index] += 1
    return histogram


def drawSun(values, origin):
    i = 0
    for eachangle in range(len(values)):
        deviation = 360 / len(values)
        angle = deviation * i
        z = values[i]
        y1 = z * math.sin(math.radians(angle))
        x1 = z * math.cos(math.radians(angle))
        y1 = int(y1)
        x1 = int(x1)
        line = [origin[0], origin[1], x1 + origin[0], -y1 + origin[1]]
        line = tuple(line)
        # print str(line)
        canvas.drawLine(line)
        del line
        i += 1


canvas = pds.Canvas()
mymap = pds.Map()
pds.drawWall(mymap, canvas)

waypoint = 0
origin = [waypoints[waypoint][0], waypoints[waypoint][1]]

# Prior to starting learning the locations, it should delete files from previous
# learning either manually or by calling signatures.delete_loc_files().
# Then, either learn a location, until all the locations are learned, or try to
# recognize one of them, if locations have already been learned.

signatures = SignatureContainer(5)
# signatures.delete_loc_files()

# learn_location()
# drawSun(signatures.read(waypoint).sig, origin)

recognize_location()
