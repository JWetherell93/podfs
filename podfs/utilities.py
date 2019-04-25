import os
import sys
import shutil

def isInt(x):
    try:
        y = int(x)
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

        removeFile(file)

def writeFile(fullName, data):

    with open(fullName, "w+") as f:

        for i in range(0, len(data)):

            f.write('{:F}\n'.format(data[i]))
