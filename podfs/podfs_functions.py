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

    parser.add_argument('--vars', nargs='*', type=str, help='Variables to apply PODFS to')

    parser.add_argument('--readWholeCase', action='store_true', help='Read OpenFOAM case, and extract data')
    parser.add_argument('--caseDir', type=str, help='Path to case directory')

    parser.add_argument('--readSurfaces', action='store_true', help='Readsurface VTK data output by OpenFOAM post processing')
    parser.add_argument('--surfaceDir', type=str, help='Path to surface data directory')
    parser.add_argument('--surfaces', nargs='*', type=str, help='List of surface names to read')

    parser.add_argument('--interpolate', action='store_true', help='Interpolate data onto new mesh')

    parser.add_argument('--translate', action='store_true', help='Translate points by specified vector')

    parser.add_argument('--rotate', action='store_true', help='Rotate points about point by specified vector')

    parser.add_argument('--saveRawData', action='store_true', help='Save pre-processed raw data')
    parser.add_argument('--rawDataDir', type=str, help='Directory to write pre-processed raw data to')

    parser.add_argument('--et', type=float, help='Energy target for calculating which fourier modes to use')

    parser.description = textwrap.dedent('''\
            Program for PODFS data compression. Pre-processor options availableself.

            Arguments can be given by file, using "@" before file name. For example
            "podfs @inputs.txt"

            Optional Arguments:
            -h, --help                  Show help message and exit

    ''')

    # parser.add_help = False
    #
    # parser.formatter_class = argparse.RawDescriptionHelpFormatter
