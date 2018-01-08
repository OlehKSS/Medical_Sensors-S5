import os, sys
import numpy
from matplotlib import pylab, pyplot, cm
from scipy import signal
from skimage import io
from _shared.phase_image import PhaseImage
from skimage import filters
from region_growing_linear_est.quality_maps import quality_map_second_order
from math import sqrt
from region_growing_linear_est.linear_regression import linear_reg
from particle_swarm_optimization.particle_initialization import phase_derivative_variance, threshold
from particle_swarm_optimization.particle_operations import find_polarity_arrays
from particle_swarm_optimization.find_residues import calculate_residues


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


#image = io.imread('test_heart_image.jpg',as_grey = True)
#stuff for finding the phase derv map
#phasemap = phase_derivative_variance(data)
#binary = threshold(phasemap)

#calculating the residues
#residue_map = calculate_residues(data)

#calculating the residues
#[S1, S0, U1, U0] = find_polarity_arrays(binary,residue_map)

#Set values to parameters of dPSO
#T = 1000    #maximal iteration times
#c1 = 2      #learning factor 1
#c2 = 2      #learning factor 2

#fig = pyplot.figure()
#pyplot.gray()
#ax1 = fig.add_subplot(221)  # left side
#ax2 = fig.add_subplot(222)  # right side
#ax3 = fig.add_subplot(223)
#ax4 = fig.add_subplot(224)
#ax1.imshow(data)
#ax2.imshow(phasemap)
#ax3.imshow(binary)
#ax4.imshow(residue_map)
#pyplot.show()

binary = numpy.zeros((256,256))
binary[244,100] = 1
phi_unwr_data = 100*numpy.ones((256,256))
phi_unwr_data[244][100] = data[244][100]
unwrapped_value = linear_reg(binary, phi_unwr_data, data, (245,100), 7)
print(unwrapped_value)

