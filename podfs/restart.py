import numpy as np
import os
from os import listdir
from os.path import isfile, isdir, join

from .dataTypes import PATCH, SCALAR, VECTOR, TIMESTEP
from .constants import vectors
from .utilities import printProgressBar

def reloadData(writeDir, patchName):

    patches = [f for f in listdir(writeDir) if isdir(join(writeDir, f))]

    if patches == []:
        sys.exit("No folders found in specified location, please double check")
    if patchName not in patches:
        sys.exit("Requested patch " + patchName + " not found in specified location, please double check")

    Patch = PATCH(patchName)

    patchDir = writeDir + patchName

    vars = listdir(patchDir)

    if vars[i] in vectors:

        print('Reading variable ' + vars[i])

        tempVar = VECTOR(vars[i])

        varDir = patchDir + "/" + vars[i]

        times = [f for f in listdir(varDir) if isdir(join(varDir, f))]

        for j in range(0, len(times)):

            timeDir = varDir + "/" + times[j]

            points, data = readTime(timeDir)

            tempVar.addTimestep( TIMESTEP(times[j], data, points) )

            printProgressBar(j, len(times)-1)

        Patch.addVector( tempVar )

    else:

        print('Reading variable ' + vars[i])

        tempVar = SCALAR(vars[i])

        varDir = patchDir + "/" + vars[i]

        times = [f for f in listdir(varDir) if isdir(join(varDir, f))]

        for j in range(0, len(times)):

            timeDir = varDir + "/" + times[j]

            points, data = readTime(timeDir)

            tempVar.addTimestep( TIMESTEP(times[j], data, points) )

            printProgressBar(j,len(times)-1)

        Patch.addScalar( tempVar )

    return Patch

def readTime(timeDir):

    pointsFile = timeDir + "/points"
    dataFile = timeDir + "/data"

    with open(pointsFile, "r") as f:
        points = f.readlines()

    with open(dataFile, "r") as f:
        data = f.readlines()

    for i in range(0, len(data)):

        points[i] = points[i].split()
        data[i] = data[i].split()

    points = np.array(points, np.float64)
    data = np.array(data, np.float64)

    return points, data
