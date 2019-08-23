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

    parser.add_argument('--format', type=str, default='null', help='Format of data to be read in')

    parser.add_argument('--path', type=str, default='null', help='Location of input data. Should be in format expected by format specifier')

    parser.add_argument('--vars', nargs='*', default='null', type=str, help='Variables to apply PODFS to')

    parser.add_argument('--surfaces', nargs='*', type=str, help='List of surface names to read')

    parser.add_argument('--ET', type=float, help='Energy target for calculating which fourier modes to use')
    parser.add_argument('--NM', type=int, help='Number of spatial modes to use')
    parser.add_argument('--dt', type=float, help='Timestep of original calculation')

    parser.add_argument('--writeDir', type=str, help='Location to write output to')
    parser.add_argument('--writeFormat', type=str, help='Format of output data')

    parser.add_argument('--checkOutput', action='store_true', help='Check calculated output against NT digitalfilters output')
    parser.add_argument('--nickDir', type=str, help='Directory containing outputs from digitialfilter.py')

    parser.add_argument('--checkReconstruction', action='store_true', help='Reconstruct each timestep and compare to raw data')

    # parser.add_argument('--readWholeCase', action='store_true', help='Read OpenFOAM case, and extract data')
    # parser.add_argument('--caseDir', type=str, help='Path to case directory')
    #
    # parser.add_argument('--readSurfaces', action='store_true', help='Readsurface VTK data output by OpenFOAM post processing')
    # parser.add_argument('--surfaceDir', type=str, help='Path to surface data directory')
    # parser.add_argument('--surfaces', nargs='*', type=str, help='List of surface names to read')
    #
    # parser.add_argument('--interpolate', action='store_true', help='Interpolate data onto new mesh')
    #
    # parser.add_argument('--translate', action='store_true', help='Translate points by specified vector')
    #
    # parser.add_argument('--rotate', action='store_true', help='Rotate points about point by specified vector')
    #
    # parser.add_argument('--saveRawData', action='store_true', help='Save pre-processed raw data')
    # parser.add_argument('--rawDataDir', type=str, help='Directory to write pre-processed raw data to')
    #
    # parser.add_argument('--et', type=float, help='Energy target for calculating which fourier modes to use')

    parser.description = textwrap.dedent('''\
            Program for PODFS data compression. Pre-processor options available.

            Arguments can be given by file, using "@" before file name. For example
            "podfs @inputs.txt"

            Optional Arguments:
            -h, --help                  Show help message and exit

    ''')

    # parser.add_help = False
    #
    # parser.formatter_class = argparse.RawDescriptionHelpFormatter
