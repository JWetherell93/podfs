from .utilities import printProgressBar

def transform(output, inputs):

    if inputs.translation is not None:
        translatePoints(output, inputs.translation)

    if inputs.rotation is not None:
        rotatePoints(output, inputs.rotation)

def translatePoints(output, translation):

    points = output.coords

    print("Translating points by: " + '{0:.6f}, {1:.6f}, {2:.6f}'.format(translation[0], translation[1], translation[2]))

    for i in range(0, len(points)):

        points[i,0] += translation[0]
        points[i,1] += translation[1]
        points[i,2] += translation[2]

        printProgressBar(i, len(points)-1)

    output.coords = points

def rotatePoints(output, rotation):

    points = output.coords

    rotation = rotation * np.pi / 180

    Rx = np.array([ [1, 0, 0],
                    [0, np.cos(rotation[0]), -np.sin(rotation[0])],
                    [0, np.sin(rotation[0]), np.cos(rotation[0])]   ])

    Ry = np.array([ [np.cos(rotation[1]), 0, np.sin(rotation[1])],
                    [0, 1, 0],
                    [-np.sin(rotation[1]), 0, np.cos(rotation[1])]  ])

    Rz = np.array([ [np.cos(rotation[2]), -np.sin(rotation[2]), 0],
                    [np.sin(rotation[2]), np.cos(rotation[2]), 0],
                    [0, 0, 1]                                       ])

    R = np.matmul(np.matmul(Rz, Ry), Rx)

    print("Rotating points by: " + '{0:.2f}, {1:.2f}, {2:.2f} degrees'.format(rotation[0], rotation[1], rotation[2]))

    for i in range(0, len(points)):

        points[i,:] = np.matmul(R, points[i,:])

        printProgressBar(i, len(points))

    output.coords = points

def mirrorPoints(output, inputs):

    print()
