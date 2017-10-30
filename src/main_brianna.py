import os, sys, numpy, struct, random
from matplotlib import pylab, pyplot, cm
from math import sqrt
from quality_map_functions import quality_map_first_order, quality_map_second_order


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


#Create a simple 9x9 image to work with
N = 9
simple_data = [[random.randrange(0,4096) for i in range(N)] for j in range(N)]
other_data = numpy.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]) +0.

#Find the quality map for the image using the module quality_map_functions
#quality_map_array = quality_map_first_order(simple_data)
#print(quality_map_array)

quality_map_array = quality_map_first_order(simple_data)
print(quality_map_array)

quality_map_array1 = quality_map_second_order(simple_data)
print(quality_map_array1)





