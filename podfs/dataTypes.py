import numpy as np
import os

from .utilities import removeDir, removeFile, cleanDir, printProgressBar

class PATCH:

    def __init__(self, patch):

        self.scalars = list()
        self.vectors = list()
        self.patchName = patch

    def addPoints(self, points):

        self.points = points

    def addScalar(self, scalar):

        self.scalars.append(scalar)

    def addVector(self, vector):

        self.vectors.append(vector)

    def createPODMatrix(self):

        NS = len( self.vectors[0].times )
        nVars = len(self.scalars) + len(self.vectors)
        nPoints = len( self.points )

        if len(self.scalars) > 0:
            A = self.scalars[0].createVariableMatrix()

            for i in range(1, len(self.scalars) ):
                A = np.append(A, self.scalars[i].createVariableMatrix(), axis=0)

            for i in range(0, len(self.vectors) ):
                A = np.append(A, self.vectors[i].createVariableMatrix(), axis=0)
        else:
            A = self.vectors[0].createVariableMatrix()

            for i in range(1, len(self.vectors) ):
                A = np.append(A, self.vectors[i].createVariableMatrix(), axis=0)

        return A

    def write(self, writeDir):

        folderName = writeDir + self.patchName

        if os.path.exists(folderName):
            cleanDir(folderName)

        else:
            os.makedirs(folderName)

        pointsFile = folderName + "/" + "points"

        with open(pointsFile, "w+") as file:

            for i in range(0, len(self.points)):

                file.write( '{:F} '.format( self.points[i,0] ) )
                file.write( '{:F} '.format( self.points[i,1] ) )
                file.write( '{:F}\n'.format( self.points[i,2] ) )

        for i in range(0, len(self.scalars)):
            self.scalars[i].write(folderName)

        for i in range(0, len(self.vectors)):
            self.vectors[i].write(folderName)

class SCALAR:

    def __init__(self, name):

        self.times = list()
        self.name = name

    def __getitem__(self, index):

        return self.times[index]

    def addTimestep(self, timestep):

        self.times.append(timestep)

    def createVariableMatrix(self):

        self.nPoints = len( self.times[0].field )
        NS = len(self.times)

        a = np.array(np.zeros( [self.nPoints, NS] ))

        for i in range(0, NS):

            a[:,i] = self.times[i].field

        return a

    def write(self, writeDir):

        folderName = writeDir + "/" + self.name

        os.makedirs(folderName)

        print('Writing variable: ' + self.name)

        for i in range(0, len(self.times)):
            self.times[i].write(folderName)
            printProgressBar(i, len(self.times)-1)

class VECTOR:

    def __init__(self, name):

        self.times = list()
        self.name = name

    def __getitem__(self, index):

        return self.times[index]

    def addTimestep(self, timestep):

        self.times.append(timestep)

    def createVariableMatrix(self):

        self.nPoints = len( self.times[0].field )
        NS = len(self.times)

        a1 = np.array(np.zeros( [self.nPoints, NS] ))
        a2 = np.array(np.zeros( [self.nPoints, NS] ))
        a3 = np.array(np.zeros( [self.nPoints, NS] ))

        for i in range(0, NS):
            a1[:,i] = self.times[i].field[:,0]
            a2[:,i] = self.times[i].field[:,1]
            a3[:,i] = self.times[i].field[:,2]

        a = np.append(a1, a2, axis=0)
        a = np.append(a, a3, axis=0)

        return a

    def write(self, writeDir):

        folderName = writeDir + "/" + self.name

        os.makedirs(folderName)

        print('Writing variable: ' + self.name)

        for i in range(0, len(self.times)):
            self.times[i].write(folderName)
            printProgressBar(i, len(self.times)-1)

class TIMESTEP:

    def __init__(self, time, field):

        self.time = time
        self.field = field

    def __getitem__(self, index):

        return self.field[index]

    def __len__(self):

        return len(self.field)

    def write(self, writeDir):

        timeDir = writeDir + "/" + self.time

        os.makedirs(timeDir)



        dataFile = timeDir + "/" + "data"

        with open(dataFile, "w+") as file:

            if len(self.field.shape) > 1:
                if self.field.shape[1] > 1:

                    for i in range(0, len(self.field)):

                        file.write( '{:F} '.format( self.field[i,0] ) )
                        file.write( '{:F} '.format( self.field[i,1] ) )
                        file.write( '{:F}\n'.format( self.field[i,2] ) )

            else:

                for i in range(0, len(self.field)):

                    file.write( '{:F}\n'.format( self.field[i] ) )
