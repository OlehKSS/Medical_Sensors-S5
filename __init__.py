import os, sys
import numpy
from matplotlib import pylab, pyplot, cm
from scipy import signal
from _shared.phase_image import PhaseImage
from skimage import filters
from region_growing_linear_est.quality_maps import quality_map_second_order
from math import sqrt
from particle_swarm_optimization.particle_initialization import phase_derivative_variance
from particle_swarm_optimization.particle_initialization import threshold
from particle_swarm_optimization.calculate_residues import calculate_residues
from particle_swarm_optimization.particle_initialization import find_polarity_arrays


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

#stuff for finding the phase derv map
phasemap = phase_derivative_variance(data)
binary = threshold(phasemap)

#calculating the residues
residue_map = calculate_residues(data)
#fig = pyplot.figure()
#pyplot.gray()
#ax1 = fig.add_subplot(121)  # left side
#ax2 = fig.add_subplot(122)  # right side
#ax1.imshow(binary)
#ax2.imshow(residue_map)
#pyplot.show()

#calculating the residues
[positive_polarity_array_region1, positive_polarity_array_region0,negative_polarity_array_region1, negative_polarity_array_region0] = find_polarity_arrays(binary,residue_map)

print(positive_polarity_array_region1)


#image = io.imread('test_heart_image.jpg',as_grey = True)
