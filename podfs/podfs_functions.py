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

    parser.add_argument('--EPOD', type=float, default=0.95)
    parser.add_argument('--EFS', type=float, default=0.9)
    parser.add_argument('--nMax', type=int, default=-1)
    parser.add_argument('--dt', type=float, default=-1.0)

    parser.add_argument('--writeDir', type=str)
    parser.add_argument('--writeFormat', type=str)

    parser.add_argument('--checkOutput', action='store_true')
    parser.add_argument('--nickDir', type=str)

    parser.add_argument('--checkReconstruction', action='store_true')

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

                --EPOD                  Desired energy content for POD modes, default 0.95
                --EFS                   Desired energy content for Fourier series, default 0.9

                --writeFormat           Format to write PODFS output in
                --writeDir              Location to save PODFS output to

                --checkOutput           Compare PODFS output to output from DigitalFiler.py
                --nickDir               Location of digitalfilter.py output

                --checkReconstruction   Compare each reconstructed timestep to the original snapshot and report mean
                                        error

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
