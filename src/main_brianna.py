import os, sys
import numpy
import struct
from matplotlib import pylab, pyplot, cm
from math import sqrt
import random


#Binary Files info
#16b unsigned int
#width = height = 256
#LitleEndian
#header to skip 512 bytes

path = "../data"
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
#len(filePaths)))

#for index, fileName in enumerate(fileNames):
#print("{0} -> {1}".format(index, fileName))

#fileNo = int(input())

#reading binary file
with open(filePaths[4], 'rb') as binaryFile:
    #skip header and read
    header_size = 512
    data_header = binaryFile.read(header_size) 
    #utf-8 and ascii decoding fails bytes(data_header).decode('utf-8')
    
    # Data_img_decoded will be the file of pixel values used for the algorithm
    data_img_decoded = []

    for i in range(256):
        temp = []

        for i in struct.iter_unpack('<H', bytes(binaryFile.read(512))):
            temp.append(*i)
        

        data_img_decoded.append(temp)

#Convert data_img_decoded to float
data_img_decoded = numpy.array(data_img_decoded) + 0.

#Print the dimensions of the image to check
#print(len(data_img_decoded))
#print(len(data_img_decoded[0]))

#pyplot.imshow(data_img_decoded, cmap = cm.Greys_r)
#pyplot.show()

#Use image data stored in data_img_decoded to create a quality map

#Create a simple 9x9 image to work with
N = 9
simple_data = [[random.randrange(0,4096) for i in range(N)] for j in range(N)]
other_data = numpy.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]) +0.
#pyplot.imshow(simple_data, cmap = cm.Greys_r)
#pyplot.show()

#Function which finds the quality value for each pixel to produce a matrix N-1xN-1
def quality_map(list):
    imrange = len(list)
    for x in range(1,(imrange-1)):
        for y in range(1,(imrange-1)):
            xsum = 0
            ysum = 0
            xdiff = 0
            ydiff = 0
            #Compute the partial derivatives in the x and y directions
            for z in range(-1,2):
                xsum0 = list[y-1][x+z] - list[y][x]
                xsum2 = list[y+1][x+z] - list[y][x]
                ysum0 = list[y+z][x-1] - list[y][x]
                ysum2 = list[y+z][x+1] - list[y][x]
                xsum = xsum + xsum0 + xsum2
                ysum = ysum + ysum0 + ysum2
                z += 1
            xmean = xsum/6.
            ymean = ysum/6.
            for z in range(-1,2):
                xdiff0 = (list[y-1][x+z] - xmean)**2.
                xdiff2 = (list[y+1][x+z] - xmean)**2.
                xdiff = xdiff + xdiff0 + xdiff2
                ydiff0 = (list[y+z][x-1] - ymean)**2.
                ydiff2 = (list[y+z][x+1] - ymean)**2.
                ydiff = ydiff + ydiff0 + ydiff2
                z += 1
            quality_value = (sqrt(xdiff)+sqrt(ydiff))/9.
            print(quality_value)
#quality_map[x-1][y-1] = quality_value
#return quality_map


quality_map(simple_data)
quality_map(other_data)
quality_map(data_img_decoded)





