import numpy as np
import os
from os import listdir
from os.path import isfile, join, isdir
import errno

from .dataTypes import SCALAR, VECTOR, TIMESTEP
from .utilities import removeChars, cleanDir, writeFile, writeVectorFile, printProgressBar

def readOpenFOAMVTK(case, vars, path):

    times = [f for f in listdir(path) if isdir(join(path, f))]

    times.sort(key=float)

    vectors = ['U']

    for i in range(0, len(vars) ):

        print('Reading variable ' + vars[i])

        if vars[i] in vectors:
            tempVar = VECTOR(vars[i])

        else:
            tempVar = SCALAR(vars[i])

        fileName = vars[i] + "_" + case.patchName + ".vtk"

        for j in range(0, len(times) ):

            fullFile = path + times[j] + "/" + fileName

            points, varData = readAsciiVTK(fullFile)

            tempVar.addTimestep( TIMESTEP(times[j], varData, points) )

            printProgressBar(j, len(times)-1)

        if vars[i] in vectors:
            case.addVector(tempVar)

        else:
            case.addScalar(tempVar)

def readAsciiVTK(file):

    with open(file, "r") as f:
        data = f.readlines()

    nPoints = int(data[4].split()[1])

    coords = data[5:nPoints+5]

    for i in range(0,nPoints):

        coords[i] = coords[i].split()

    coords = np.array(coords, "float64")

    offset = int(data[nPoints+6].split()[1])

    varData = data[nPoints+offset+10:]

    for i in range(0, nPoints):

        varData[i] = varData[i].split()

    varData = np.array(varData, "float64")

    return coords, varData
