import os, sys
import numpy
from matplotlib import pylab, pyplot, cm
from _shared.phase_image import PhaseImage
from region_growing_linear_est.quality_maps import quality_map_first_order, quality_map_second_order

#Binary Files info
#16b unsigned int
#width = height = 256
#LitleEndian
#header to skip 512 bytes

path = "./data"
fileExt = [".sur"]
filePaths = []
fileNames = []

#finding all files in folder
for dirName, subdirList, fileList in os.walk(path):
    for fileName in fileList:
        if fileExt[0] in fileName.lower():
            fileNames.append(fileName)
            filePaths.append(os.path.join(dirName, fileName))

print("Byte order", sys.byteorder)
print("Number of files found is {0}. Which would you like to open?".format(
    len(filePaths)))

for index, fileName in enumerate(fileNames):
    print("{0} -> {1}".format(index, fileName))    

fileNo = int(input())

#reading binary file
phase_img = PhaseImage(256, 256, path = filePaths[fileNo])
data = phase_img.read()
#pyplot.imshow(data, cmap = cm.Greys_r)
#pyplot.show()  

#calculate quality maps

qm1 = quality_map_first_order(data)

qm2 = quality_map_second_order(data)
  