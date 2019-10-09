import numpy as np
from scipy.interpolate import griddata
from .utilities import printProgressBar

def interpolateModes(output, inputs):

    for v in range(0, len(output.vars)):

        var = output.vars[v]

        print('Interpolating modes for variable: ' + var.name)

        for n in range(0, len(var.modes)):

            var.modes[n].spatialMode = interpolateMode(var.modes[n].spatialMode, output.coords, inputs.newPointsFile)

            printProgressBar(n, len(var.modes)-1)

        var.meanField = interpolateMode(var.meanField, output.coords, inputs.newPointsFile)

    with open(inputs.newPointsFile, "r") as pointsFile:
        pointData = pointsFile.readlines()

    for i in range(0, len(pointData)):
        pointData[i] = pointData.split()

    points = np.array(pointData)

    output.coords = points

def interpolateMode(spatialMode, origPoints, filename):

    with open(filename, "r") as pointsFile:
        pointData = pointsFile.readlines()

    for i in range(0, len(pointData)):
        pointData[i] = pointData.split()

    points = np.array(pointData)

    newMode = griddata(origPoints, spatialMode, points, method='linear')

    return newMode
