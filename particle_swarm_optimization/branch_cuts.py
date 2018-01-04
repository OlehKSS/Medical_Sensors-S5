import numpy
from math import sqrt

def place_branch_cuts(image, S, Pg):
    '''Function which creates a binary branch image from the positive and reordered negative residue arrays'''
    num_particles = len(S)
    [rows,cols] = numpy.shape(image)
    
    branch_cuts = numpy.zeros((rows,cols))  #Define size of branch cut image
    
    for h in range (0,num_particles):
        unraveled_coordsS = numpy.unravel_index(S[h],(rows,cols))
        unraveled_coordsPg = numpy.unravel_index(Pg[h],(rows,cols))
        M1 = len(S[h])
        N1 = len(U[h])
        max_points = min(M1,N1)
        for j in range (0,max_points):
            unraveled_coordsS = numpy.unravel_index(S[h],(rows,cols))
            unraveled_coordsPg = numpy.unravel_index(Pg[h],(rows,cols))
    
    
    return branch_cuts
















