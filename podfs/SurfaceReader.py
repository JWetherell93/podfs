import numpy as np
import os
from os import listdir
from os.path import isfile, join, isdir
from utilities import removeChars, cleanDir, writeFile, writeVectorFile
import errno

class vectorField:

    def __init__(self, name, surfaceName, path, times):

        self.name = name
        self.path = path
        self.surfaceName = surfaceName
        self.times = times

        self.component1 = list()
        self.component2 = list()
        self.component3 = list()

        self.x = list()
        self.y = list()
        self.z = list()

        self.writeFile = writeFile

    def readField(self):

        print( "READING VARIABLE: " + self.name )

        for i in range( 0, len(self.times) ):

            time = self.times[i]

            print( "Time = " + time + "s" )

            fullFileName = self.path + time + "/" + self.name + "_" + self.surfaceName

            coords, varData = self.readAsciiVTK(fullFileName)

            self.x.append( coords[:,0] )
            self.y.append( coords[:,1] )
            self.z.append( coords[:,2] )

            self.component1.append( varData[:,0] )
            self.component2.append( varData[:,1] )
            self.component3.append( varData[:,2] )

        print()

    def readSurfaceVTK(self, file, binary):

        if binary:

            coords, varData = self.readBinaryVTK(file)

        else:

            coords, varData = self.readAsciiVTK(file)

        return coords, varData

    def readAsciiVTK(self, file):

        with open(file+".vtk", "r") as f:
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

    def createWriteDir(self, writePath):

        folderName = writePath + "/" + self.name

        if os.path.exists(folderName):
            cleanDir(folderName)

        else:
            os.makedirs(folderName)

    def write(self, writePath):

        self.createWriteDir(writePath)

        print( "WRITING VARIABLE: " + self.name )

        for i in range(0, np.shape(self.component1)[0]):

            fullName = writePath + "/" + self.name + "/" + '{:.6F}'.format(float(self.times[i]))

            components = np.array(np.zeros( [len(self.component1[i]),3] ))

            components[:,0] = self.component1[i]
            components[:,1] = self.component2[i]
            components[:,2] = self.component3[i]

            writeVectorFile(fullName, components )

class scalarField:

    def __init__(self, name, surfaceName, path, times):

        self.name = name
        self.path = path
        self.surfaceName = surfaceName
        self.times = times

        self.field = list()

        self.x = list()
        self.y = list()
        self.z = list()

        self.writeFile = writeFile

    def readField(self):

        print( "READING VARIABLE: " + self.name )

        for i in range( 0, len(self.times) ):

            time = self.times[i]

            print( "Time = " + time + "s" )

            fullFileName = self.path + time + "/" + self.name + "_" + self.surfaceName

            coords, varData = self.readAsciiVTK(fullFileName)

            self.x.append( coords[:,0] )
            self.y.append( coords[:,1] )
            self.z.append( coords[:,2] )

            self.field.append( varData )

        print()

    def readSurfaceVTK(self, file, binary):

        if binary:

            coords, varData = self.readBinaryVTK(file)

        else:

            coords, varData = self.readAsciiVTK(file)

        return coords, varData

    def readAsciiVTK(self, file):

        with open(file+".vtk", "r") as f:
            data = f.readlines()

        nPoints = int(data[4].split()[1])

        coords = data[5:nPoints+5]

        for i in range(0,nPoints):

            coords[i] = coords[i].split()

        coords = np.array(coords, "float64")

        offset = int(data[nPoints+6].split()[1])

        varData = data[nPoints+offset+10:]

        for i in range(1, len(varData)):

            varData[0] += varData[i]

        varData = varData[0].split()

        varData = np.array(varData, "float64")

        return coords, varData

    def createWriteDir(self, writePath):

        folderName = writePath + "/" + self.name

        if os.path.exists(folderName):
            cleanDir(folderName)

        else:
            os.makedirs(folderName)

    def write(self, writePath):

        self.createWriteDir(writePath)

        print( "WRITING VARIABLE: " + self.name )

        for i in range(0, len(self.field)):

            fullName = writePath + "/" + self.name + "/" + '{:.6F}'.format(float(self.times[i]))

            writeFile(fullName, self.field[i])

class RawData:

    def __init__(self, dir, surfaceName, vars):

        self.surfaceName = surfaceName

        self.readSurfaceData(dir, surfaceName, vars)

    def readSurfaceData(self, dir, surfaceName, vars):

        self.variables = list()

        self.times = [f for f in listdir(dir) if isdir(join(dir, f))]

        for i in range(0, len(vars)):

            if vars[i] in ["U"]:

                self.variables.append( vectorField( vars[i], surfaceName, dir, self.times ) )

                self.variables[i].readField()

            else:

                self.variables.append( scalarField( vars[i], surfaceName, dir, self.times ) )

                self.variables[i].readField()

    def write(self, writeDir):

        for i in range(0, len(self.variables)):

            self.variables[i].write(writeDir + "/" + self.surfaceName)

        print( "WRITING COORDINATES" )
        writeFile(writeDir + "/" + self.surfaceName + "/" + "x", self.variables[0].x[0])
        writeFile(writeDir + "/" + self.surfaceName + "/" + "y", self.variables[0].y[0])
        writeFile(writeDir + "/" + self.surfaceName + "/" + "z", self.variables[0].z[0])
