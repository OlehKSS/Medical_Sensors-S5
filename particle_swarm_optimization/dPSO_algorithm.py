import numpy
from math import pi
from math import sqrt
from particle_swarm_optimization.find_residues import calculate_residues
from particle_swarm_optimization.particle_initialization import phase_derivative_variance, threshold
from particle_swarm_optimization.particle_operations import find_polarity_arrays, calculate_fitness

def adjustment_operator (input_array,k,l):
    '''Function which deletes the element in the kth position and inserts it in the lth postion'''
    if k == l:
        return input_array
    else:
        temp = input_array[k-1]
        output_array = numpy.delete(input_array,k-1)
        output_array = numpy.insert(output_array,l-1,temp)
    return output_array

#Definition 3, AS plus AS, which constructs a longer AS
def AS_plus_AS (AS1, AS2):
    [rows1,cols1,AO] = numpy.shape(AS1)
    [rows2,cols2,AO] = numpy.shape(AS2)
    new_cols = cols1 + cols2
    AS = numpy.zeros((rows1,new_cols,2))
    AS[:,0:cols1,:] = AS1
    AS[:,cols1:new_cols,:] = AS2
    return AS

#Defintion 4, array minus array, which contructs an AS
def array_minus_array (W, R):
    [num_particles,N1] = numpy.shape(W)
    AS = numpy.zeros((num_particles,N1,2))
    for i in range (0, num_particles):
        num_AO = 0
        temp_particle1 =  W[i,:]
        temp_particle2 =  R[i,:]
        for j in range (0, N1):
            if temp_particle1[j] != temp_particle2[j]:
                index2 = j
                value = temp_particle1[j]
                for k in range (j+1,N1):
                    if value == temp_particle2[k]:
                        index1 = k
                        AS[i,num_AO,0] = index1+1
                        AS[i,num_AO,1] = index2+1
                        temp_particle2 = adjustment_operator(temp_particle2,index1+1,index2+1)
                        j = 0
                        num_AO = num_AO + 1
                        break
            elif j == N1-1:
                break
    return AS

#Defintion 6, a number multiplying AS, producing a shorter AS
def num_times_AS (num, AS):
    if num < 1:
        [rows,cols,AO] = numpy.shape(AS)
        threshold = int(num * cols)
        AS = AS[:,0:threshold,:]
        return AS
    else:
        return AS

#Defintion 7, an array plus AS, acting the AOs on the array, producing an array
def array_plus_AS (array, AS):
    [num_particles,N1] = numpy.shape(array)
    [rows,cols,AO] = numpy.shape(AS)
    #AOs act on the each particle
    for i in range (0,num_particles):
        particle_temp = array[i,:]
        for j in range (0,cols):
            index1 = AS[i,j,0]
            index2 = AS[i,j,1]
            particle_temp = adjustment_operator(particle_temp,index1,index2)
        array[i,:] = particle_temp
    return array

                      
#Provide the original image, number of particles, maximal iteration times, learning factor 1 and learning factor 2
def find_best_match_by_dPSO(image, num_particles, T, c1, c2):
    '''Function which performs the dPSO on an image given the image, number of required parameters, T (maximal iteration times), c1 (learning factor 1), c2 (learning factor 2) and returns the best match in each region'''
    
    [rows,cols] = numpy.shape(image)
    
    #Calculate the phasemap and residue map to segment the image
    print("Initializing paramters for dPSO")
    phasemap = phase_derivative_variance(image)
    thresholded_im = threshold(phasemap)
    residue_map = calculate_residues(image)
    [regions_S, regions_U] = find_polarity_arrays(thresholded_im, residue_map)
    print("Parameters initialized")
    #Variable to output best positions
    global_best_positions = [numpy.zeros_like(regions_U[0]),numpy.zeros_like(regions_U[1])]
    
    #Calculations for the hth group of residues
    for h in range (0,2):
        
        print('Calculations for the {}th group of residues'.format(h))
        #Get S and U
        S = regions_S[h]
        U = regions_U[h]
        
        #Constants
        M1 = len(S) #length of S
        N1 = len(U) #length of U
        max_points = min(M1,N1)
        
        #Initialize the swarm by randomly shuffling U the numnber of particles times
        swarm = numpy.zeros((num_particles,N1))
        swarm[0,:] = U
        for i in range (1,num_particles):
            numpy.random.shuffle(U)
            swarm[i,:] = U
        swarm = swarm.astype(int)
        
        #For each particle, initialize the random velocity
        V = (N1) * numpy.random.rand(num_particles,N1,2) + 1
        V = V.astype(int)
        
        t = 1   #number of iterations

        #Initialize P_local as the swarm
        P_local = numpy.array(swarm)
        #Unravel indexes to coordinates in format 2 x #indices -> (i,j)
        S_coords = numpy.unravel_index(S,(rows,cols))    #remains fixed
        lowest_fitness = 1000
        termination_cond = 0
        print('Determining minimal indexes in negative polarity array...'.format(t))
        while t < T and termination_cond < 50:
            
            #Evaluate the fitness of every particle and save in P_fitness_array
            P_fitness_array = numpy.zeros((num_particles,1))

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
        
                P_fitness_array[k,0] = fitnessP
                
                #Find P_local for each particle
                if fitnessU < fitnessP:
                    P_local[k] = swarm[k]
        
            #Find global best position
            Pg_temp = numpy.argmin(P_fitness_array)
            Pg = numpy.copy(P_local[Pg_temp])
            if (P_fitness_array[Pg_temp] < lowest_fitness):
                lowest_fitness = P_fitness_array[Pg_temp]
                termination_cond = 0
            elif(P_fitness_array[Pg_temp] == lowest_fitness):
                termination_cond = termination_cond + 1     #terminate if there are 50 repitions of the same fitness value

            #print('Pg = {}'.format(Pg))
            #print('lowest fitness = {}'.format(lowest_fitness))
            
            w = 0.9 - 0.5*(t/T)     #inertial weight
    
            t = t + 1   #increment the iterations
            
            Pg_for_V = numpy.tile(Pg,(num_particles,1)) #to compare with every particle
            
            #Find a new V
            V1 = num_times_AS(w,V)
            V2 = num_times_AS((c1 * numpy.random.rand(1)), array_minus_array(P_local,swarm))
            V3 = num_times_AS((c2 * numpy.random.rand(1)), array_minus_array(Pg_for_V,swarm))
            new_V = AS_plus_AS(AS_plus_AS(V1,V2), V3)
            V = new_V.astype(int)

            #Find a new U
            swarm = array_plus_AS(swarm,V)
        
        print('iterations = {}'.format(t))
        global_best_positions[h] = Pg
    print('Positive polarity array region 0 = {}'.format(regions_S[0]))
    print('Original Negative polarity array region 0 = {}'.format(regions_U[0]))
    print('New global best positions region 0 = {}'.format(global_best_positions[0]))

    print('Positive polarity array region 1 = {}'.format(regions_S[1]))
    print('Original Negative polarity array region 1 = {}'.format(regions_U[1]))
    print('New global best positions region 1 = {}'.format(global_best_positions[1]))

    return [regions_S, regions_U, global_best_positions]









