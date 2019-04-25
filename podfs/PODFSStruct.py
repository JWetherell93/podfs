import numpy as np
import numpy.matlib
import sys
import os
import math
from .utilities import writeFile

class Mode:
    def __init__(self,  b_ij, NF, spatialMode, energy ):

        self.b_ij = b_ij
        self.NF = NF
        self.spatialMode = spatialMode
        self.energy = energy

    # def write(self, format, writeDir):



class Modes:
    def __init__(self, spatialModes, cInd, numFcs, c, NM, NF, period, energy, meanField):

        self.modes = list()
        self.period = period
        self.NM = NM
        self.meanField = meanField

        for i in range(0,NM):

            b_ij = np.array(np.zeros([ NF[i], 3 ]))

            for j in range(0, NF[i]):

                b_ij[j,0] = cInd[i,j] - numFcs/2

                b_ij[j,1] = c[ cInd[i,j], i ].real

                b_ij[j,2] = c[ cInd[i,j], i ].imag

            spatialMode = spatialModes[:,i]

            self.modes.append( Mode( b_ij, NF[i], spatialMode, energy[i] ) )

    # def write(self, format, writeDir)
    #
    #     self.writeFormats = ["openfoam"]
    #
    #     if format not in self.writeFormats:
    #
    #         print "Unreconised write format specified. Please select from the following:"
    #
    #         for i in self.writeFormats:
    #             print i
    #
    #         print
    #
    #         sys.exit()
    #
    #     for i in range(0, len(self.modes)):
    #
    #         modeNumber = "mode" + '{0:04d}'.format(i) + "/"
    #
    #         self.modes[i].write("openfoam", writeDir + modeNumber)
    #
    #     writeFile(writeDir + "meanField", self.meanField)



class PODFS:

    def __init__(self, A, nTimesteps, nModes, dt, energyTarget):

        self.A = A
        self.NS = int(nTimesteps)
        self.NM = int(nModes)
        self.dt = dt
        self.ET = energyTarget

    def getFluctuatingComponent(self):

        npnv = int(self.A.shape[0])
        self.meanField = np.array(np.zeros([npnv, 1]))
        self.meanField[:,0] = np.mean(self.A,1)

        self.APrime = self.A - np.matlib.repmat(self.meanField, 1, self.NS)

    def covarianceMatrix(self):

        self.getFluctuatingComponent()

        self.C = np.dot( self.APrime.transpose(), self.APrime ) / self.NS

    def eigenvalues(self):

        self.energy, self.temporalModes = np.linalg.eig(self.C)

    def sortEigenvalues(self):

        energySorted = np.array(np.zeros([self.NS]))
        modeIndex = np.array(np.zeros([self.NS]), "int")
        eV = np.array(np.zeros(self.temporalModes.shape))

        for k in range(0, self.NS):

            modeIndex[k] = k

            if math.isnan(self.energy[k]):
                energySorted[k] = -1e10
                self.temporalModes[:,k] = 0

            else:
                energySorted[k] = self.energy[k].real

        energySorted[0:self.NS], modeIndex[0:self.NS] = zip(*sorted(zip(energySorted[:], modeIndex[:]),reverse=True))

        self.modeIndex = modeIndex

        for i in range(0, self.NS):

            eV[:,i] = self.temporalModes[:,modeIndex[i]]

        self.energy = energySorted
        self.temporalModes = eV

    def findValidModes(self):

        numValidModes = 0

        tol_CN = 1e-15

        cond1 = ( self.energy[numValidModes].real / self.energy[0].real ) > tol_CN**2
        cond2 = ( numValidModes < self.NS-2 )
        cond3 = ( self.energy[numValidModes.real] > 0 )

        while cond1 and cond2 and cond3:

            numValidModes += 1

            cond1 = ( self.energy[numValidModes].real / self.energy[0].real ) > tol_CN**2
            cond2 = ( numValidModes < self.NS-2 )
            cond3 = ( self.energy[numValidModes.real] > 0 )

            if cond1 and cond3:
                numValidModes += 1

            cond1 = ( self.energy[numValidModes].real / self.energy[0].real ) > tol_CN**2
            cond2 = ( numValidModes < self.NS-2 )
            cond3 = ( self.energy[numValidModes.real] > 0 )

        if self.NM < 0 or self.NM > numValidModes:
            self.NM = numValidModes

        self.numValidModes = numValidModes

    def scaleTemporalModes(self):

        for i in range(0, self.numValidModes):

            temporalModeMag = sum( np.multiply(self.temporalModes[:,i].real, self.temporalModes[:,i].real ) ) / self.NS

            self.temporalModes[:,i] = self.temporalModes[:,i] * np.sqrt( self.energy[i].real / temporalModeMag )

    def truncateSpatialModes(self):

        energyTruncInv = np.diag( np.divide( np.ones([self.NM]), self.energy[0:self.NM].real ) )

        spatialModesTrunc = np.dot( self.A[:, 0:self.NS], self.temporalModes[:, 0:self.NM].real )

        spatialModesTrunc = np.dot( spatialModesTrunc, energyTruncInv )

        self.spatialModesTrunc = spatialModesTrunc / self.NS

    def fourierCoeffs(self):

        stride = 1
        numFcs = self.NS
        time= np.linspace(0,(self.NS-1)*self.dt*stride,self.NS)
        period = time[-1] + (time[1] - time[0])

        c = np.array(np.zeros([numFcs, self.NM]), "complex64")
        cInd = np.array(np.zeros([self.NM, numFcs]), "int")
        NF = np.array(np.zeros(self.NM), "int")

        for i in range(0, self.NM):

            y = self.temporalModes[:,i]

            for n in range(0, numFcs):

                k = n - numFcs/2

                ctemp = y * np.exp(-1j * 2 * k * np.pi * time / period)

                c[n,i] = ctemp.sum() / ctemp.size

            cMod = np.abs(c[:,i])

            for j in range (0,numFcs):
        		cInd[i,j]=j

            cMod,cInd[i,:]=zip(*sorted(zip(cMod,cInd[i,:]),reverse=True))

            energy = 0

            energySum = np.sum(np.abs(c[:,i]))

            NF[i] = 0

            while energy < energySum * self.ET:
                energy += np.abs( c[ cInd[ i, NF[i] ], i ] )
                NF[i] += 1

            print "Fourier Coeffs for Mode " + str(i) + ": " + str(NF[i])

        self.cInd = cInd
        self.numFcs = numFcs
        self.c = c
        self.NF = NF
        self.period = period

    def run(self):

        self.covarianceMatrix()
        self.eigenvalues()
        self.sortEigenvalues()
        self.findValidModes()
        self.scaleTemporalModes()
        self.truncateSpatialModes()
        self.fourierCoeffs()

    def outputModes(self):

        modes = Modes(self.spatialModesTrunc, self.cInd, self.numFcs, self.c, self.NM, self.NF, self.period, self.energy, self.meanField)

        return modes
