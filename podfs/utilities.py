import os
import sys
import shutil
import numpy as np
from os.path import isfile, isdir
import textwrap

def isInt(x):
    try:
        y = int(x)
        return True
    except ValueError:
        return False

def isFloat(x):
    try:
        y = float(x)
        return True
    except ValueError:
        return False

def removeChars(text,chars):
    for c in chars:
        if c in text:
            text = text.replace(c,"")

    return text

def removeDir(dir):
    try:
        shutil.rmtree(dir)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

def removeFile(file):
    try:
        os.remove(file)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

def cleanDir(dir):

    dirContents = os.listdir(dir)

    for i in range(0, len(dirContents)):

        file = dir + "/" + dirContents[i]

        if isfile(file):
            removeFile(file)

        elif isdir(file):
            cleanDir(file)
            removeDir(file)

def writeFile(fullName, data):

    with open(fullName, "w+") as f:

        for i in range(0, len(data)):

            f.write('{:F}\n'.format(data[i]))

def writeVectorFile(fullName, data):

    with open(fullName, "w+") as f:

        for i in range(0, np.shape(data)[0]):

            f.write('{:F} '.format(data[i, 0]))
            f.write('{:F} '.format(data[i, 1]))
            f.write('{:F}\n'.format(data[i, 2]))

def writeFoamHeader(fileObject, CLASS):

    fileObject.write(textwrap.dedent('''\
                // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
                FoamFile
                {
                    version     2.0;
                    format      ascii;
                    class       '''+CLASS+''';
                    location    "constant";
                    object      mode;
                }
                // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
                '''
    ))

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=95, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()
