import numpy
from math import pi
from math import sqrt
from find_residues import calculate_residues
from particle_initalization import phase_derivative_variance, threshold
from particle_operations import find_polarity_arrays

def adjustment_operator (input_array,k,l):
    '''Function which deletes the element in the kth position and inserts it in the lth postion'''
    temp = input_array[k]
    output_array = numpy.delete(input_array,k)
    output_array = numpy.insert(output_array,l,temp)

    return output_array


#Provide the original image, positive_polarity_arrays, and negative_polarity_arrays respectively
def find_best_match_by_dPSO(image, num_particles, T, c1, c2):
    '''Function which performs the dPSO on an image given the image, number of required parameters, T (maximal iteration times), c1 (learning factor 1), c2 (learning factor 2) and returns the best match in each region'''
    [rows,cols] = numpy.shape(image)
    
    phasemap = phase_derivative_variance(image)
    thresholded_im = threshold(phasemap)
    [S, U] = find_polarity_arrays(thresholded_image, residue_map, num_particles)
    
    #Calculations for region 1
    for h in range (0,num_particles):
        #Unravel indexes to coordinates in format 2 x #indices -> (i,j)
        unraveled_coordsS = numpy.unravel_index(S[h],(rows,cols))    #remains fixed
        unraveled_coordsU = numpy.unravel_index(U[h],(rows,cols))
        
        t = 1   #number of iterations
        fitness = 10000
        stopping_condition = 1
        while t < T and fitness > stopping_condition:
            
            #For each particle, find the random velocity for U
            AS = ???
            #Apply AS to U
            
            
            #Determine the fitness
            M1 = len(S[h])
            N1 = len(U[h])
            max_points = min(M1,N1)
            fitnessU = 0
            fitnessP = 0
            unraveled_coordsP = numpy.unravel_index(P[h],(rows,cols))
            for j in range (0,max_points):
                iteration_sumU = sqrt((unraveled_coordsS[1][j]-unraveled_coordsU[1][j])**2 + (unraveled_coordsS[0][j]-unraveled_coordsU[0][j])**2)
                iteration_sumP = sqrt((unraveled_coordsS[1][j]-unraveled_coordsP[1][j])**2 + (unraveled_coordsS[0][j]-unraveled_coordsP[0][j])**2)
                fitnessU = fitnessU + iteration_sumU
                fitnessP = fitnessP + iteration_sumP

                #Find P_new and Pg
                if fitnessU > fitnessP:
                    P_new = U[h]
                else:
                    P_new = P[h]
                Pg[j] = numpy.argmin(fitnessP)
            
                w = 0.9 - 0.5*(t/T)     #inertial weight
    
    
            t = t + 1




    return branches









