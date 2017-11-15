import numpy
from math import sqrt

'''Unwrap the phase using the linear regression prediction'''

def linear_reg(X, point, img_data):
    
    #Define a linear model phi_unwr = X_unwr * B + E where
    #phi_unwr and X_unwr are given and B and E are calculated
    X = numpy.pad(X, [(0,0),(1,0)], mode = 'constant', constant_values = 1)
    phi_unwr = {img_data[X[0][2]][X[0][1]], img_data[X[1][2]][X[1][1]], img_data[X[2][2]][X[2][1]]}
                  
    #Find B, E, rank, and singular values of X
    [B, E, rank, s] = numpy.linalg.lstsq(X,phi_unwr)
                  
    #Estimate the value of phi using the least squares equation
    point = numpy.pad(point, [(0,0),(1,0)], mode = 'constant', constant_values = 1)
    phi_est = numpy.matmul(point,B)
    
    #Set the value of phi according to the original image data
    phi = img_data[point[2]][point[1]]
                  
    #Calculate the unwrapped phase using ***insert forumula***
    unwr_phase = phi + 2 * pi * int((phi_est - phi)/(2 * pi))
    
    return unwr_phase, B

def calc_unwr_phase(point, B, img_data):
    
    #Estimate the value of phi using the least squares equation
    point = numpy.pad(point, [(0,0),(1,0)], mode = 'constant', constant_values = 1)
    phi_est = numpy.matmul(point,B)
    
    #Set the value of phi according to the original image data
    phi = img_data[point[2]][point[1]]
    
    #Calculate the unwrapped phase using ***insert forumula***
    unwr_phase = phi + 2 * pi * int((phi_est - phi)/(2 * pi))
    
    return unwr_phase



