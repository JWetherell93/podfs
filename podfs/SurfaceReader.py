import numpy as np
import os
from os import listdir
from os.path import isfile, join, isdir
from utilities import removeChars, cleanDir
import errno

def writeFile(fullName, data):

    with open(fullName, "w+") as f:

        for i in range(0, len(data)):

            f.write('{:F}\n'.format(data[i]))

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

        print "READING VARIABLE: " + self.name

        for i in range( 0, len(self.times) ):

            time = self.times[i]

            print "Time = " + time + "s"

            fullFileName = self.path + time + "/" + self.name + "_" + self.surfaceName

            coords, varData = self.readAsciiVTK(fullFileName)

            self.x.append( coords[:,0] )
            self.y.append( coords[:,1] )
            self.z.append( coords[:,2] )

            self.component1.append( varData[:,0] )
            self.component2.append( varData[:,1] )
            self.component3.append( varData[:,2] )

        print "                             "

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

        for i in ["x", "y", "z"]:

            folderName = writePath + "/" + self.name + i

            if os.path.exists(folderName):
                cleanDir(folderName)

            else:
                os.makedirs(folderName)

    def write(self, writePath):

        self.createWriteDir(writePath)

        print "WRITING VARIABLE: " + self.name

        for i in range(0, len(self.component1)):

            fullName1 = writePath + "/" + self.name + "x" + "/" + '{:.6F}'.format(float(self.times[i]))
            fullName2 = writePath + "/" + self.name + "y" + "/" + '{:.6F}'.format(float(self.times[i]))
            fullName3 = writePath + "/" + self.name + "z" + "/" + '{:.6F}'.format(float(self.times[i]))

            self.writeFile(fullName1, self.component1[i])
            self.writeFile(fullName2, self.component2[i])
            self.writeFile(fullName3, self.component3[i])

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

        print "READING VARIABLE: " + self.name

        for i in range( 0, len(self.times) ):

            time = self.times[i]

            print "Time = " + time + "s"

            fullFileName = self.path + time + "/" + self.name + "_" + self.surfaceName

            coords, varData = self.readAsciiVTK(fullFileName)

            self.x.append( coords[:,0] )
            self.y.append( coords[:,1] )
            self.z.append( coords[:,2] )

            self.field.append( varData )

        print "                             "

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

        print "WRITING VARIABLE: " + self.name

        for i in range(0, len(self.field)):

            fullName = writePath + "/" + self.name + "/" + '{:.6F}'.format(float(self.times[i]))

            self.writeFile(fullName, self.field[i])

class RawData:

    def __init__(self, dir, surfaceName, vars):

        self.readSurfaceData(dir, surfaceName, vars)

        self.writeFile = writeFile

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

            self.variables[i].write(writeDir)

        print "WRITING COORDINATES"
        self.writeFile(writeDir + "/" + "x", self.variables[0].x[0])
        self.writeFile(writeDir + "/" + "y", self.variables[0].y[0])
        self.writeFile(writeDir + "/" + "z", self.variables[0].z[0])
