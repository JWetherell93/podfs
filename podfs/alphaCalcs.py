import numpy as np
import sys
import os
from os import listdir
from os.path import isfile, isdir, join
from math import pi
import matplotlib.pyplot as plt

from .constants import vectors
from .dataTypes import PATCH, VECTOR, SCALAR, TIMESTEP
from .utilities import printProgressBar

def calculateAlpha(output, patch, inputs):

    A = output.coords[0,:]
    B = output.coords[1,:]
    C = output.coords[-1,:]

    AB = B - A
    AC = C - A

    n = np.cross(AB, AC)

    nhat = np.divide(n, np.sqrt(sum(k**2 for k in n)))

    reconPatch = reconstructPatch(output, patch, inputs)

    for k in range(0, len(patch.vectors)):

        if patch.vectors[k].name == 'U':
            U_orig = patch.vectors[k]
            U_recon = reconPatch.vectors[k]
            break

    Umean_orig = 0
    Umean_recon = 0

    print('\nChecking mass flow...')

    for t in range(0, len(U_orig.times)):

        Um_orig = 0
        Um_recon = 0

        for j in range(0, len(U_orig.times[t])):

            Um_orig += np.dot( U_orig.times[t][j,:], nhat )
            Um_recon += np.dot( U_recon.times[t][j,:], nhat )

        Umean_orig += (Um_orig / (j+1))
        Umean_recon += (Um_recon / (j+1))

        printProgressBar(t, len(U_orig.times)-1)

    Umean_orig /= (t+1)
    Umean_recon /= (t+1)

    Udiff = Umean_orig - Umean_recon

    for j in range(0, len(output.vars)):
        if output.vars[j].name == 'U':
            meanField = output.vars[j].meanField
            break

    umean = 0

    for k in range(0, len(meanField)):

        umean += np.dot( meanField[k,:], nhat )

    umean /= (k+1)

    alpha = 1 + Udiff/umean

    print('\nAlpha Value for surface ' + patch.patchName + ': {0:.4f}'.format(alpha))

    output.vars[j].addAlpha(alpha)

    if inputs.checkReconstruction:

        print('\nCHECKING RECONSTRUCTION...')

        for j in range(0, len(patch.vectors)):

            print('Comparing variable: ' + patch.vectors[j].name)

            vector = patch.vectors[j]

            totalDiff = 0

            for k in range(0, len(vector.times)):

                origTime = vector.times[k]
                newTime = reconPatch.vectors[j].times[k]

                diff = np.array(np.zeros(np.shape(origTime.field)))

                for ii in range(0, len(origTime)):
                    diff[ii,:] = origTime[ii,:] - newTime[ii,:]

                meanDiff = np.mean(abs(diff), axis=0)

                totalDiff += meanDiff

                printProgressBar(k, len(vector.times)-1)

            totalDiff /= (k+1)

            # print('\n')
            print('\nAbsolute Difference: {0:.4f}, {1:.4f}, {2:.4f}'.format(totalDiff[0], totalDiff[1], totalDiff[2]))

        # fig, (ax1, ax3) = plt.subplots(nrows=1, ncols=2, num=1, clear=True)
        #
        # cntr1 = ax1.tricontourf(origTime.points[:,2], origTime.points[:,1], origTime.field[:,0])
        # #cntr2 = ax2.tricontourf(origTime.points[:,2], origTime.points[:,1], outputs[i].vars[0].meanField[:,0])
        # cntr3 = ax3.tricontourf(newTime.points[:,2], newTime.points[:,1], newTime.field[:,0])
        #
        # cbar1 = fig.colorbar(cntr1, ax=ax1)
        # #cbar2 = fig.colorbar(cntr2, ax=ax2)
        # cbar3 = fig.colorbar(cntr3, ax=ax3)
        #
        # plt.show()

def reconstructPatch(OUTPUT, patch, inputs):

    reconstructed = PATCH(patch.patchName)

    times = list()
    stride = 1

    if len(patch.scalars) > 0:
        for i in range(0, len(patch.scalars[0].times)):
            times.append(patch.scalars[0].times[i].time)
    else:
        for i in range(0, len(patch.vectors[0].times)):
            times.append(patch.vectors[0].times[i].time)

    times = np.linspace(0,(len(times)-1)*inputs.dt*stride,len(times))

    period = times[-1]+ ( times[1] - times[0] )

    for i in range(0, len(inputs.vars)):

        print('Reconstructing variable: ' + inputs.vars[i])

        if inputs.vars[i] not in vectors:
            tempVar = SCALAR(inputs.vars[i])
        else:
            tempVar = VECTOR(inputs.vars[i])

        for t in range(0, len(times)):

            time = float(times[t])

            tempVar.addTimestep( TIMESTEP(time, reconstructTimestep(OUTPUT.vars[i].meanField, OUTPUT.vars[i].modes, time, period, OUTPUT.vars[i].alpha)) )

            printProgressBar(t, len(times)-1)

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

        fluctuating += modes[i].spatialMode * temporalMode.real

    reconstructedTimestep = meanField + fluctuating

    return reconstructedTimestep

def checkTemporalModes(outputs, patches, inputs, podfs):

    for i in range(0, len(outputs)):

        output = outputs[i]
        patch = patches[i]
        PODFS = podfs[i]

        stride = 1
        numFcs = PODFS.NS
        time= np.linspace(0,(PODFS.NS-1)*PODFS.dt*stride,PODFS.NS)
        period = time[-1] + (time[1] - time[0])

        for var in output.vars:

            for m in range(0, len(var.modes)):

                y = PODFS.temporalModes[:,m]

                temporalMode = np.array(np.zeros(np.shape(time)), complex)

                for t in range(0, len(time)):

                    for j in range(0, var.modes[m].NF):
                        exponent = complex(0,2*pi*var.modes[m].b_ij[j,0]*time[t]/period)
                        temporalMode[t] += complex(var.modes[m].b_ij[j,1], var.modes[m].b_ij[j,2]) * np.exp(exponent)

                plt.plot(time, y)
                plt.plot(time, temporalMode)
                plt.legend(('Original', 'Reconstructed'))
                plt.savefig('temporalModes2/' + '{0:04d}'.format(m) + '_temporalMode.png')
                plt.clf()
