import numpy as np
import sys
import os

class Mode:

    def __init__(self,  b_ij, NF, spatialMode, energy ):

        self.b_ij = b_ij
        self.NF = NF
        self.spatialMode = spatialMode
        self.energy = energy

class Variable:

    def __init__(self, name, type):

        self.modes = list()
        self.name = name
        self.type = type

    def addMode(self, mode):

        self.modes.append(mode)

    def addMeanField(self, meanField):

        self.meanField = meanField

class StandardOutput:

    def __init__(self):

        self.vars = list()

    def addVariable(self, variable):

        self.vars.append(variable)

    def addCoordinates(self, points):

        self.coords = points
