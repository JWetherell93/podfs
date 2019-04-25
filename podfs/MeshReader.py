import numpy as np
import struct
import copy
from .utilities import isInt, removeChars

class face:
    def __init__(self, type, pIDs):
        self.type = type
        self.pIDs = pIDs
        self.neighbours = list()

class point:
    def __init__(self, x, y, z):
        self.component = np.array(np.zeros(3))
        self.component[0] = x
        self.component[1] = y
        self.component[2] = z

class cell:
    def __init__(self, cellID, faces, neighbours, onBoundary):
        self.cellID = cellID
        self.faces = faces
        self.neighbours = neighbours
        self.onBoundary = onBoundary

class boundary:
    def __init__(self, name, type, startFace, nFaces):
        self.name = name
        self.type = type
        self.startFace = startFace
        self.nFaces = nFaces

class cellFace:
    def __init__(self, type, fID, pIDs, points, neighbour):
        self.type = type
        self.pIDs = pIDs
        self.points = points
        self.neighbour = neighbour

    def calcFaceNormal(self):

        p1 = self.points[0,:]
        p2 = self.points[1,:]
        p3 = self.points[2,:]

        v1 = p2 - p1
        v2 = p3 - p1

        self.normal = np.cross(v1, v2)

class foamMesh:
    def __init__(self, meshDir, cellsDir, binary):
        self.readPoints(meshDir+"points", binary)
        self.readFaces(meshDir+"faces", binary)
        self.readOwner(meshDir+"owner", binary)
        self.readNeighbour(meshDir+"neighbour", binary)
        self.readBoundary(meshDir+"boundary")
        self.constructCells()
        self.readCentres(cellsDir+"C", binary)
        self.readVolumes(cellsDir+"V", binary)

    def readPoints(self, filename="constant/polyMesh/points", binary=False):

        # Read in everything in points file
        with open(filename, "r") as pointsFile:
            pointsData = pointsFile.readlines()

        # Find row containing number of points (first row that is only an integer)
        for i in range(len(pointsData)):
            if isInt(pointsData[i]):
                break

        # Read number of points
        nPoints = int(pointsData[i])

        # Initialise empty list to hold all points
        points = list()

        if binary:
            pointsBin = pointsData[i+1]

            pointsBin = removeChars(pointsBin, "()")

            for p in range(0,nPoints):

                tempPoint = struct.unpack("@ddd", pointsBin[p*24:p*24+24])

                x = tempPoint[0]
                y = tempPoint[1]
                z = tempPoint[2]

                points.append(point(x,y,z))

        else:

            # Remove all rows from file contents, apart from list of points
            pointsData = pointsData[i+2:i+nPoints+2]

            # Loop through each entry in list of points
            for dataRow in pointsData:

                # Remove brackets from string
                temp = removeChars(dataRow,"()")

                # Split string into different entries based on spaces
                temp = temp.split()

                # Extract x, y and z values
                x = float(temp[0])
                y = float(temp[1])
                z = float(temp[2])

                # Create instance of point class, append to points list
                points.append(point(x,y,z))

                # Clean variable
                del temp

        # Add points list and number of points list as attributes of foamMesh
        self.points = points
        self.nPoints = nPoints

    def readFaces(self, filename="constant/polyMesh/faces", binary=False):

        # Open file and read in contents
        with open(filename,"r") as facesFile:
            facesData = facesFile.readlines()

        # Read binary contents
        if binary:

            # Find line contining number of faces (first line that is just an integer)
            for i in range(len(facesData)):
                if isInt(facesData[i]):
                    break

            # Read in number of faces
            nFaces = int(facesData[i]) - 1

            # Find next row containing just an integer
            for j in range(i+1,len(facesData)):
                if isInt(facesData[j]):
                    break

            # Extract binary list of face indices
            faceIndices_b = facesData[i+1]

            # Remove first character, it's a bracket
            faceIndices_b = faceIndices_b[1:]

            # Check that list hasn't been split over multiple lines
            # Concatenate if it has
            if (j - i) > 2:
                k = i + 2
                while k < j:
                    faceIndices_b = faceIndices_b + facesData[k]
                    k = k + 1

            # Find row containing just a new line marker
            for k in range(j,len(facesData)):
                if facesData[k] == "\n":
                    break

            # Extract binary list of face vertices
            faceVertices_b = facesData[j+1]

            # Remove first character, it's a bracket
            faceVertices_b = faceVertices_b[1:]

            # Check that list hasn't been split over multiple lines
            # Concatenate if it has
            if (k - j) > 2:
                i = j + 2
                while i < k:
                    faceVertices_b = faceVertices_b + facesData[i]
                    i = i + 1

            # Convert binary list to python list for face faceIndices
            faceIndices = list()

            # Indices stored as 4 byte integers
            for i in range(0, len(faceIndices_b)/4):
                faceIndex = struct.unpack("@i", faceIndices_b[i*4:i*4+4])
                faceIndex = int(faceIndex[0])
                faceIndices.append(faceIndex)

            # Convert binary list to python list for face face vertices
            faceVertices = list()

            # Vertices stored as 4 byte integers
            for i in range(0, len(faceVertices_b)/4):
                faceVertex = struct.unpack("@i", faceVertices_b[i*4:i*4+4])
                faceVertex = int(faceVertex[0])
                faceVertices.append(faceVertex)

            # Create empty list of faces
            faces = list()

            # Use index list and vertex list to construct list of vertices for each face
            for i in range(0, len(faceIndices)-1):
                start = faceIndices[i]
                end = faceIndices[i+1]
                pIDs = faceVertices[start:end]

                # Classify face based on number of points
                if len(faceVertices) == 3:
                    type = "tria"
                elif len(faceVertices) == 3:
                    type = "quad"
                elif len(faceVertices) >= 4:
                    type = "poly"

                # Create face instance
                faces.append(face(type, pIDs))


        # Read ascii contents
        else:

            # Find line contining number of faces (first line that is just an integer)
            for i in range(len(facesData)):
                if isInt(facesData[i]):
                    break

            # Read in number of faces
            nFaces = int(facesData[i])

            # Remove un-needed lines, leaving only list of faces
            facesData = facesData[i+2:i+nFaces+2]

            # Create empty list for faces
            faces = list()

            # Loop through each row
            for dataRow in facesData:

                # First number in row is number of points that make up the face
                facePoints = int(dataRow[0])

                # Classify face based on number of points
                if facePoints == 3:
                    type = "tria"
                elif facePoints == 3:
                    type = "quad"
                elif facePoints >= 4:
                    type = "poly"

                # Remove brakets from remainder of row
                temp = removeChars(dataRow[1:],"()")

                # Split entry based on spaces
                temp = temp.split()

                # Create empty list for point IDs
                pIDs = list()

                # Append each point ID into list
                for i in range(0,len(temp)):
                    pIDs.append(int(temp[i]))

                # Append face instance onto list of facesFile
                faces.append(face(type,pIDs))

        # Add number of faces and list of faces as foamMesh attributes
        self.faces = faces
        self.nFaces = nFaces

    def readOwner(self, filename="constant/polyMesh/owner", binary=False):

        # Open file, and read all contents
        with open(filename,"r") as ownerFile:
            ownerData = ownerFile.readlines()

        # Find row that starts with "note"
        for i in range(len(ownerData)):
            if ownerData[i][4:8] == "note":
                break

        # Split row
        info = ownerData[i].split()

        # Go through each entry, extract nCells and nInternalFaces
        for j in range(len(info)):
            if info[j] == "nCells:":
                self.nCells = int(info[j+1])
            if info[j] == "nInternalFaces:":
                self.nInternalFaces = int(removeChars(info[j+1],"\";"))

        # Find row containing integer only, which is start of owner list
        for k in range(len(ownerData)):
            if isInt(ownerData[k]):
                break

        # Binary reader
        if binary:
            # Extract binary data, first character is un-needed bracket
            ownerList_b = ownerData[k+1]
            ownerList_b = ownerList_b[1:]

            # For each face, append owner to neighbour list
            for i in range(0, len(ownerList_b)/4):
                owner = struct.unpack("@i", ownerList_b[i*4:i*4+4])
                owner = int(owner[0])
                self.faces[i].neighbours.append(owner)

        else:

            # Remove unnecessary lines from ownerData
            ownerData = ownerData[k+2:k+2+self.nFaces]

            # For each face, append owner to neighbour list
            for i in range(len(ownerData)):
                owner = int(ownerData[i])
                self.faces[i].neighbours.append(owner)

    def readNeighbour(self, filename="constant/polyMesh/neighbour", binary=False):

        # Open file, and read all contents
        with open(filename, "r") as neighbourFile:
            neighbourData = neighbourFile.readlines()

        # Find row containing integer only, start of neighbour list
        for i in range(len(neighbourData)):
            if isInt(neighbourData[i]):
                break

        # Binary reader
        if binary:
            # Extract binary data, first value is un-needed bracket
            neighbourList_b = neighbourData[i+1]
            neighbourList_b = neighbourList_b[1:]

            # For each internal face, append neighbour to neighbour list
            for i in range(0, len(neighbourList_b)/4):
                neighbour = struct.unpack("@i", neighbourList_b[i*4:i*4+4])
                # unpack outputs result as tuple, extract to give int
                neighbour = int(neighbour[0])
                self.faces[i].neighbours.append(neighbour)

        # ASCII reader
        else:
            # Remove unnecessary lines from neighbourData
            neighbourData = neighbourData[i+2:i+2+self.nInternalFaces]

            # For each internal face, append neighbour to neighbour list
            for j in range(len(neighbourData)):
                neighbour = int(neighbourData[j])
                self.faces[j].neighbours.append(neighbour)

    def readBoundary(self, filename="constant/polyMesh/boundary"):

        # Read file contents
        with open(filename, "r") as boundaryFile:
            boundaryData = boundaryFile.readlines()

        # Find number of boundaries
        for i in range(0, len(boundaryData)):
            if isInt(boundaryData[i]):
                self.nBoundaries = int(boundaryData[i])
                break

        # Initialise lists
        boundaries = list()
        start = list()
        end = list()

        j = i

        # Get start and end indices for each boundary
        while len(end) < self.nBoundaries:
            if boundaryData[j].split()[0] == "{":
                start.append(j-1)
            if boundaryData[j].split()[0] == "}":
                end.append(j)
            j = j + 1

        # Construct boundary class instance
        for i in range(self.nBoundaries):
            Boundary = boundaryData[start[i]:end[i]]

            name = Boundary[0].split()[0]

            type = Boundary[2].split()[1]
            type = removeChars(type, ";")

            for j in range(3, len(Boundary)):
                temp = Boundary[j].split()

                if temp[0] == "nFaces":
                    nFaces = int(removeChars(temp[1], ";"))
                elif temp[0] == "startFace":
                    startFace = int(removeChars(temp[1], ";"))
                elif temp[0] == "neighbourPatch":
                    neighbourPatch = removeChars(temp[1], ";")
                elif temp[0] == "transform":
                    transformType = removeChars(temp[1], ";")


            boundaries.append(boundary(name, type, startFace, nFaces))

            if type == "cyclic":
                boundaries[-1].neighbourPatch = neighbourPatch
                boundaries[-1].transformType = transformType

        self.boundaries = boundaries

    def constructCells(self):

        self.cells = list()

        for cellID in range(0, self.nCells):

            onBoundary = False

            fIDs = list()

            for face in range(0, self.nFaces):
                if cellID in self.faces[face].neighbours:
                    fIDs.append(face)

            faces = list()

            for fID in fIDs:

                pIDs = self.faces[fID].pIDs

                type = self.faces[fID].type

                points = np.array(np.zeros([len(pIDs),3]))

                for i in range(0, len(pIDs)):

                    points[i,:] = copy.deepcopy(self.points[pIDs[i]].component)

                faceNeighbours = self.faces[fID].neighbours

                neighbours = list()

                if len(faceNeighbours) == 2:

                    if faceNeighbours[0] == cellID:
                        neighbours.append(faceNeighbours[1])
                        neighbour = faceNeighbours[1]
                    elif faceNeighbours[1] == cellID:
                        neighbours.append(faceNeighbours[0])
                        neighbour = faceNeighbours[0]

                else:

                    onBoundary = True

                    for boundary in self.boundaries:

                        if (face >= boundary.startFace) and (face < boundary.startFace+boundary.nFaces):

                            neighbours.append(boundary)
                            neighbour = -1

                faces.append(cellFace(type, fID, pIDs, points, neighbour))

                faces[-1].calcFaceNormal()

            self.cells.append(cell(cellID, faces, neighbours, onBoundary))

    def readCentres(self, filename="0/C", binary=False):

        # Only read file if it exists, else skip function
        try:
            with open(filename, "r") as centresFile:
                centresData = centresFile.readlines()
        except IOError:
            print "No cell centres file found, skipping"
            return

        # Binary reader
        if binary:

            # Find number of points in field, check it matches mesh
            for i in range(0, len(centresData)):
                if isInt(centresData[i]):
                    if int(centresData[i]) != self.nCells:
                        raise Exception("Number of cells in centres file does not match number in mesh files")
                    break

            # Extract binary data
            centres_b = centresData[i+1][1:]

            # For each cell
            for j in range(0, self.nCells):

                # Unpack x, y and z coordinates of cell centres
                centre = struct.unpack("@ddd", centres_b[j*24:j*24+24])

                # Convert to floating point numbers
                c_x = float(centre[0])
                c_y = float(centre[1])
                c_z = float(centre[2])

                # Create point instance for cell centre within cell instance
                self.cells[j].c = point(c_x, c_y, c_z)

        else:

            # Find data list
            for i in range(0, len(centresData)):
                if len(centresData[i].split()) >= 1:
                    if centresData[i].split()[0] == "internalField":
                        break

            # Split to get only list of values
            centres = centresData[i].split(">")[1]

            # Check number of points in field matches number of cells in mesh
            if int(centres[1]) != self.nCells:
                raise Exception("Number of cells in centres file does not match number in mesh files")

            # Remove space and number of field values from start of list
            centres = centres[2:]

            # Remove all brackets and trailing semi colon
            centres = removeChars(centres, "();")

            # Split each value into individual list entries
            centres = centres.split()

            # For each cell
            for i in range(0, self.nCells):

                # Convert to floats
                c_x = float(centres[i*3])
                c_y = float(centres[i*3+1])
                c_z = float(centres[i*3+2])

                # Create point instance for cell centre within cell instance
                self.cells[i].c = point(c_x, c_y, c_z)

    def readVolumes(self, filename="0/V", binary=False):

        # Only open file if it exists, otherwise exit function
        try:
            with open(filename, "r") as volumesFile:
                volumesData = volumesFile.readlines()
        except:
            print "No cell volumes file found, skipping"
            return

        # Binary reader
        if binary:

            # Find line containing internal field information
            for i in range(0, len(volumesData)):
                if len(volumesData[i].split()) >= 1:
                    if volumesData[i].split()[0] == "internalField":
                        break

            # If field is uniform, reading in data becomes much easier
            if volumesData[i].split()[1] == "uniform":

                volume = int( removeChars( volumesData[i].split()[2], ";" ) )

                for i in range(0, self.nCells):

                    self.cells[i].V = volume

            # If field not uniform
            else:

                # Find binary data entries, check field matches mesh
                for i in range(0, len(volumesData)):
                    if isInt(volumesData[i]):
                        if int(volumesData[i]) != self.nCells:
                            raise Exception("Number of cells in volumes file does not match number in mesh files")
                        break

                # Extract binary data entries
                volumes_b = volumesData[i+1][1:]

                # Add cell volume to cell instance
                for j in range(0, self.nCells):

                    volume = struct.unpack("@d", volumes_b[j*8:j*8+8])

                    self.cells[j].V = float(volume[0])

        # ASCII reader
        else:

            # Find field information
            for i in range(0, len(volumesData)):
                if len(volumesData[i].split()) >= 1:
                    if volumesData[i].split()[0] == "internalField":
                        break

            # For uniform field, reading becomes much easier
            if volumesData[i].split()[1] == "uniform":

                volume = int( removeChars( volumesData[i].split()[2], ";" ) )

                for i in range(0, self.nCells):

                    self.cells[i].V = volume

            # For non-uniform field
            else:

                # Get data list
                volumes = volumesData[i].split(">")[1]

                # Check field agrees with mesh
                if int(volumes[1]) != self.nCells:
                    raise Exception("Number of cells in volumes file does not match number in mesh files")

                # Remove space and number of cells from beginning of list
                volumes = volumes[2:]

                # Remove all brackets and final semi-colon
                volumes = removeChars(volumes, "();")

                # Split list so each value is a separate list entry
                volumes = volumes.split()

                #Add volumes to cell instances
                for i in range(0, self.nCells):

                    volume = float(volumes[i])

                    self.cells[i].V = volume
