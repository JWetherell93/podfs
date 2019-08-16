import argparse
from argparse import ArgumentParser
import sys
import numpy as np
import os

from .PODFSStruct import PODFS
from .restart import reloadData
from .OFWriter import write_OpenFOAM
from .podfs_functions import MyArgumentParser
from .podfs_functions import addArguments
from .OpenFOAMVTK import readOpenFOAMVTK
from .dataTypes import PATCH
from .nickDigitalFilter import readDigitalFilterData
from .utilities import cleanDir
from .checkPODFSOutput import checkOutput 

def main():

    parser = MyArgumentParser(
                            prog = 'podfs',
                            usage = '%(prog)s [options]',
                            description = 'Script for PODFS data compression, including pre-processor options',
                            fromfile_prefix_chars = '@',
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            add_help=False,
                            )

    addArguments(parser)

    inputs = parser.parse_args()

    readFormats = ['OpenFOAMVTK', 'DigitalFilter', 'resume']
    writeFormats = ['OpenFOAM']

    if inputs.format == 'null':
        sys.exit('format not specified, please specify a format for the input data')
    elif inputs.format not in readFormats:
        sys.exit('\"' + inputs.format + '\" is not a supported format, please specify a recognised input format')

    patches = list()

    if inputs.format == 'OpenFOAMVTK':

        for i in range(0, len(inputs.surfaces)):

            patches.append( PATCH(inputs.surfaces[i]) )

            readOpenFOAMVTK(patches[i], inputs.vars, inputs.path)

    elif inputs.format == 'DigitalFilter':

        patches.append( PATCH('inlet') )

        readDigitalFilterData( patches[0], inputs.path )

    elif inputs.format == 'resume':

        patches = reloadData(inputs.path)

    A = list()

    for i in range(0, len(patches)):
        A.append(patches[i].createPODMatrix())

    podfs = list()

    for i in range(0, len(A)):
        podfs.append( PODFS(A[i], A[i].shape[1], inputs.NM, inputs.dt, inputs.ET) )
        podfs[i].run()

    outputs = list()

    for i in range(0, len(podfs)):
        outputs.append(podfs[i].createOutput(patches[i]))

    if inputs.writeFormat == "OpenFOAM":

        for i in range(0, len(patches)):

            patchWriteDir = inputs.writeDir + patches[i].patchName + "/"

            if os.path.exists(patchWriteDir):
                cleanDir(patchWriteDir)

            else:
                os.makedirs(patchWriteDir)

            write_OpenFOAM(outputs[i], patchWriteDir)

    if inputs.checkOutput:
        checkOutput(outputs[i], inputs.nickDir)
