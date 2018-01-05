import numpy
from math import sqrt
from math import pi

'''Unwrap the phase using the linear regression prediction'''

#Define a linear model phi_unwr = X_unwr * B + E where
#phi_unwr is given and X_unwr, B, and E are calculated
#Provide the unwrapped unwrapped phase data (phi_unwr), the
#original image data, the coordinate to unwrap (point(i,j)),
#and the window_size. It returns the unwrapped phase prediction.

#Initialize phi_unwr_data with some values not in the phi_unwr_data set (100 or something like that. Change value in line 32 if necessary)
def linear_reg(phi_unwr_data, original_im_data, point, window_size):
    
    #Find X_unwr (window over original data) from the unwrapped phase data, the coordinate
    #to unwrap and window size
    #[rows,cols] = numpy.shape(phi_unwr)
    low_range = int((window_size-1)/2)
    high_range = int((window_size+1)/2)
    
    #Pad both arrays equal to high_range
    phi_unwr_data = numpy.pad(phi_unwr_data, high_range, 'constant', constant_values = 100)
    original_im_data = numpy.pad(original_im_data, high_range, 'constant', constant_values = 0)
    
    #Windows of original and unwrapped data size window_size x window_size
    X_unwr = original_im_data[point[0]-low_range+high_range:point[0]+2*high_range,point[1]-low_range+high_range:point[1]+2*high_range]
    phi_unwr_data = phi_unwr_data[point[0]-low_range+high_range:point[0]+2*high_range,point[1]-low_range+high_range:point[1]+2*high_range]
    
    #Create a list of indicies in phi_unwr that have been unwrapped
    phi_unwr_data = numpy.ndarray.flatten(phi_unwr_data)
    X_unwr = numpy.ndarray.flatten(X_unwr)
    unwr_indicies = numpy.where(numpy.ndarray.flatten(phi_unwr_data) != 100)[0]
    
    #Get values of the wrapped and unwrapped phase, put into arrays called phi_unwr and X
    phi_unwr = numpy.empty(1,len(unwr_indicies))
    X = numpy.empty(1,len(unwr_indicies))
    for i in range (0,len(unwr_indicies)):
        phi_unwr[i] = phi_unwr_data[unwr_indicies[i]]
        X[i] = X_unwr[unwr_indicies[i]]
                  
    #Find B, E, rank, and singular values of X
    [B, E, rank, s] = numpy.linalg.lstsq(X,phi_unwr)
                  
    #Estimate the value of phi using the least squares equation
    point_val = original_im_data[point[0]+high_range][point[1]+high_range]
    phi_est = numpy.matmul(point_val,B)
    
    #Set the value of phi according to the original image data
    phi = original_im_data[point[0],point[1]]
                  
    #Calculate the unwrapped phase using ***insert forumula***
    unwr_phase = phi + 2 * pi * int((phi_est - phi)/(2 * pi))
    
    return unwr_phase



