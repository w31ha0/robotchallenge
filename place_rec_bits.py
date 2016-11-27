#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import sonic
import os
import math
import numpy as np


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
            if os.path.isfile(self.filenames[n]) is False:
                break
            n += 1

        if n >= self.size:
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
        s = []
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for line in f:
                linex = line[1:-2]
                s.append(tuple(map(float, linex.split(','))))
            ls.sig = s
            f.close()
        else:
            print "WARNING: Signature does not exist."

        return ls


# FILL IN: spin robot or sonar to capture a signature and store it in ls
def characterize_location(ls, _dir):
    sn = sonic.Sonic()
    _dir *= -1
    readings, _dir = sn.rotateSonar(math.pi * 2, _dir)
    ls.sig[0:len(readings)] = readings
    print ls.sig
    return _dir


def characterize_location_for_real(ls, _dir):
    sn = sonic.Sonic()
    _dir *= -1
    readings, _dir = sn.rotateSonar(math.pi * 2, _dir)
    return _dir, readings


# FILL IN: compare two signatures
def compare_signatures(ls1, ls2):
    dist = 0
    # TODO:    You should implement the function that compares two signatures
    for i in range(len(ls1.sig)):
        diff = abs(ls1.sig[i] - ls2.sig[i])
        dist += diff

    return dist


def getSavedDistance(currentAngle, match):
    if (len(match.sig)) >= 2:
        for i in range(len(match.sig)):
            if match.sig[i][0] >= currentAngle:
                return match.sig[i][1], match.sig[i + 1:len(match.sig)]
    else:
        return False, False


def findAnomaly(readings, match):
    threshold = 10
    differingIndices = []

    if len(match.sig) > len(readings):
        lengthX = len(readings)
    else:
        lengthX = len(match.sig)
    for i in range(lengthX - 1):
        tmp_match = match
        oldDistance = []
        currentAngle = int(readings[i][0])
        currentDistance = readings[i][1]
        for theta in [0]:
            # for theta in [4,0,-4]:
            oldDistance.append(getSavedDistance(currentAngle - theta, tmp_match)[0])
            if getSavedDistance(currentAngle - theta, match)[1] is False:
                pass
            else:
                pass
                # match.sig = getSavedDistance(currentAngle-theta, match)[1]
        difference = min([old - currentDistance for old in oldDistance])
        if difference > threshold:
            differingIndices.append((currentAngle, difference))
    print "Anomalies: " + str(differingIndices)

    filteredIndices = []
    tmp = []
    for index, item in enumerate(differingIndices):
        if abs(item[0] - differingIndices[index - 1][0]) <= 8.0:
            tmp.append(((item[0] + differingIndices[index - 1][0]) / 2.0, differingIndices[index - 1][1]))
        else:
            if tmp != []:
                filteredIndices.append((np.median([pair[0] for pair in tmp]), sum([pair[1] for pair in tmp])))
                tmp = []
    if tmp != []:
        filteredIndices.append((np.median([pair[0] for pair in tmp]), sum([pair[1] for pair in tmp])))
        tmp = []
    tmp2 = [error[1] for error in filteredIndices]

    print filteredIndices[tmp2.index(max(tmp2))][0]
    return filteredIndices[tmp2.index(max(tmp2))][0]


def getLocationOfObject(currentPosition, distance):
    currentOrientation = math.radians(currentPosition[2])
    dx = distance * math.cos(currentOrientation)
    dy = distance * math.sin(currentOrientation)
    return currentPosition[0] + dx, currentPosition[1] + dy


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


# This function characterizes the current location, and stores the obtained
# signature into the next available file.
'''
def learn_location(signatures, _dir):
    ls = LocationSignature()
    _dir = characterize_location(ls, _dir)
    idx = signatures.get_free_index()
    if idx == -1:  # run out of signature files
        print "\nWARNING:"
        print "No signature file is available. NOTHING NEW will be learned and stored."
        print "Please remove some loc_%%.dat files.\n"
        return _dir, readings

    signatures.save(ls, idx)
    print "STATUS:  Location " + str(idx) + " learned and saved."
    return _dir

def recognize_location(signatures, _dir):
    ls_obs = LocationSignature()
    _dir = characterize_location(ls_obs, _dir)
    currentBestMatch = LocationSignature()
    matchedIndex = 0

    # FILL IN: COMPARE ls_read with ls_obs and find the best match
    for idx in range(signatures.size):
        prevDist = 10000
        print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
        ls_read = signatures.read(idx)

        dist = compare_signatures(ls_obs, ls_read)
    if dist < prevDist:
        currentBestMatch = ls_read
        matchedIndex = idx
    print "Found matched index " + str(matchedIndex) + " for file " + str(signatures.filenames[matchedIndex])
    return currentBestMatch, _dir

def drawSun(canvas, values, origin):
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
'''
