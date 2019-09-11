import numpy as np
import sys
import os
from os import listdir
from os.path import isfile, isdir, join
from math import pi
import matplotlib.pyplot as plt

from .constants import vectors
from .dataTypes import PATCH, VECTOR, SCALAR, TIMESTEP

def calculateAlpha(outputs, patches, inputs):

    reconPatches = list()

    for i in range(0, len(patches)):

        A = outputs[i].coords[0,:]
        B = outputs[i].coords[1,:]
        C = outputs[i].coords[-1,:]

        AB = B - A
        AC = C - A

        n = np.cross(AB, AC)

        nhat = np.divide(n, np.sqrt(sum(k**2 for k in n)))

        reconPatches.append( reconstructPatch(outputs[i], patches[i], inputs) )

        for k in range(0, len(patches[i].vectors)):

            if patches[i].vectors[k].name == 'U':
                U_orig = patches[i].vectors[k]
                U_recon = reconPatches[i].vectors[k]
                break

        Umean_orig = 0
        Umean_recon = 0

        for t in range(0, len(U_orig.times)):

            Um_orig = 0
            Um_recon = 0

            for j in range(0, len(U_orig.times[t])):

                Um_orig += np.dot( U_orig.times[t][j,:], nhat )
                Um_recon += np.dot( U_recon.times[t][j,:], nhat )

            Umean_orig += (Um_orig / (j+1))
            Umean_recon += (Um_recon / (j+1))

        Umean_orig /= (t+1)
        Umean_recon /= (t+1)

        Udiff = Umean_orig - Umean_recon

        for j in range(0, len(outputs[i].vars)):
            if outputs[i].vars[j].name == 'U':
                meanField = outputs[i].vars[j].meanField
                break

        umean = 0

        for k in range(0, len(meanField)):

            umean += np.dot( meanField[k,:], nhat )

        umean /= (k+1)

        alpha = 1 + Udiff/umean

        print(alpha)

        outputs[i].vars[j].addAlpha(alpha)

        if inputs.checkReconstruction:

            for j in range(0, len(patches[i].vectors)):

                vector = patches[i].vectors[j]

                totalDiff = 0

                for k in range(0, len(vector.times)):

                    origTime = vector.times[k]
                    newTime = reconPatches[i].vectors[j].times[k]

                    diff = np.array(np.zeros(np.shape(origTime.field)))

                    for ii in range(0, len(origTime)):
                        diff[ii,:] = origTime[ii,:] - newTime[ii,:]

                    meanDiff = np.mean(abs(diff), axis=0)

                    totalDiff += meanDiff

                totalDiff /= (k+1)

                print(totalDiff)

            fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, num=1, clear=True)

            cntr1 = ax1.tricontourf(origTime.points[:,2], origTime.points[:,1], origTime.field[:,0])
            cntr2 = ax2.tricontourf(origTime.points[:,2], origTime.points[:,1], outputs[i].vars[0].meanField[:,0])
            cntr3 = ax3.tricontourf(newTime.points[:,2], newTime.points[:,1], newTime.field[:,0])

            cbar1 = fig.colorbar(cntr1, ax=ax1)
            cbar2 = fig.colorbar(cntr2, ax=ax2)
            cbar3 = fig.colorbar(cntr3, ax=ax3)

            plt.show()

def reconstructPatch(OUTPUT, patch, inputs):

    reconstructed = PATCH(patch.patchName)

    times = list()

    if len(patch.scalars) > 0:
        for i in range(0, len(patch.scalars[0].times)):
            times.append(patch.scalars[0].times[i].time)
    else:
        for i in range(0, len(patch.vectors[0].times)):
            times.append(patch.vectors[0].times[i].time)

    period = float(times[-1]) #+ ( float(times[1]) - float(times[0]) )

    for i in range(0, len(inputs.vars)):

        if inputs.vars[i] not in vectors:
            tempVar = SCALAR(inputs.vars[i])
        else:
            tempVar = VECTOR(inputs.vars[i])

        for t in range(0, len(times)):

            time = float(times[t])

            tempVar.addTimestep( TIMESTEP(time, reconstructTimestep(OUTPUT.vars[i].meanField, OUTPUT.vars[i].modes, time, period, OUTPUT.vars[i].alpha), OUTPUT.coords) )

        if inputs.vars[i] not in vectors:
            reconstructed.addScalar(tempVar)
        else:
            reconstructed.addVector(tempVar)

    return reconstructed

def reconstructTimestep(meanField, modes, time, period, alpha):

    fluctuating = 0

    for i in range(0, len(modes)):
        temporalMode = complex(0,0)
        for j in range(0, modes[i].NF):
            exponent = complex(0,2*pi*modes[i].b_ij[j,0]*time/period)
            temporalMode += complex(modes[i].b_ij[j,1], modes[i].b_ij[j,2]) * np.exp(exponent)

        fluctuating += modes[i].spatialMode * abs(temporalMode)#.real

    reconstructedTimestep = meanField + fluctuating

    return reconstructedTimestep
