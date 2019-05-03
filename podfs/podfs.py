import argparse
from argparse import ArgumentParser
from .podfs_functions import MyArgumentParser
from .podfs_functions import addArguments
import sys

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

    if inputs.readWholeCase:

        # Extract data from OpenFOAM Case
        print( "Extracting data from case: " + inputs.caseDir )

    if inputs.readSurfaces:

        surfaceData = list()

        # Read data from surfaces output by OpenFOAM post processing
        for i in range(0, len(inputs.surfaces)):

            print( "Reading data from surface: " + inputs.surfaces[i] )

            surfaceData.append( RawData(inputs.surfaceDir, inputs.surfaces[i], inputs.vars) )

    if inputs.interpolate or inputs.translate or inputs.rotate:

        print( "Transforming data" )

    if inputs.saveRawData:

        if inputs.readSurfaces:
            for i in range(len(surfaceData)):
                print( "Saving raw data for surface: " + inputs.surfaces[i] )
                surfaceData[i].write(inputs.rawDataDir + '/' + inputs.surfaces[i])
