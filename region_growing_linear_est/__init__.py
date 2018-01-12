'''
This module unwraps phase images using region growing and local linear estimation.
'''
from collections import deque
from math import floor
from numpy import zeros
#import numpy as np
from matplotlib import pyplot as plt
from region_growing_linear_est.linear_regression import linear_reg
from region_growing_linear_est.quality_maps import quality_map_second_order
from _shared.phase_image import PhaseImage

def unwrap(phase_img, window_size = 7):
    '''This function unwraps provided phase image.

    Args:
        phase_img (PhaseImage): n by n array of pixels that represents wrapped phase.
        window_size (int): window size for unrapping. Default is 7

    Returns:
        PhaseImage: phase image with unwrapped data.   
    '''

    #number of stacks
    n_stack = 5
    stacks = []
    rows, cols = phase_img.shape

    #calculate quality map
    phase_img.read()

    print('Calculating quality map...')
    qm2 = quality_map_second_order(phase_img.phase_data)

    qmap_max = qm2.max()
    qmap_min = qm2.min()

    #step for distributing pixels in stacks
    qstep = (qmap_max - qmap_min) / n_stack

    #creating stacks for holding pixels
    for i in range(n_stack):
        stacks.append(deque())

    checked_pixels =  zeros(phase_img.shape)
    visited_pixels =  zeros(phase_img.shape)

    unwrapped_phase_img = zeros(phase_img.shape)
    pixels_unwrapped = 0
    percent_unwrapped = 0

    #selecting initial seed
    #by reducing image size by 40% I try to omit noisy borders
    for i in range(round(0.45*rows), round(0.6*rows)):
        for j in range(round(0.45*cols), round(0.6*cols)):
            if (qm2[i, j] <= qstep) and (checked_pixels[i, j] != 1):
                seed = (i, j)
                #I will skip seed adding here,since I will do population with neighbors here
                #stacks[0].append(seed)
                #initial seed phase is taken as it is
                checked_pixels[i, j] = 1
                visited_pixels[i, j] = 1
                unwrapped_phase_img[i, j] = phase_img.get_phase_of_pxl(i, j)
                pixels_unwrapped = pixels_unwrapped + 1
                #adding seed neighbors
                neigbors = get_4neighbors(seed, visited_pixels)
                push_pixels_to_stacks(neigbors, stacks, qm2, qstep)
                break

        #we need only one pixel as a seed
        if (len(stacks[0]) != 0):
            break

    #selecting first non-zero stack and seed pixel, getting his neighbors
    is_stacks_empty = False

    while (not is_stacks_empty):
        for stack in stacks:
            #finds first not empty stack and do phase uwrapping
            if (len(stack) != 0):
                temp_seed = stack.popleft()

                neigbors = get_4neighbors(temp_seed, visited_pixels)

                if (len(neigbors) != 0):
                    push_pixels_to_stacks(neigbors, stacks, qm2, qstep)
                
                unwr_val = linear_reg(phase_img.phase_data,\
                    unwrapped_phase_img,\
                    checked_pixels,\
                    temp_seed,\
                    window_size)

                checked_pixels[temp_seed[0], temp_seed[1]] = 1
                unwrapped_phase_img[temp_seed[0], temp_seed[1]] = unwr_val

                #printing information about the progress
                pixels_unwrapped = pixels_unwrapped + 1
                temp_percent = int((pixels_unwrapped / unwrapped_phase_img.size) * 100)

                if (abs(percent_unwrapped - temp_percent) > 5):
                    percent_unwrapped = temp_percent
                    print('Unwrapped {}%'.format(percent_unwrapped))
                #after unwrapping done we will perform new search through stacks    
                break 
        #checking whether there is any not empty stack
        for stack in stacks:
            if (len(stack) != 0):
                #stacks not empty, go on with unwrapping
                is_stacks_empty = False
                break
            else:         
                is_stacks_empty = True

    return PhaseImage.from_phase_data(unwrapped_phase_img)


def push_pixels_to_stacks(pixels, stacks, quality_map, quality_step):
    '''The function places pixel in one of the stacks depending on the corresponding quality value.

    Args:
        pixels ((int,int)): coordinates of the pixels to be pushed into corresponding stacks.
        stacks (list(deque)): list of stacks.
        quality_map (numpy.array(x,y)): quality map.
        quality_step (float): upper limit of quality value, the lower the better.

    Returns:
        None.    
    '''
    for pixel_coords in pixels:
        temp_pixel_row, temp_pixel_col = pixel_coords
        #finding stack index for pixel to be pushed in
        pixel_quality = quality_map[temp_pixel_row, temp_pixel_col]
        index = abs(floor(pixel_quality/quality_step))
        
        if (index < len(stacks)):
            stacks[index].append(pixel_coords)

        elif (index >= len(stacks)):
            #case when we get to the highest value in range
            stacks[index - 1].append(pixel_coords)


def get_4neighbors(pixel, visited_pixels_map):
    '''The function selects 4 unvisited neigbors of provided seed pixel in 4-neighborhood.
    Selected pixels will be marked as visited.

    Args:
        pixel (int, int): coordinates of the pixel in format (row, column).
        visited_pixels_map (numpy.array(x,y)): map of pixels, 1 - pixel was visited, 
            0 - pixel wasn't visited.

    Return:
        list((int, int)): list of selected neighbors.
    '''
    img_rows, img_cols = visited_pixels_map.shape
    pixel_row, pixel_col = pixel
    neighbors = []

    for i in (-1, 0, 1):
        temp_row = pixel_row + i
        #checking image boundaries
        if (temp_row <= 0) or (temp_row >= img_rows):
            continue

        if (i == 0) :
            #checking neighbors in neaby columns    
            for j in (-1, 1):
                temp_col = pixel_col + j
                #checking image boundaries
                if (temp_col <= 0) or (temp_col >= img_cols):
                    continue

                #check whether this pixel wasn't visited and a push it to neighbors
                if (visited_pixels_map[temp_row, temp_col] != 1):
                    neighbors.append((temp_row, temp_col))
                    visited_pixels_map[temp_row, temp_col] = 1

        else:
            #checking neighbors in neaby rows
            temp_col = pixel_col

            #check whether this pixel wasn't visited and a push it to neighbors
            if (visited_pixels_map[temp_row, temp_col] != 1):
                neighbors.append((temp_row, temp_col))
                visited_pixels_map[temp_row, temp_col] = 1            

    return neighbors

