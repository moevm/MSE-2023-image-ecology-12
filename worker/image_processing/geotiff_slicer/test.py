import os
from glob import glob

from slice2tiles import sliceToTiles
from geotiff2png import geotiffToPng

# Get path to current dir
currDir = os.getcwd()

# Get all images in test\img
tiffImageNames = glob("test\\img\\*")

# Generate tiles for geotiffs in test\img and store to test\output:
for i in range(len(tiffImageNames)):
    print('-'*100)
    print('<-->', i, tiffImageNames[i])
    # Cut path to file
    fileName = tiffImageNames[i][tiffImageNames[i].rfind('\\') + 1:]
    # Cut extension
    fileName = fileName[:fileName.rfind('.')]

    sliceToTiles(currDir + '\\' + tiffImageNames[i], currDir + '\\test\\output\\' + fileName)

# Convert geotiff from test\img to png ang store to test\output
for i in range(len(tiffImageNames)):
    # Cut path to file
    fileName = tiffImageNames[i][tiffImageNames[i].rfind('\\') + 1:]
    # Cut extension
    fileName = fileName[:fileName.rfind('.')]

    geotiffToPng(currDir + '\\' + tiffImageNames[i], currDir + '\\test\\output\\' + fileName + '.png')
