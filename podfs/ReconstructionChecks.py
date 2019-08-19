import numpy as np
import sys
import os
from os import listdir
from os.path import isfile, isdir, join

from .dataTypes import PATCH, VECTOR, SCALAR, TIMESTEP

def checkReconstruction(outputs, patches, inputs):



def reconstructPatch(OUTPUT, patch, inputs):

    times = list()

    if len(patch.scalars) > 0:
        for i in range(0, len(patch.scalars[0].times)):
            times.append(patch.scalars[0].times[i].time)
    else:
        for i in range(0, len(patch.vectors[0].times)):
            times.append(patch.vectors[0].times[i].time)

    period = times[-1] + ( times[1] - times[0] )



def reconstructTimestep(meanField, modes, time, period):

    fluctuating = 0

    for i in range(0, len(modes)):
        for j in range(0, mode.NF):
            exponent = complex(0,2*pi*mode.b_ij[i,0]*time/period)
            temporalMode += complex(b_ij[i,1], b_ij[i,2]) * exponent

        fluctuating += mode.spatialMode * abs(temporalMode)

    reconstructedTimestep = meanField + fluctuating

    return reconstructedTimestep
