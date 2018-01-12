import os, sys
import numpy
from matplotlib import pylab, pyplot, cm
from scipy import signal
from skimage import io
from _shared.phase_image import PhaseImage
from skimage import filters
#from region_growing_linear_est.quality_maps import quality_map_second_order
from math import sqrt
#from region_growing_linear_est.linear_regression import linear_reg
from particle_swarm_optimization.particle_initialization import phase_derivative_variance, threshold
from particle_swarm_optimization.particle_operations import find_polarity_arrays
from particle_swarm_optimization.find_residues import calculate_residues

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


#W = [1,4,3,2,5]
#R = [1,5,4,2,3]
#W = numpy.array(W)
#R = numpy.array(R)
#W = W.reshape(1,5)
#R = R.reshape(1,5)

#AS = array_minus_array(W,R)

#newW = array_plus_AS(R,AS)
#print(newW)

image = io.imread('test_heart_image.jpg',as_grey = True)
phasemap = phase_derivative_variance(image)
thresholded_im = threshold(phasemap)
residue_map = calculate_residues(image)
[regions_S, regions_U] = find_polarity_arrays(thresholded_im, residue_map)

[rows,cols] = numpy.shape(image)

#Set values to parameters of dPSO
T = 1000    #maximal iteration times
c1 = 2      #learning factor 1
c2 = 2      #learning factor 2
num_particles = 300

S = regions_S[0]
U = regions_U[0]

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

#For each particle, initialize the random velocity in the range (1,len(U1))
V = (N1) * numpy.random.rand(num_particles,N1,2) + 1
V = V.astype(int)

t = 1   #number of iterations
#Pg = numpy.zeros((1,N1))
#Pg_old = numpy.ones((1,N1))
#stopping_condition = numpy.ones((1,N1))

#Initialize P_local as the swarm
P_local = numpy.copy(swarm)
#Unravel indexes to coordinates in format 2 x #indices -> (i,j)
S_coords = numpy.unravel_index(S,(rows,cols))    #remains fixed
lowest_fitness = 1000
termination_cond = 0

while t < T and termination_cond < 50:
    print('iterations = {}'.format(t))
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
        termination_cond = termination_cond + 1

    print('Pg = {}'.format(Pg))
    print('lowest fitness = {}'.format(lowest_fitness))
            
    w = 0.9 - 0.5*(t/T)     #inertial weight
            
    t = t + 1   #increment the iterations
            
    Pg_for_V = numpy.tile(Pg,(num_particles,1)) #to compare with every particle

    #Find a new V
    V1 = num_times_AS(w,V)
    V2 = num_times_AS((c1 * numpy.random.rand(1)), array_minus_array(P_local,swarm))
    V3 = num_times_AS((c2 * numpy.random.rand(1)), array_minus_array(Pg_for_V,swarm))
    new_V = AS_plus_AS(AS_plus_AS(V1,V2), V3)
    V = new_V.astype(int)
            
    #Find a new swarm
    swarm = array_plus_AS(swarm,V)
