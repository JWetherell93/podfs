import numpy as np
import os

from .dataTypes import PATCH, SCALAR, VECTOR, TIMESTEP
from .constants import vectors

def reloadData(writeDir):

    patches = [f for f in listdir(writeDir) if isdir(join(writeDir, f))]

    Patches = list()

    if patches == []:
        sys.exit("No folders found in specified location, please double check")

    for i in range(0, len(patches)):

        Patches.append( PATCH(patches[i]) )

        patchDir = writeDir + "/" + patches[i]

        vars = listdir(patchDir)

        if vars[i] in vectors:

            tempVar = VECTOR(vars[i])

            varDir = patchDir + "/" + vars[i]

            times = [f for f in listdir(varDir) if isdir(join(varDir, f))]

            for j in range(0, len(times)):

                timeDir = varDir + "/" + times[j]

                points, data = readTime(timeDir)

                tempVar.addTimestep( TIMESTEP(times[j], data, points) )

            Patches.addVector( tempVar )

        else:

            tempVar = SCALAR(vars[i])

            varDir = patchDir + "/" + vars[i]

            times = [f for f in listdir(varDir) if isdir(join(varDir, f))]

            for j in range(0, len(times)):

                timeDir = varDir + "/" + times[j]

                points, data = readTime(timeDir)

                tempVar.addTimestep( TIMESTEP(times[j], data, points) )

            Patches.addScalar( tempVar )

    return Patches

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
    data = np.array(data. np.float64)

    return points, data
