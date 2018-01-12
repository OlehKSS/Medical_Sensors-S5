import numpy
from math import sqrt

'''Use image data stored in data_img_decoded to create a quality map'''

def quality_map_second_order(list):
    '''Function which finds the second order quality value for each pixel to produce a matrix NxN'''
    #Define a black border around the edge of the list for the quality map
    list = numpy.pad(list, 2, 'constant', constant_values=0)
    imrange = len(list)
    quality_map = numpy.empty([imrange-4,imrange-4],dtype = float)
    for x in range(2,(imrange-2)):
        for y in range(2,(imrange-2)):
            xpartial = 0
            x2partial = 0
            ypartial = 0
            y2partial = 0
            xdiff = 0
            ydiff = 0
            #Compute the average second order derivative for each pixel in the 9x9 window
            # and then take this value and subtract the middle pixel from it, following
            # the given quality map formula.
            for z in range(0,3):
                for t in range (-1,2):
                    x1partial = list[y+t][x-2+z] + list[y+t][x+z] - 2. * list[y+t][x-1+z]
                    y1partial = list[y-2+z][x+t] + list[y+z][x+t] - 2. * list[y-1+z][x+t]
                    x2partial = x2partial + x1partial
                    y2partial = y2partial + y1partial
                xpartial = xpartial + x2partial
                ypartial = ypartial + y2partial
            xmean = xpartial/9.
            ymean = ypartial/9.
            xdiff = (list[y][x-1] + list[y][x+1] - 2. * list[y][x] - xmean)**2.
            ydiff = (list[y-1][x] + list[y+1][x] - 2. * list[y][x] - ymean)**2.
            quality_value = (sqrt(xdiff)+sqrt(ydiff))/9.
            quality_map[y-2][x-2] = quality_value
    return quality_map

