import numpy as np
import os
from os import listdir
from os.path import isfile, join, isdir
import errno

from .dataTypes import SCALAR, VECTOR, TIMESTEP
from .utilities import removeChars, cleanDir, writeFile, writeVectorFile, printProgressBar
from .constants import vectors

def readOpenFOAMVTK(patch, vars, path):

    times = [f for f in listdir(path) if isdir(join(path, f))]

    times.sort(key=float)

    for i in range(0, len(vars) ):

        print('Reading variable ' + vars[i])

        if vars[i] in vectors:
            tempVar = VECTOR(vars[i])

        else:
            tempVar = SCALAR(vars[i])

        fileName = vars[i] + "_" + patch.patchName + ".vtk"

        for j in range(0, len(times) ):

            fullFile = path + times[j] + "/" + fileName

            if i == 0 and j == 0:

                points, varData = readAsciiVTK(fullFile, True)

                patch.addPoints(points)

            else:

                varData = readAsciiVTK(fullFile, False)

            tempVar.addTimestep( TIMESTEP(times[j], varData) )

            printProgressBar(j, len(times)-1)

        if vars[i] in vectors:
            patch.addVector(tempVar)

        else:
            patch.addScalar(tempVar)

def readAsciiVTK(file, readPoints):

    with open(file, "r") as f:
        data = f.readlines()

    nPoints = int(data[4].split()[1])

    if readPoints:

        coords = data[5:nPoints+5]

        for i in range(0,nPoints):

            coords[i] = coords[i].split()

        coords = np.array(coords, "float64")

    offset = int(data[nPoints+6].split()[1])

    varData = data[nPoints+offset+10:]

    for i in range(0, nPoints):

        varData[i] = varData[i].split()

    varData = np.array(varData, "float64")

    if readPoints:

        return coords, varData

    else:

        return varData
