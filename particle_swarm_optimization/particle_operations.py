import numpy
from math import pi

def find_polarity_arrays(thresholded_image, residue_map, num_particles):
    '''Function which gives 4 arrays of polarity (row-major order) for regions 0 and 1'''
    
    #Add occurences from the thresolded image (possible values 0,1) and residue map (possible values (-1,0,1)
    summed_im1 = numpy.ndarray.flatten(thresholded_image + residue_map) #want equal to 2 for +ve1, want equal to -1 for-ve0
    summed_im0 = numpy.ndarray.flatten(thresholded_image + (-1) * residue_map) #want equal to 2 for -ve0, want equal to -1 for-ve1
    
    #Find the occurrances in each matrix and write out their indexes (row-major order)
    positive_polarity_array_region1 = numpy.where(summed_im1 == 2)[0]
    positive_polarity_array_region0 = numpy.where(summed_im1 == -1)[0]
    negative_polarity_array_region1 = numpy.where(summed_im0 == -1)[0]
    negative_polarity_array_region0 = numpy.where(summed_im0 == 2)[0]
    
    
    
    return S, U
    



