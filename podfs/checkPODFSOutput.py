import numpy as np
import sys
import os
from os import listdir
from os.path import isfile, isdir, join

from .OutputStruct import StandardOutput, Variable, Mode
from .nickDigitalFilter import readPRF

def checkOutput(OUTPUT, nickDir):

    nickOUTPUT = readNickOutput(nickDir)

    error = False

    if len(OUTPUT.vars[0].modes) != len(nickOUTPUT.vars[0].modes):
        print("Number of modes does not match between two methods. Please check input settings")
        error = True

    NM = len(OUTPUT.vars[0].modes)

    for i in range(0, NM):
        if OUTPUT.vars[0].modes[i].NF != nickOUTPUT.vars[0].modes[i].NF:
            print("Number of fourier coefficients for mode " + str(i) + "does not match")
            error = True

    if not compareSpatialModes(OUTPUT.vars[0].meanField, nickOUTPUT.vars[0].meanField):
        print("Mean fields do not match")
        error = True

    for i in range(0, NM):
        if not compareSpatialModes(OUTPUT.vars[0].modes[i].spatialMode, nickOUTPUT.vars[0].modes[i].spatialMode):
            print("Spatial modes for mode " + str(i) + "do not match")
            error = True

        if not compareFourierModes(OUTPUT.vars[0].modes[i], nickOUTPUT.vars[0].modes[i]):
            print("Fourier modes for mode " + str(i) + "do not match")
            error = True

    if not error:
        print("All checks passed succesfully")
    else:
        print("Some checks returned errors, see above output")

def readNickOutput(readDir):

    NickOUTPUT = StandardOutput()

    U = Variable('U', 'vector')

    points, nickMeanField = readPRF(readDir + "PODFS_mean.prf")

    U.addMeanField(nickMeanField)
    NickOUTPUT.addCoordinates(points)

    NM, dt, NF, b_ij = readDATFile(readDir + "PODFS.dat")

    runTot = 0

    for i in range(0, NM):

        b_ij_mode = b_ij[runTot:runTot + NF[i]]

        __, mode = readPRF(readDir + "PODFS_mode_" + '{0:04d}'.format(i+1) + ".prf")

        U.addMode( Mode(b_ij_mode, NF[i], mode, 0) )

        runTot += NF[i]

    NickOUTPUT.addVariable( U )

    return NickOUTPUT

def readDATFile(filename):

    with open(filename, "r") as f:
        data = f.readlines()

    NM = int(data[0])
    dt = float(data[1])

    NF = data[2:2+NM]
    for i in range(0, NM):
        NF[i] = NF[i].split()
        NF[i] = int(NF[i][1])

    b_ij = np.array(np.zeros([ sum(NF), 3 ]), dtype=np.float64)

    temp = data[2+NM:]

    for i in range(0, len(b_ij)):

        temp[i] = temp[i].split()
        b_ij[i,:] = np.array(temp[i], dtype=np.float64)

    return NM, dt, NF, b_ij

def compareSpatialModes(mode1, mode2):

    error = True

    tol = 1e-5

    for i in range(0, len(mode1)):
        if abs(abs(mode1[i,0]) - abs(mode2[i,0])) > tol:
            error = False
        if abs(abs(mode1[i,1]) - abs(mode2[i,1])) > tol:
            error = False
        if abs(abs(mode1[i,2]) - abs(mode2[i,2])) > tol:
            error = False

    # for i in range(0, len(mode1)):
    #     if abs(mode1[i,0] - mode2[i,0]) > tol:
    #         error = False
    #     if abs(mode1[i,1] - mode2[i,1]) > tol:
    #         error = False
    #     if abs(mode1[i,2] - mode2[i,2]) > tol:
    #         error = False

    return error

def compareFourierModes(mode1, mode2):

    error = True

    tol = 1e-5

    for i in range(0, mode1.NF):
        if abs(abs(mode1.b_ij[i,0]) - abs(mode2.b_ij[i,0])) > tol:
            error = False
        if abs(abs(mode1.b_ij[i,1]) - abs(mode2.b_ij[i,1])) > tol:
            error = False
        if abs(abs(mode1.b_ij[i,2]) - abs(mode2.b_ij[i,2])) > tol:
            error = False

    # for i in range(0, mode1.NF):
    #     if abs(mode1.b_ij[i,0] - mode2.b_ij[i,0]) > tol:
    #         error = False
    #     if abs(mode1.b_ij[i,1] - mode2.b_ij[i,1]) > tol:
    #         error = False
    #     if abs(mode1.b_ij[i,2] - mode2.b_ij[i,2]) > tol:
    #         error = False

    return error
