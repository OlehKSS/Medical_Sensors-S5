import os, sys
import numpy
import struct
from matplotlib import pylab, pyplot, cm


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

print("Byte order", sys.byteorder)
print("Number of files found is {0}. Which would you like to open?".format(
    len(filePaths)))

for index, fileName in enumerate(fileNames):
    print("{0} -> {1}".format(index, fileName))    

fileNo = int(input())

#reading binary file
with open(filePaths[fileNo], 'rb') as binaryFile:
    #skip header and read
    header_size = 512
    data_header = binaryFile.read(header_size) 
    #utf-8 and ascii decoding fails bytes(data_header).decode('utf-8')

    data_img_decoded = []

    for i in range(255):
        temp = []

        for i in struct.iter_unpack('<H', bytes(binaryFile.read(512))):
            temp.append(*i)
        
        data_img_decoded.append(temp)

    pyplot.imshow(data_img_decoded, cmap = cm.Greys_r)
    pyplot.show()   

    