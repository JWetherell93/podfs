import argparse
from argparse import ArgumentParser
import textwrap
from os.path import isfile, join, isdir
import sys

from .version import __version__
from .constants import readFormats, writeFormats

class MyArgumentParser(ArgumentParser):

    def convert_arg_line_to_args(self, arg_line):

        if arg_line == '':
            return []
        elif arg_line[0] == '#':
            return []
        else:
            temp = arg_line.split()
            for i in range(0, len(temp)):
                if temp[i][0] == '#':
                    temp = temp[:i]
                    break
            return temp

def getParser():

    parser = MyArgumentParser(
                            prog = 'podfs',
                            usage = '%(prog)s [options]',
                            description = 'Script for PODFS data compression, including pre-processor options',
                            fromfile_prefix_chars = '@',
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            add_help=False,
                            )

    parser.add_argument('-h', '--help', action='store_true')

    parser.add_argument('--format', type=str, default='null')

    parser.add_argument('--path', type=str, default='null')

    parser.add_argument('--vars', nargs='*', default=[], type=str)

    parser.add_argument('--surfaces', nargs='*', type=str, default=[])

    parser.add_argument('--saveRawData', action='store_true')
    parser.add_argument('--saveDir', type=str)

    parser.add_argument('--cutData', action='store_true')
    parser.add_argument('--xLow', type=float)
    parser.add_argument('--xHigh', type=float)
    parser.add_argument('--yLow', type=float)
    parser.add_argument('--yHigh', type=float)
    parser.add_argument('--zLow', type=float)
    parser.add_argument('--zHigh', type=float)

    parser.add_argument('--EPOD', type=float, default=0.95)
    parser.add_argument('--EFS', type=float, default=0.9)
    parser.add_argument('--nMax', type=int, default=-1)
    parser.add_argument('--dt', type=float, default=-1.0)

    parser.add_argument('--writeDir', type=str)
    parser.add_argument('--writeFormat', type=str)

    parser.add_argument('--checkOutput', action='store_true')
    parser.add_argument('--nickDir', type=str)

    parser.add_argument('--checkReconstruction', action='store_true')

    parser.add_argument('--interpolateModes', action='store_true')
    parser.add_argument('--newPointsFile', type=str)

    parser.add_argument('--transformPoints', action='store_true')
    parser.add_argument('--translation', nargs=3, type=float)
    parser.add_argument('--rotation', nargs=3, type=float)
    parser.add_argument('--mirrorNormal', nargs=3, type=int)
    parser.add_argument('--mirrorCentre', type=float)

    parser.description = textwrap.dedent('''\

            Usage: podfs [options]

            Program for PODFS data compression. Pre-processor options available.

            Arguments can be given by file, using "@" before file name. For example
            "podfs @inputs.txt"

            Required Arguments:
                --format                Format of input data
                --path                  Location of input data
                --vars                  Variables on which to perform analysis
                --surfaces              List of surface names

                --nMax                  Maximum number of spatial modes to use
                --dt                    Timestep of original calculation

            Optional Arguments:
                -h, --help              Show help message and exit

                --saveRawData           Save pre-processed data prior to running analysis
                --saveDir               Directory in which to save pre-processed data

                --cutData               Use a subset of the provided data. Currently only available for planar
                                        input data.
                --xLow                  X-coordinate below which to remove data. Use "yLow" and "zLow" for other
                                        coordinates.
                --xHigh                 X-coordinate above which to remove data. Use "yHigh" and "zHigh" for other
                                        coordinates.

                --EPOD                  Desired energy content for POD modes, default 0.95
                --EFS                   Desired energy content for Fourier series, default 0.9

                --writeFormat           Format to write PODFS output in
                --writeDir              Location to save PODFS output to

                --checkOutput           Compare PODFS output to output from DigitalFiler.py
                --nickDir               Location of digitalfilter.py output

                --checkReconstruction   Compare each reconstructed timestep to the original snapshot and report mean
                                        error

                --interpolateModes      Interpolate calculated spatial modes onto a provided new grid
                --newPointsFile         File containing points to interpolate spatial modes onto

                --transformPoints       Transform the spatial coordinates. Translation, rotation and mirroring
                                        currently supported. At least one must be specified.
                --translation           Vector by which to translate coordinates
                --rotation              Angles by which to rotate coordinates, in degrees. 3 values required. First
                                        value rotation about x axis, second about y and third about z.
                --mirrorNormal          Unit vector specifying direction to mirror in. Currently only cartesian
                                        directions supported.
                --mirrorCentre          Scalar value that locates the plane to mirror points

    ''')

    return parser

def printStuff():

    startString = textwrap.dedent('''\

    *********************************************************************************************************
    *********************************************************************************************************
    **                                   _____   ____  _____  ______ _____                                 **
    **                                  |  __ \ / __ \|  __ \|  ____/ ____|                                **
    **                                  | |__) | |  | | |  | | |__ | (___                                  **
    **                                  |  ___/| |  | | |  | |  __| \___ \                                 **
    **                                  | |    | |__| | |__| | |    ____) |                                **
    **                                  |_|     \____/|_____/|_|   |_____/                                 **
    **                                                                                                     **
    *********************************************************************************************************
    *********************************************************************************************************

    Version: ''' + __version__ + '''
    Author: Jack Wetherell
    ''')

    print(startString)

def checkInputs(inputs):

    printStuff()

    # Check required inputs have been specified
    if inputs.format == 'null':
        print('ERROR:')
        sys.exit('format not specified, please specify a format for the input data \n')
    elif inputs.format not in readFormats:
        print('ERROR:')
        sys.exit('\"' + inputs.format + '\" is not a supported format, please specify a recognised input format \n')

    if not isdir(inputs.path):
        print('ERROR:')
        sys.exit('Path specified for input data not valid, please double check input \n')

    if inputs.vars == []:
        print('ERROR:')
        sys.exit('No variables specified, please give at least one variable to analyse \n')

    if inputs.nMax == -1:
        print('ERROR:')
        sys.exit('Maximum number of modes not specified, please enter 0 if no limit \n')

    if inputs.dt == -1:
        print('ERROR:')
        sys.exit('Timestep not specified, please provide timestep of original calculation \n')

    if inputs.surfaces == []:
        print('ERROR:')
        sys.exit('No surfaces given, please specify at least one surface/patch \n')

    # Ensure all paths have a trailing "/"
    if not inputs.path[-1] == '/':
        inputs.path += '/'

    if inputs.saveDir is not None:
        if not inputs.saveDir[-1] == '/':
            inputs.saveDir += '/'

    if inputs.writeDir is not None:
        if not inputs.writeDir[-1] == '/':
            inputs.writeDir += '/'

    if inputs.nickDir is not None:
        if not inputs.nickDir[-1] == '/':
            inputs.nickDir += '/'

    # Check that transformation specified if transformPoints option used
    if inputs.transformPoints:
        if inputs.translation is not None:
            __=1
        elif inputs.rotation is not None:
            __=1
        elif inputs.mirrorNormal is not None and inputs.mirrorCentre is not None:
            __=1
        else:
            print('ERROR:')
            sys.exit('transformPoints option selected, but no transformation provided')

    # Check at least one cut limit specified, and set all empty ones to +/- infinity
    if inputs.cutData:

        if not (inputs.xLow or inputs.xHigh or inputs.yLow or inputs.yHigh or inputs.zLow or inputs.zHigh):
            print('Error: ')
            sys.exit('cutData option used, but no limits supplied for cut')

        else:
            if inputs.xLow is None:
                inputs.xLow = float('-inf')
            if inputs.xHigh is None:
                inputs.xHigh = float('inf')
            if inputs.yLow is None:
                inputs.yLow = float('-inf')
            if inputs.yHigh is None:
                inputs.yHigh = float('inf')
            if inputs.zLow is None:
                inputs.zLow = float('-inf')
            if inputs.zHigh is None:
                inputs.zHigh = float('inf')
