import numpy
from math import sqrt, pi

#Initialize phi_unwr_data with some values not in the phi_unwr_data set 
#(100 or something like that. Change value in line 32 if necessary)
def linear_reg(wrapped_img, unwpd_img, checked_pxls_map, point, window_size=7):    
    '''Unwrap the phase using the linear regression prediction. It defines a linear model 
    phi_unwr_data = x_unwr * B + E, where phi_unwr_data is given and x_unwr, B, and E are calculated.

    Args:
        wrapped_img (numpy.array(int, int)): original image data.
        unwpd_img (numpy.array(int, int)): the unwrapped phase data.
        checked_pxls_map (numpy.array(int, int)): map of pixels that were unwrapped.
        point (int, int): the coordinate of pixel to unwrap.
        window_size (:obj:`int`, optional): window size. Default value is 7.

    Returns:
        (int): the unwrapped phase prediction.
    '''
    
    #Find x_unwr (window over original data) from the unwrapped phase data, the coordinate
    #to unwrap and window size
    low_range = int((window_size-1)/2)
    high_range = int((window_size+1)/2)
    point_new_coords = (low_range, low_range)
    #window around the point we want to unwrap in image coordinates
    window_low_row = point[0]-low_range+high_range
    window_high_row = point[0]+2*high_range
    window_low_col = point[1]-low_range+high_range
    window_high_col = point[1]+2*high_range
    
    #Pad the three arrays with size equal to high_range
    checked_pxls_map = numpy.pad(checked_pxls_map, high_range, 'constant', constant_values = 0)
    unwpd_img = numpy.pad(unwpd_img, high_range, 'constant', constant_values = 0)

    #Windows of original and unwrapped data size window_size x window_size
    unwpd_img = unwpd_img[window_low_row : window_high_row, window_low_col : window_high_col]
    checked_pxls_map = checked_pxls_map[window_low_row : window_high_row,\
    window_low_col : window_high_col]
    
    #Create a list of indicies in phi_unwr that have been unwrapped
    checked_pxls_map_flat = numpy.ndarray.flatten(checked_pxls_map)
    unwr_indicies = numpy.where(checked_pxls_map_flat != 0)[0]
    unwpd_img_flat = numpy.ndarray.flatten(unwpd_img)


    #window coords [0, 1][2, 3]
    
    #Get values of the wrapped and unwrapped phase, put into array called phi_unwr 
    #unwpd_pxls_coords = numpy.empty((2,len(unwr_indicies)))
    unwpd_pxls_coords = numpy.transpose(numpy.unravel_index(unwr_indicies, unwpd_img.shape))
    phi_unwr = numpy.empty((len(unwr_indicies), 1))

    for i, unwr_index in enumerate(unwr_indicies):
        phi_unwr[i, 0] = unwpd_img_flat[unwr_index]
                  
    #Find B, E, rank, and singular values of unwpd_pxls_coords
    [B, E, rank, s] = numpy.linalg.lstsq(unwpd_pxls_coords,phi_unwr)
                  
    #Estimate the value of phi using the least squares equation
    phi_est = float(numpy.dot(point_new_coords, B))
    
    #Set the value of phi according to the original image data
    phi = wrapped_img[point[0]][point[1]]
                  
    #Calculate the unwrapped phase using paper formula
    unwr_phase = phi + 2 * pi * round((phi_est - phi)/(2 * pi))
    
    return unwr_phase
