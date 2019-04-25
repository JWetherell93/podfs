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

class Variable:

    def __init__(self, name, path):
        self.name = name
        self.path = path + name

        self.getListOfTimes()

    def getListOfTimes(self):

        self.timeFiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]

    def readTimesteps(self, nPoints):

        self.timesteps = list()

        for i in range(len(self.timeFiles)):

            self.timesteps.append(Timestep(self.path, self.timeFiles[i], nPoints))

    def createVariableMatrix(self):

        nPoints = len(self.timesteps[0].field)
        nTimeSteps = len(self.timeFiles)

        a = np.array(np.zeros([nPoints, nTimeSteps]))

        for i in range(nTimeSteps):

            a[:,i] = self.timesteps[i].field

        return a

class Timestep:

    def __init__(self, path, name, nPoints):
        self.name = name

        self.readData(path)

        if not len(self.field) == nPoints:
            print "Error reading timestep data for variable \"" + path + "\", for timestep \"" + self.name + "\""
            print "Number of points in file does not match number of coordinate points"
            print "Please double check file in question"
            sys.exit()

    def readData(self, path):

        with open(path + "/" + self.name, "r") as f:
            data = f.readlines()

        self.field = np.array(data, "float64")

class InputData:

    def __init__(self, dataDir, vars, coordType):

        # vars is a list of variables to decompose
        # Currently accepted variables are:
        # Ux, Uy, Uz, p, p_rgh, T, alpha, LS, k, epsilon, omega

        self.initialiseVarList()

        self.setVarsToUse(vars)

        self.checkVarsExist(dataDir, coordType)

        self.constructVars(dataDir, coordType)

        self.checkConsistentTimes()

        continueFlag = raw_input("Construction and error checking complete. Based on any error messages, do you wish to continue? y or n \n")

        while continueFlag != "y" and continueFlag != "n":
            print "Please enter either y or n."
            continueFlag = raw_input("Do you wish to continue? \n")

        if continueFlag == "n":
            sys.exit()

        self.readCoordinateData()

        self.readTimesteps()

    def initialiseVarList(self):

        self.availVars = list()

        self.availVars.append("Ux")
        self.availVars.append("Uy")
        self.availVars.append("Uz")
        self.availVars.append("p")
        self.availVars.append("p_rgh")
        self.availVars.append("T")
        self.availVars.append("alpha")
        self.availVars.append("LS")
        self.availVars.append("k")
        self.availVars.append("epsilon")
        self.availVars.append("omega")

    def setVarsToUse(self,  vars):

        self.useVars = np.array(np.zeros([len(self.availVars)]))

        for i in range(0,len(self.availVars)):

            if self.availVars[i] in vars:
                self.useVars[i] = 1

        unrecognisedVars = [x for x in vars if x not in self.availVars]

        for j in range(len(unrecognisedVars)):
            print "Variable " + unrecognisedVars[j] + " not recognised. Please check for typos or modify source code"

    def checkVarsExist(self, dataDir, coordType):

        if coordType == "cartesian":
            for j in ["x", "y", "z"]:

                if not os.path.isfile(dataDir + j):
                    print "Could not find file for coordinate " + j + ". Exiting..."
                    sys.exit()

        elif coordType == "cylindrical":
            for j in ["x", "r", "theta"]:

                if not os.path.isfile(dataDir + j):
                    print "Could not find file for coordinate " + j + ". Exiting..."
                    sys.exit()

        else:
            print "Unrecognised coordinate system \"" + coordType + "\". Exiting..."
            sys.exit()

        for i in range(len(self.useVars)):

            if self.useVars[i] == 1:

                if not self.checkForVar(self.availVars[i], dataDir):
                    self.useVars[i] = 0
                    print "Could not find directory for variable " + self.availVars[i] + ". Skipping this variable."

    def checkForVar(self, var, dataDir):

        if os.path.isdir(dataDir + var):
            return True
        else:
            return False

    def constructVars(self, dataDir, coordType):

        self.coordinates = Coordinates(dataDir, coordType)

        self.vars = list()

        for i in range(len(self.useVars)):

            if self.useVars[i] == 1:

                self.vars.append(Variable(self.availVars[i], dataDir))

    def checkConsistentTimes(self):

        differences = list()

        for i in range(1,len(self.vars)):

            differences.append([x for x in self.vars[0].timeFiles if x not in self.vars[i].timeFiles])

        for diff in differences:

            if len(diff) > 0:

                print "Inconsistent time files between variables. Please double check contents of each variable directory."

    def readCoordinateData(self):

        self.coordinates.readCoords()

        self.nPoints = len(self.coordinates.x)

    def readTimesteps(self):

        for i in range(len(self.vars)):

            self.vars[i].readTimesteps(self.nPoints)

    def createPODMatrix(self):

        nTimeSteps = len(self.vars[0].timeFiles)
        nVars = int(sum(self.useVars))
        nPoints = self.nPoints

        A = np.array(np.zeros([nPoints * nVars, nTimeSteps]))

        for i in range(nVars):

            A[i*nPoints:i*nPoints+nPoints, :] = self.vars[i].createVariableMatrix()

        return A
