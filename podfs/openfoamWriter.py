import os
from utilities import cleanDir, writeFoamHeader
import numpy as np

def writeOF(InputData, Modes, writeDir, args):

    makeFolderTree(writeDir, Modes, InputData, args)

    coords = np.array([])

    coords = np.append(coords, InputData.coordinates.x, axis=0)
    coords = np.append(coords, InputData.coordinates.y, axis=0)
    coords = np.append(coords, InputData.coordinates.z, axis=0)

    writeVectorSpatialMode(0, writeDir+"/", "points", coords, InputData.nPoints, False)

    startRow = 0

    for i in range(0, len(InputData.scalars)):

        var = InputData.scalars[i]

        startRow = startRow + InputData.nPoints * i

        varDir = writeDir + "/" + var + "/"

        writeScalarSpatialMode(startRow, varDir, "meanField", Modes.meanField[:,0],  InputData.nPoints, True)

        for j in range(0, len(Modes.modes)):

            modeDir = writeDir + "/" + var + "/mode" + '{0:04d}'.format(j) + "/"

            writeScalarSpatialMode(startRow, modeDir, "spatialMode", Modes.modes[j].spatialMode, InputData.nPoints, True)

            fourier = np.array([])

            fourier = np.append(fourier, Modes.modes[j].b_ij[:,0], axis=0)
            fourier = np.append(fourier, Modes.modes[j].b_ij[:,1], axis=0)
            fourier = np.append(fourier, Modes.modes[j].b_ij[:,2], axis=0)

            writeVectorSpatialMode(0, modeDir, "fourierCoeffs", fourier, Modes.modes[j].NF, False)

    if len(InputData.scalars) > 0:
        startRow = startRow + InputData.nPoints

    for i in range(0, len(InputData.vectors)):

        var = InputData.vectors[i]

        startRow = startRow + InputData.nPoints * i * 3

        varDir = writeDir + "/" + var + "/"

        writeVectorSpatialMode(startRow, varDir, "meanField", Modes.meanField[:,0],  InputData.nPoints, True)

        for j in range(0, len(Modes.modes)):

            modeDir = writeDir + "/" + var + "/mode" + '{0:04d}'.format(j) + "/"

            writeVectorSpatialMode(startRow, modeDir, "spatialMode", Modes.modes[j].spatialMode, InputData.nPoints, True)

            fourier = np.array([])

            fourier = np.append(fourier, Modes.modes[j].b_ij[:,0], axis=0)
            fourier = np.append(fourier, Modes.modes[j].b_ij[:,1], axis=0)
            fourier = np.append(fourier, Modes.modes[j].b_ij[:,2], axis=0)

            writeVectorSpatialMode(0, modeDir, "fourierCoeffs", fourier, Modes.modes[j].NF, False)

    if len(InputData.vectors) > 0:
        startRow = startRow + InputData.nPoints * 3

def makeFolderTree(writeDir, Modes, InputData, args):

    for i in range(0, len(InputData.vars)):

        folderName = writeDir + "/" + InputData.vars[i].name

        if os.path.exists(folderName):
            cleanDir(folderName)

        else:
            os.makedirs(folderName)

        for j in range(0, len(Modes.modes)):

             modeFolder = folderName + "/" + "mode" + '{0:04d}'.format(j)

             os.makedirs(modeFolder)

def writeScalarSpatialMode(startRow, modeDir, filename, data, nPoints, header):

    with open(modeDir + filename, "w") as spatialFile:

        if header:
            writeFoamHeader(spatialFile, "scalarField")
            spatialFile.write("\n")

        spatialFile.write(str(nPoints))

        spatialFile.write("(")

        for i in range(startRow, startRow+nPoints):

            spatialFile.write('{:F}\n'.format(data[i]))

        spatialFile.write(")")

def writeVectorSpatialMode(startRow, modeDir, filename, data, nPoints, header):

    with open(modeDir + filename, "w") as spatialFile:

        if header:
            writeFoamHeader(spatialFile, "vectorField")
            spatialFile.write("\n")

        spatialFile.write(str(nPoints) + "\n")

        spatialFile.write("(\n")

        for i in range(startRow, startRow+nPoints):

            spatialFile.write('({:F} '.format(data[i]))
            spatialFile.write('{:F} '.format(data[i+nPoints]))
            spatialFile.write('{:F})\n'.format(data[i+nPoints+nPoints]))

        spatialFile.write(")")
