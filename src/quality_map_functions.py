import numpy
from math import sqrt

#Use image data stored in data_img_decoded to create a quality map

#Function which finds the first order quality value for each pixel to produce a matrix N-1xN-1
def quality_map_first_order(list):
    #Define a black border around the edge of the list for the quality map
    list = numpy.pad(list, 1, 'constant', constant_values=0)
    imrange = len(list)
    quality_map = numpy.empty([imrange-2,imrange-2],dtype = float)
    for x in range(1,(imrange-1)):
        for y in range(1,(imrange-1)):
            xsum = 0
            ysum = 0
            xdiff = 0
            ydiff = 0
            #Compute the partial derivatives in the x and y directions
            for z in range(-1,2):
                xsum0 = list[y-1][x+z] - 2. * list[y][x] + list[y+1][x+z]
                ysum0 = list[y+z][x-1] - 2. * list[y][x] + list[y+z][x+1]
                xsum = xsum + xsum0
                ysum = ysum + ysum0
                z += 1
            xmean = xsum/6.
            ymean = ysum/6.
            for z in range(-1,2):
                xdiff0 = (list[y-1][x+z] - xmean)**2. + (list[y+1][x+z] - xmean)**2.
                xdiff = xdiff + xdiff0
                ydiff0 = (list[y+z][x-1] - ymean)**2. + (list[y+z][x+1] - ymean)**2.
                ydiff = ydiff + ydiff0
                z += 1
            quality_value = (sqrt(xdiff)+sqrt(ydiff))/9.
            quality_map[x-1][y-1] = quality_value
    return quality_map

def quality_map_second_order(list):
    #Define a black border around the edge of the list for the quality map
    list = numpy.pad(list, 1, 'constant', constant_values=0)
    imrange = len(list)
    quality_map = numpy.empty([imrange-4,imrange-4],dtype = float)
    quality_map = numpy.empty([imrange-4,imrange-4],dtype = float)
    for x in range(2,(imrange-2)):
        for y in range(2,(imrange-2)):
            xpartial = 0
            x2partial = 0
            ypartial = 0
            y2partial = 0
            xdiff = 0
            ydiff = 0
            #Compute the first order partial derivatives in the x and y directions
            for z in range(0,3):
                for t in range (-1,2):
                    x1partial = list[y+t][x-2+z]+list[y+t][x+z] - 2. * list[y+t][x-1+z]
                    y1partial = list[y-2+z][x+t]+list[y+z][x+t] - 2. * list[y-1+z][x+t]
                    x2partial = x2partial + x1partial
                    y2partial = y2partial + y1partial
                    t += 1
                xpartial = xpartial + x2partial
                ypartial = ypartial + y2partial
                z += 1
            xmean = xpartial/9.
            ymean = ypartial/9.
            xdiff = (list[y][x-1] + list[y][x+1] - 2. * list[y][x] - xmean)**2.
            ydiff = (list[y-1][x] + list[y+1][x] - 2. * list[y][x] - ymean)**2.
            quality_value = (sqrt(xdiff)+sqrt(ydiff))/9.
            quality_map[x-2][y-2] = quality_value
    return quality_map

