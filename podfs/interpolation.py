import numpy as np
from scipy.interpolate import griddata

def interpolateMode(spatialMode, origPoints, filename):

    with open(filename, "r") as pointsFile:
        pointData = pointsFile.readlines()

    for i in range(0, len(pointData)):
        pointData[i] = pointData.split()

    points = np.array(pointData)

    newMode = griddata(origPoints, spatialMode, points, method='linear')

    return newMode
