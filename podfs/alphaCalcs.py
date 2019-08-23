import numpy as np
import sys
import os
from os import listdir
from os.path import isfile, isdir, join

from .ReconstructionChecks import reconstructPatch
from .constants import vectors

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
