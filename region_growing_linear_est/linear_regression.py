import numpy
from math import sqrt
from math import pi

'''Unwrap the phase using the linear regression prediction'''

#Define a linear model unwr_im = X_unwr * B + E where unwr_im and X_unwr are given and B and E are calculated. Provide the binary checked image (indicating which pixels have been unwrapped (0 wrapped, 1 unwrapped), the unwrapped phase image (unwr_im), the original image data (wr_im), the coordinate to unwrap (point(i,j)), and the window_size. It returns the unwrapped phase prediction.

def linear_reg(checked_binary_im, unwr_im, wr_im, point, window_size):
    
    #Find X_unwr (window over original data) from the unwrapped phase data, the coordinate
    #to unwrap and window size
    low_range = int((window_size-1)/2)
    high_range = int((window_size+1)/2)
    
    #Pad the three arrays with size equal to high_range
    checked_binary_im = numpy.pad(checked_binary_im, high_range, 'constant', constant_values = 0)
    unwr_im = numpy.pad(unwr_im, high_range, 'constant', constant_values = 0)
    wr_im = numpy.pad(wr_im, high_range, 'constant', constant_values = 0)
    
    #Windows of original and unwrapped data size window_size x window_size
    X_unwr = wr_im[point[0]-low_range+high_range:point[0]+2*high_range,point[1]-low_range+high_range:point[1]+2*high_range]
    unwr_im = unwr_im[point[0]-low_range+high_range:point[0]+2*high_range,point[1]-low_range+high_range:point[1]+2*high_range]
    checked_binary_im = checked_binary_im[point[0]-low_range+high_range:point[0]+2*high_range,point[1]-low_range+high_range:point[1]+2*high_range]
    
    #Create a list of indicies in phi_unwr that have been unwrapped
    checked_binary_im = numpy.ndarray.flatten(checked_binary_im)
    X_unwr = numpy.ndarray.flatten(X_unwr)
    unwr_im = numpy.ndarray.flatten(unwr_im)
    unwr_indicies = numpy.where(numpy.ndarray.flatten(checked_binary_im) != 0)[0]
    
    #Get values of the wrapped and unwrapped phase, put into arrays called phi_unwr and X
    X = numpy.empty((1,len(unwr_indicies)))
    phi_unwr = numpy.empty((1,len(unwr_indicies)))
    for i in range (0,len(unwr_indicies)):
        phi_unwr[i] = unwr_im[unwr_indicies[i]]
        X[i] = X_unwr[unwr_indicies[i]]
                  
    #Find B, E, rank, and singular values of X
    [B, E, rank, s] = numpy.linalg.lstsq(X,phi_unwr)
                  
    #Estimate the value of phi using the least squares equation
    point_val = wr_im[point[0]+high_range][point[1]+high_range]
    phi_est = point_val*B
    
    #Set the value of phi according to the original image data
    phi = wr_im[point[0]+high_range][point[1]+high_range]
                  
    #Calculate the unwrapped phase using ***insert forumula***
    unwr_phase = phi + 2 * pi * int((phi_est - phi)/(2 * pi))
    
    return unwr_phase



