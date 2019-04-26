from argparse import ArgumentParser

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

def main():

	parser = MyArgumentParser(
							prog = 'podfs',
							usage = '%(prog)s [options]',
							description = 'Script for PODFS data compression, including pre-processor options',
							fromfile_prefix_chars = '@'
							)

	parser.add_argument('--readCase', action='store_true')
	parser.add_argument('--caseDir')

	parser.add_argument('--readSurfaces', action='store_true')
	parser.add_argument('--surfaceDir')
	parser.add_argument('--surfaces', nargs='*')

	parser.add_argument('--interpolate', action='store_true')

	parser.add_argument('--translate', action='store_true')

	parser.add_argument('--rotate', action='store_true')

	parser.add_argument('--saveRawData', action='store_true')

	inputs = parser.parse_args()

	if inputs.readCase:

		# Extract data from OpenFOAM Case
		print "Extracting data from case: " + inputs.caseDir

	if inputs.readSurfaces:

		# Read data from surfaces output by OpenFOAM post processing
		for i in range(0, len(inputs.surfaces)):
			print "Reading data from surface: " + inputs.surfaces[i]

	if inputs.interpolate or inputs.translate or inputs.rotate:

		print "Transforming data"

	if inputs.saveRawData:

		# Save processed surface data
		print "Saving raw data"
