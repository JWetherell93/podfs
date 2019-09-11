import argparse
from argparse import ArgumentParser
import textwrap

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

def addArguments(parser):

    parser.add_argument('-h', '--help', action='store_true')

    parser.add_argument('--format', type=str, default='null')

    parser.add_argument('--path', type=str, default='null')

    parser.add_argument('--vars', nargs='*', default='null', type=str)

    parser.add_argument('--surfaces', nargs='*', type=str)

    parser.add_argument('--saveRawData', action='store_true')
    parser.add_argument('--saveDir', type=str)

    parser.add_argument('--ET', type=float, default=0.9)
    parser.add_argument('--NM', type=int)
    parser.add_argument('--dt', type=float)

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

                --nm                    Number of spatial modes to use
                --dt                    Timestep of original calculation

            Optional Arguments:
                -h, --help              Show help message and exit

                --surfaces              List of surface names

                --saveRawData           Save pre-processed data prior to running analysis
                --saveDir               Directory in which to save pre-processed data

                --ET                    Energy target for calculation of Fourier Coefficients, default 0.9

                --writeFormat           Format to write PODFS output in
                --writeDir              Location to save PODFS output to

                --checkOutput           Compare PODFS output to output from DigitalFiler.py
                --nickDir               Location of digitalfilter.py output

                --checkReconstruction   Compare each reconstructed timestep to the original snapshot and report mean
                                        error

    ''')
