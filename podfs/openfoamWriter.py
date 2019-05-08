import os
from utilities import cleanDir, writeFoamHeader
import numpy as np

def writeOF(Input, Modes, writeDir, args):

    makeFolderTree(writeDir, Modes, Input, args)

    startRow = 0

    for i in range(0, len(Input.scalars)):

        var = Input.scalars[i]

        startRow = startRow + Input.nPoints * i

        varDir = writeDir + "/" + var + "/"

        writeScalarSpatialMode(startRow, varDir, "meanField", Modes.meanField[:,0],  Input.nPoints)

        for j in range(0, len(Modes.modes)):

            modeDir = writeDir + "/" + var + "/mode" + '{0:04d}'.format(j) + "/"

            writeScalarSpatialMode(startRow, modeDir, "spatialMode", Modes.modes[j].spatialMode, Input.nPoints)

            writeVectorSpatialMode(0, modeDir, "fourierCoeffs", np.reshape(Modes.modes[j].b_ij, [-1,1])[:,0], Modes.modes[j].NF)

    if len(Input.scalars) > 0:
        startRow = startRow + Input.nPoints

    for i in range(0, len(Input.vectors)):

        var = Input.vectors[i]

        startRow = startRow + Input.nPoints * i * 3

        varDir = writeDir + "/" + var + "/"

        writeVectorSpatialMode(startRow, varDir, "meanField", Modes.meanField[:,0],  Input.nPoints)

        for j in range(0, len(Modes.modes)):

            modeDir = writeDir + "/" + var + "/mode" + '{0:04d}'.format(j) + "/"

            writeVectorSpatialMode(startRow, modeDir, "spatialMode", Modes.modes[j].spatialMode, Input.nPoints)

            writeVectorSpatialMode(0, modeDir, "fourierCoeffs", np.reshape(Modes.modes[j].b_ij, [-1,1])[:,0], Modes.modes[j].NF)

    if len(Input.vectors) > 0:
        startRow = startRow + Input.nPoints * 3

def makeFolderTree(writeDir, Modes, Input, args):

    for i in range(0, len(Input.vars)):

        folderName = writeDir + "/" + Input.vars[i].name

        if os.path.exists(folderName):
            cleanDir(folderName)

        else:
            os.makedirs(folderName)

        for j in range(0, len(Modes.modes)):

             modeFolder = folderName + "/" + "mode" + '{0:04d}'.format(j)

             os.makedirs(modeFolder)

def writeScalarSpatialMode(startRow, modeDir, filename, data, nPoints):

    with open(modeDir + filename, "w") as spatialFile:

        writeFoamHeader(spatialFile, "scalarField")

        spatialFile.write("\n")

        spatialFile.write(str(nPoints))

        spatialFile.write("(")

        for i in range(startRow, startRow+nPoints):

            spatialFile.write('{:F}\n'.format(data[i]))

        spatialFile.write(")")

def writeVectorSpatialMode(startRow, modeDir, filename, data, nPoints):

    with open(modeDir + filename, "w") as spatialFile:

        writeFoamHeader(spatialFile, "vectorFieldField")

        spatialFile.write("\n")

        spatialFile.write(str(nPoints) + "\n")

        spatialFile.write("(\n")

        for i in range(startRow, startRow+nPoints):

            spatialFile.write('({:F} '.format(data[i]))
            spatialFile.write('{:F} '.format(data[i+nPoints]))
            spatialFile.write('{:F})\n'.format(data[i+nPoints+nPoints]))

        spatialFile.write(")")
