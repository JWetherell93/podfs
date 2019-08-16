import numpy as np
import os
from os import listdir
from os.path import isfile, join
import sys

from .dataTypes import VECTOR, TIMESTEP
from .utilities import isFloat

def readDigitalFilterData(patch, path):

    U = VECTOR('U')

    prfFiles = [f for f in listdir(path) if (isfile(join(path, f)) and f[-4:]=='.prf')]

    timeFiles = [f[:-4] for f in prfFiles if isFloat(f[:-4])]

    timeFiles.sort(key=float)

    timeValues = np.array(timeFiles, dtype=np.float64)

    for i in range(0, len(timeValues)):

        filename = path + timeFiles[i] + ".prf"

        points, timeData = readPRF(filename)

        U.addTimestep( TIMESTEP(timeFiles[i], timeData, points) )

    patch.addVector(U)

def readPRF(filename):

    with open(filename, 'r') as f:
        data = f.readlines()

    for i in range(0, len(data)):
        if data[i].split(',')[0] == 'data':
            i += 1
            break

    data = data[i:]

    for i in range(0, len(data)):
        data[i] = data[i].split(',')

    data = np.array(data, dtype=np.float64)

    points = data[:,:3]
    U = data[:,3:]

    return points, U
