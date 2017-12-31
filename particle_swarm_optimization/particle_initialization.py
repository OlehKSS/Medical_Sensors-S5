import numpy
from math import sqrt
from scipy import signal
from skimage import filters

def phase_derivative_variance(list):
    '''Function which finds the phase derivative variance for each pixel to produce a matrix NxN'''
    
    imrange = len(list)
    phase_derivative_map = numpy.empty([imrange,imrange],dtype = float)
    list = numpy.array(list) + 0. #Convert to float
    
    #Define filters in x, y, and mean value
    Gx = [[-1.,0.,1.],[-2.,0.,2.],[-1.,0.,1.]]
    Gy = [[-1.,-2.,-1.],[0.,0.,0.],[1.,2.,1.]]
    mean = [[1./9.,1./9.,1./9.],[1./9.,1./9.,1./9.],[1./9.,1./9.,1./9.]]
    
    #Find maps of horizontal and vertical derivative, default pads boundaries with 0
    xderv = signal.convolve2d(Gx,list)
    yderv = signal.convolve2d(Gy,list)
    
    #Find map of means, default pads boundaries with 0
    xmean = signal.convolve2d(mean,xderv)
    ymean = signal. convolve2d(mean,yderv)
    
    #Pad xderv and yderv with 0 to avoid problems with edge derivatives
    xderv = numpy.pad(xderv, 1, 'constant', constant_values=0.)
    yderv = numpy.pad(yderv, 1, 'constant', constant_values=0.)

    #Apply the first order derivative formula
    for x in range(2,imrange+2):
        for y in range(2,imrange+2):
            xdiff0 = 0.
            xdiff = 0.
            ydiff0 = 0.
            ydiff = 0.
            for z in range(-1,2):
                for t in range (-1,2):
                    xdiff0 = (xderv[y+z][x+t] - xmean[y][x])**2.
                    xdiff = xdiff + xdiff0
                    ydiff0 = (yderv[y+z][x+t] - ymean[y][x])**2.
                    ydiff = ydiff + ydiff0
            phase_derivative_value = (sqrt(xdiff)+sqrt(ydiff))/9.
            phase_derivative_map[y-2][x-2] = phase_derivative_value
    return phase_derivative_map



def threshold(phase_derivative_map):
    '''Function which creates a binary image from the phase derivative map NxN'''
    
    #Apply otsu threshold to the image
    thresh = filters.threshold_otsu(phase_derivative_map)
    thresholded_image = phase_derivative_map > thresh

    return thresholded_image

def find_polarity_arrays(thresholded_image, residue_map):
    '''Function which gives 4 arrays of polarity (row-major order) for regions 0 and 1'''
    
    #Add occurences from the thresolded image (possible values 0,1) and residue map (possible values (-1,0,1)
    summed_im1 = numpy.ndarray.flatten(thresholded_image + residue_map) #want equal to 2 for +ve1, want equal to -1 for-ve0
    summed_im0 = numpy.ndarray.flatten(thresholded_image + (-1) * residue_map) #want equal to 2 for -ve0, want equal to -1 for-ve1
    
    #Find the occurrances in each matrix and write out their indexes (row-major order)
    positive_polarity_array_region1 = numpy.where(summed_im1 == 2)[0]
    positive_polarity_array_region0 = numpy.where(summed_im1 == -1)[0]
    negative_polarity_array_region1 = numpy.where(summed_im0 == -1)[0]
    negative_polarity_array_region0 = numpy.where(summed_im0 == 2)[0]
    
    return positive_polarity_array_region1, positive_polarity_array_region0,negative_polarity_array_region1, negative_polarity_array_region0
















