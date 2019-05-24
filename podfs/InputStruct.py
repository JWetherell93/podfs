import numpy as np
import os
from os import listdir
from os.path import isfile, join
import sys

class Coordinates:

    def __init__(self, path, type):
        self.path = path
        self.type = type

    def readCoords(self):

        if self.type == "cartesian":
            with open(self.path + "x", "r") as f:
                x = f.readlines()
                self.x = np.array(x, "float64")

            with open(self.path + "y", "r") as f:
                y = f.readlines()
                self.y = np.array(y, "float64")

            with open(self.path + "z", "r") as f:
                z = f.readlines()
                self.z = np.array(z, "float64")

        elif self.type == "cylindrical":
            with open(self.path + "x", "r") as f:
                x = f.readlines()
                self.x = np.array(x, "float64")

            with open(self.path + "r", "r") as f:
                r = f.readlines()
                self.y = np.array(r, "float64")

            with open(self.path + "theta", "r") as f:
                theta = f.readlines()
                self.z = np.array(theta, "float64")

class Scalar:

    def __init__(self, name, path):
        self.name = name
        self.path = path + name

        self.getListOfTimes()

    def getListOfTimes(self):

        self.times = [f for f in listdir(self.path) if isfile(join(self.path, f))]

    def readTimesteps(self, nPoints):

        self.timeStepData = list()

        for i in range(len(self.times)):

            self.timeStepData.append(self.readTimestep(self.path, self.times[i], nPoints))

    def readTimestep(self, path, time, nPoints):

        with open(path + "/" + time, "r") as f:
            data = f.readlines()

        data = np.array(data, "float64")

        if not len(data) == nPoints:
            print( "Error reading timestep data for variable \"" + path + "\", for timestep \"" + self.name + "\"" )
            print( "Number of points in file does not match number of coordinate points" )
            print( "Please double check file in question" )
            sys.exit()

        return data

    def createVariableMatrix(self):

        nPoints = len(self.timeStepData[0])
        nTimeSteps = len(self.times)

        a = np.array(np.zeros([nPoints, nTimeSteps]))

        for i in range(nTimeSteps):

            a[:,i] = self.timeStepData[i]

        return a

class Vector:

    def __init__(self, name, path):
        self.name = name
        self.path = path + name

        self.getListOfTimes()

    def getListOfTimes(self):

        self.times = [f for f in listdir(self.path) if isfile(join(self.path, f))]

    def readTimesteps(self, nPoints):

        self.timeStepData = list()

        for i in range(len(self.times)):

            self.timeStepData.append(self.readTimestep(self.path, self.times[i], nPoints))

    def readTimestep(self, path, time, nPoints):

        with open(path + "/" + time, "r") as f:
            data = f.readlines()

        temp = np.array(np.zeros([len(data), 3], "float64"))

        for i in range(0, len(data)):

            temp[i,:] = data[i].split()

        if not len(data) == nPoints:
            print( "Error reading timestep data for variable \"" + path + "\", for timestep \"" + self.name + "\"" )
            print( "Number of points in file does not match number of coordinate points" )
            print( "Please double check file in question" )
            sys.exit()

        return temp

    def createVariableMatrix(self):

        nPoints = len(self.timeStepData[0])
        nTimeSteps = len(self.times)

        a = np.array(np.zeros([nPoints*3, nTimeSteps]))

        for i in range(nTimeSteps):

            a[:,i] = np.reshape(self.timeStepData[i], (1,-1), order='F')

        return a

class Timestep:

    def __init__(self, path, name, nPoints):
        self.name = name

        self.readData(path)

        if not len(self.field) == nPoints:
            print( "Error reading timestep data for variable \"" + path + "\", for timestep \"" + self.name + "\"" )
            print( "Number of points in file does not match number of coordinate points" )
            print( "Please double check file in question" )
            sys.exit()

    def readData(self, path):

        with open(path + "/" + self.name, "r") as f:
            data = f.readlines()

        self.field = np.array(data, "float64")

class InputData:

    def __init__(self, dataDir, scalars, vectors, coordType):

        self.scalars = scalars
        self.vectors = vectors

        self.checkVarsExist(dataDir, coordType)

        self.constructVars(dataDir, coordType)

        self.checkConsistentTimes()

        continueFlag = input("Construction and error checking complete. Based on any error messages, do you wish to continue? y or n \n")

        while continueFlag != "y" and continueFlag != "n":
            print( "Please enter either y or n." )
            continueFlag = raw_input("Do you wish to continue? \n")

        if continueFlag == "n":
            sys.exit()

        self.readCoordinateData()

        self.readTimesteps()

    def checkVarsExist(self, dataDir, coordType):

        if coordType == "cartesian":
            for j in ["x", "y", "z"]:

                if not os.path.isfile(dataDir + j):
                    print( "Could not find file for coordinate " + j + ". Exiting..." )
                    sys.exit()

        elif coordType == "cylindrical":
            for j in ["x", "r", "theta"]:

                if not os.path.isfile(dataDir + j):
                    print( "Could not find file for coordinate " + j + ". Exiting..." )
                    sys.exit()

        else:
            print( "Unrecognised coordinate system \"" + coordType + "\". Exiting..." )
            sys.exit()

        if len(self.scalars) > 0:

            for i in range(len(self.scalars)):

                if not self.checkForVar(self.scalars[i], dataDir):
                    self.scalars.pop[i]
                    print( "Could not find directory for scalar " + self.scalars[i] + ". Skipping this variable." )

        if len(self.vectors) > 0:

            for i in range(len(self.vectors)):

                if not self.checkForVar(self.vectors[i], dataDir):
                    self.scalars.pop(i)
                    print( "Could not find directory for vector " + self.vectors[i] + ". Skipping this variable." )

    def checkForVar(self, var, dataDir):

        if os.path.isdir(dataDir + var):
            return True
        else:
            return False

    def constructVars(self, dataDir, coordType):

        self.coordinates = Coordinates(dataDir, coordType)

        self.vars = list()

        for i in range(len(self.scalars)):

            self.vars.append(Scalar(self.scalars[i], dataDir))

        for i in range(len(self.vectors)):

            self.vars.append(Vector(self.vectors[i], dataDir))

    def checkConsistentTimes(self):

        differences = list()

        for i in range(1,len(self.vars)):

            differences.append([x for x in self.vars[0].times if x not in self.vars[i].times])

        for diff in differences:

            if len(diff) > 0:

                print( "Inconsistent time files between variables. Please double check contents of each variable directory." )

    def readCoordinateData(self):

        self.coordinates.readCoords()

        self.nPoints = len(self.coordinates.x)

    def readTimesteps(self):

        for i in range(len(self.vars)):

            self.vars[i].readTimesteps(self.nPoints)

    def createPODMatrix(self):

        nTimeSteps = len(self.vars[0].times)
        nVars = len(self.scalars) + len(self.vectors)
        nPoints = self.nPoints

        A = self.vars[0].createVariableMatrix()

        for i in range(1,nVars):

            A = np.append(A, self.vars[i].createVariableMatrix(), axis=0)

        return A
