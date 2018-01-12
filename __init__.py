import os, sys
import numpy
from matplotlib import pylab, pyplot, cm
from scipy import signal
from skimage import io
from _shared.phase_image import PhaseImage
from skimage import filters
#from region_growing_linear_est.quality_maps import quality_map_second_order
from math import sqrt
#from region_growing_linear_est.linear_regression import linear_reg
from particle_swarm_optimization.particle_initialization import phase_derivative_variance, threshold
from particle_swarm_optimization.particle_operations import find_polarity_arrays
from particle_swarm_optimization.find_residues import calculate_residues
from particle_swarm_optimization.dPSO_algorithm import find_best_match_by_dPSO

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

#print("Byte order", sys.byteorder)
#print("Number of files found is {0}. Which would you like to open?".format(
#    len(filePaths)))

#for index, fileName in enumerate(fileNames):
#    print("{0} -> {1}".format(index, fileName))

#fileNo = int(input())

#reading binary file
#phase_img = PhaseImage(256, 256, path = filePaths[fileNo])
#data = phase_img.read()
data = io.imread('test_heart_image.jpg',as_grey = True)

print("What would you like to do?")
print("1 -> Display wrapped phase image")
print("2 -> Calculate and display phase derivative variance and thresholded variance maps")
print("3 -> Calculate and display residue map")
print("4 -> Perform dPSO to obtain Pg for all regions")

operation = int(input())

if operation == 1:
    pyplot.imshow(data, cmap = cm.Greys_r)
    pyplot.title('Wrapped Phase Image')
    pyplot.show()
elif operation == 2:
    print("Please wait...")
    phasemap = phase_derivative_variance(data)
    binary = threshold(phasemap)
    fig = pyplot.figure()
    pyplot.gray()
    ax1 = fig.add_subplot(131)  # left side
    ax2 = fig.add_subplot(132)  # right side
    ax3 = fig.add_subplot(133)
    ax1.set_title('Wrapped Phase Image')
    ax2.set_title('Phase Derivative Variance Map')
    ax3.set_title('Thresholded PDV Map')
    ax1.imshow(data)
    ax2.imshow(phasemap)
    ax3.imshow(binary)
    pyplot.show()
elif operation == 3:
    residue_map = calculate_residues(data)
    fig = pyplot.figure()
    pyplot.gray()
    ax1 = fig.add_subplot(121)  # left side
    ax2 = fig.add_subplot(122)
    ax1.imshow(data)
    ax2.imshow(residue_map)
    ax1.set_title('Wrapped Phase Image')
    ax2.set_title('Residue Map')
    pyplot.show()
elif operation == 4:
    #Set values to parameters of dPSO
    T = 1000    #maximal iteration times
    c1 = 2      #learning factor 1
    c2 = 2      #learning factor 2
    print("How many particles in the swarm? (if unknown, enter 300)")
    num_particles = int(input())
    find_best_match_by_dPSO(data, num_particles, T, c1, c2)
else:
    print("Please enter a valid operation")

