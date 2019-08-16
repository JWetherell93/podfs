import numpy as np
import sys
import os

from .utilities import cleanDir, writeFoamHeader

def write_OpenFOAM(OUTPUT, writeDir):

    makeFolderTree(OUTPUT, writeDir)

    nPoints = len(OUTPUT.coords[:,0])

    writeVectorSpatialMode(writeDir, "points", OUTPUT.coords, nPoints, False)

    for i in range(0, len(OUTPUT.vars)):

        var = OUTPUT.vars[i]

        varDir = writeDir + var.name + '/'

        if var.type == 'scalar':
            writeScalarSpatialMode(varDir, "meanField", var.meanField, nPoints, True)
        else:
            writeVectorSpatialMode(varDir, "meanField", var.meanField, nPoints, True)

        for j in range(0, len(var.modes)):

            modeDir = varDir + "mode" + '{0:04d}'.format(j) + "/"

            if var.type == 'scalar':
                writeScalarSpatialMode(modeDir, "spatialMode", var.modes[j].spatialMode, nPoints, True)
            else:
                writeVectorSpatialMode(modeDir, "spatialMode", var.modes[j].spatialMode, nPoints, True)

            #print(var.modes[j].NF)
            writeVectorSpatialMode(modeDir, "fourierCoeffs", var.modes[j].b_ij, var.modes[j].NF, False)


def makeFolderTree(OUTPUT, writeDir):

    for i in range(0, len(OUTPUT.vars)):

        folderName = writeDir + OUTPUT.vars[i].name

        if os.path.exists(folderName):
            cleanDir(folderName)

        else:
            os.makedirs(folderName)

        for j in range(0, len(OUTPUT.vars[i].modes)):

             modeFolder = folderName + "/" + "mode" + '{0:04d}'.format(j)

             os.makedirs(modeFolder)

def writeScalarSpatialMode(modeDir, filename, data, nPoints, header):

    with open(modeDir + filename, "w") as spatialFile:

        if header:
            writeFoamHeader(spatialFile, "scalarField")
            spatialFile.write("\n")

        spatialFile.write(str(nPoints))

        spatialFile.write("(")

        for i in range(0, nPoints):

            spatialFile.write('{:F}\n'.format(data[i]))

        spatialFile.write(")")

def writeVectorSpatialMode(modeDir, filename, data, nPoints, header):

    with open(modeDir + filename, "w") as spatialFile:

        if header:
            writeFoamHeader(spatialFile, "vectorField")
            spatialFile.write("\n")

        spatialFile.write(str(nPoints) + "\n")

        spatialFile.write("(\n")

        for i in range(0, nPoints):

            spatialFile.write('({:F} '.format(data[i, 0]))
            spatialFile.write('{:F} '.format(data[i,1]))
            spatialFile.write('{:F})\n'.format(data[i,2]))

        spatialFile.write(")")
