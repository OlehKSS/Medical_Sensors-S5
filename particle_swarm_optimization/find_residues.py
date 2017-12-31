import numpy
from math import pi

def calculate_residues(image):
    '''Function which calculates the residue map using a 2x2 window on an image'''
    
    #Convert image to float
    image = numpy.array(image) + 0.

    #Convert the image to a wrapped image with values between -pi and pi
    length = numpy.max(image) - numpy.min(image)
    image = (image - (length/2.))/(length/2.)*pi

    #Pad the image with zeros for residue calulation
    #image = numpy.pad(image, 1, 'constant', constant_values=0.)
    [rows,cols] = numpy.shape(image)
    
    #Calculate the residues for each point following formula (1) in He paper
    IM_active=image;
    IM_below=numpy.zeros([rows,cols],dtype = float)
    IM_right=numpy.zeros([rows,cols],dtype = float)
    IM_belowright=numpy.zeros([rows,cols],dtype = float)
    
    IM_below[0:rows-2,:] = image[1:rows-1,:]
    IM_right[:,0:cols-2] = image[:,1:cols-1]
    IM_belowright[0:rows-2,0:cols-2] = image[1:rows-1,1:cols-1]
    
    res1 = ((IM_active - IM_below + pi) % (2*pi)) - pi
    res2 = ((IM_below - IM_belowright + pi) %  (2*pi)) - pi
    res3 = ((IM_belowright - IM_right + pi) %  (2*pi)) - pi
    res4 = ((IM_right - IM_active + pi) %  (2*pi)) - pi
    
    temp_residues = res1 + res2 + res3 + res4
    
    residues = (temp_residues >= 6)*1
    residues = residues - (temp_residues<=-6)*1;
    residues[:,cols-1] = 0
    residues[rows-1,:] = 0
    residues[:,0] = 0
    residues[0,:] = 0
    
    residue_map = residues;

    return residue_map
    



