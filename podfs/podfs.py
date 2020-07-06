import os
import textwrap

from .programInputs import getParser, checkInputs, printStuff
from .dataTypes import PATCH
from .OpenFOAMVTK import readOpenFOAMVTK
from .nickDigitalFilter import readPreCalcDFData
from .restart import reloadData
from .preProcessing import cutData
from .PODFSStruct import PODFS
from .transformations import transform
from .OFWriter import write_OpenFOAM
from .checkPODFSOutput import checkOutput
from .alphaCalcs import calculateAlpha
from .interpolation import interpolateModes
from .utilities import cleanDir

def main():

    parser = getParser()

    inputs = parser.parse_args()

    if inputs.help:
        printStuff()
        print(parser.description)
        return

    checkInputs(inputs)

    for i in range(0, len(inputs.surfaces)):

        print('------------------------')
        print('    SURFACE: ' + inputs.surfaces[i])
        print('------------------------ \n')

        print('READING DATA... ')

        if inputs.format == 'OpenFOAMVTK':
            patch = PATCH(inputs.surfaces[i])
            readOpenFOAMVTK(patch, inputs.vars, inputs.path)

        elif inputs.format == 'PreCalcDF':
            patch = PATCH('inlet')
            readPreCalcDFData( patch, inputs.path )

        elif inputs.format == 'resume':
            patch = reloadData(inputs.path, inputs.surfaces[i])

        if inputs.saveRawData:
            print('\n SAVING DATA...')
            patch.write(inputs.saveDir)

        print('\nPRE-PROCESSING...')

        if inputs.cutData:
            cutData(patch, inputs)

        print('\nRUNNING PODFS ANALYSIS...')

        A = patch.createPODMatrix()

        podfs = PODFS(A, A.shape[1], inputs)
        podfs.run()

        output = podfs.createOutput(patch)

        print('\nTRANSFORMING POINTS...')

        if inputs.transformPoints:

            transform(output, inputs)

        print('\nWRITING DATA...')

        if inputs.writeFormat == "OpenFOAM":

            patchWriteDir = inputs.writeDir + patch.patchName + "/"

            if os.path.exists(patchWriteDir):
                cleanDir(patchWriteDir)

            else:
                os.makedirs(patchWriteDir)

            write_OpenFOAM(output, patchWriteDir, patch, podfs)

        if inputs.checkOutput:

            print('\nCHECKING OUTPUT...')

            checkOutput(output, inputs.nickDir)

        print('\nCALCULATING ALPHA...')

        calculateAlpha(output, patch, inputs)

        if inputs.interpolateModes:

            print ('\nINTERPOLATING MODES...')

            interpolateModes(output, inputs)

    print('\nANALYSIS COMPLETED\n')
