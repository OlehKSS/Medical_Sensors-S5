import numpy
from math import pi

#Find the polarity arrays from the binary image and residue map. Return two vectors S (positive polarity array vector) and U (negative polarity array vector)
def find_polarity_arrays(thresholded_image, residue_map):
    '''Function which gives 4 arrays of polarity (row-major order) for regions 0 and 1'''
    
    #Add occurences from the thresolded image (possible values 0,1) and residue map (possible values (-1,0,1)
    summed_im1 = numpy.ndarray.flatten(thresholded_image + residue_map) #want equal to 2 for +ve1, want equal to -1 for -ve0
    summed_im0 = numpy.ndarray.flatten(thresholded_image + (-1) * residue_map) #want equal to -1 for +ve0, want equal to 2 for -ve1
    
    #Find the occurrances in each matrix and write out their indexes (row-major order)
    positive_polarity_array_region1 = numpy.where(summed_im1 == 2)[0]
    negative_polarity_array_region0 = numpy.where(summed_im1 == -1)[0]
    positive_polarity_array_region0 = numpy.where(summed_im0 == -1)[0]
    negative_polarity_array_region1 = numpy.where(summed_im0 == 2)[0]
    
    S = [positive_polarity_array_region0, positive_polarity_array_region1]
    U = [negative_polarity_array_region0, negative_polarity_array_region1]
    
    return S, U

#Provide the swarm, number of particles in the swarm, the rows, columns of the image, P_local and S_coords (+ve polarity array coordinates)
def calculate_fitness(swarm,num_particles,rows,cols,P_local,S_coords):
    #Evaluate the fitness of every particle and save in P_fitness_array
    P_fitness_array = numpy.zeros((1,num_particles))
    U_fitness_array = numpy.zeros((1,num_particles))
    
    for k in range (0,num_particles):
        
        #Unravel indexes to coordinates in format 2 x #indices -> (i,j)
        U_coords = numpy.unravel_index(swarm[k],(rows,cols))
        P_coords = numpy.unravel_index(P_local[k],(rows,cols))
        
        #Find fitness of the kth particle
        fitnessP = 0
        fitnessU = 0
        for j in range (0,max_points):
            iteration_sumU = sqrt((S_coords[1][j]-U_coords[1][j])**2 + (S_coords[0][j]-U_coords[0][j])**2)
            iteration_sumP = sqrt((S_coords[1][j]-P_coords[1][j])**2 + (S_coords[0][j]-P_coords[0][j])**2)
            fitnessU = fitnessU + iteration_sumU
            fitnessP = fitnessP + iteration_sumP
        
        P_fitness_array[0,k] = fitnessP
        U_fitness_array[0,k] = fitnessU
                
        #Find P_local and Pg
        if fitnessU < fitnessP:
            P_local[k] = swarm[k]
        else:
            P_local[k] = P_local[k]
            
        Pg = numpy.amin(P_fitness_array) #global best position
    
    return P_local, P_fitness_array, Pg



