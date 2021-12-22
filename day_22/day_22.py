# -*- coding: utf-8 -*-
import time
import numpy as np
from itertools import permutations

def read_input(path_to_file:str = 'input/raw_input.txt') -> str:
    with open(path_to_file) as f:
        data = [lines.strip('\n') for lines in f.readlines()]
    return data


def part1(data, threshold = 50):
    # create a cube
    reboot_steps = [coord.split(',') for coord in data]
    max_x = 0
    max_y = 0
    max_z = 0
    min_x = 0
    min_y = 0
    min_z = 0
    # read the input and create a dict
    command_dict = {}
    for reboot_step in reboot_steps:
        line = reboot_steps.index(reboot_step)
        command = reboot_step[0].split(' ')[0]
        x_range = [int(x) for x in reboot_step[0].split('=')[1].split('..')]
        y_range = [int(y) for y in reboot_step[1].split('=')[1].split('..')]
        z_range = [int(z) for z in reboot_step[2].split('=')[1].split('..')]        
        if (threshold >= max(x_range) and threshold >= max(y_range) and threshold >= max(z_range)) and (-threshold <= min(x_range) and -threshold <= min(y_range) and -threshold <= min(z_range)):
            max_x = max(x_range) if min(x_range) > max_x else max_x
            max_y = max(y_range) if min(y_range) > max_y else max_y
            max_z = max(z_range) if min(z_range) > max_z else max_z
            min_x = min(x_range) if min(x_range) < min_x else min_x
            min_y = min(y_range) if min(y_range) < min_y else min_y
            min_z = min(z_range) if min(z_range) < min_z else min_z
            cuboids = (command, set((x,y,z) for x in range(x_range[0], x_range[1]+1)
                        for y in range(y_range[0], y_range[1]+1)
                        for z in range(z_range[0], z_range[1]+1)))
            command_dict[line] = cuboids
            
    # create the cuboids on and off (z,y,x)
    mat_x = threshold*2
    mat_y = threshold*2
    mat_z = threshold*2
    cuboid_matrix = np.zeros(shape=(mat_z+1, mat_y+1, mat_x+1), dtype=int)
    #print(cuboid_matrix.shape)

    for _, line in command_dict.items():
        command = line[0]
        for cube in line[1]:
            # recalculate coordinates:
            x = cube[0] + threshold
            y = cube[1] + threshold
            z = cube[2] + threshold
            cuboid_matrix[z, y, x] = 1 if command == 'on' else 0
    
    #print(cuboid_matrix)
    #print((cuboid_matrix==1).sum())
    return (cuboid_matrix==1).sum()


def part2(data):    
    return 0

def test():
    data = read_input(path_to_file='input/test_input.txt')
    
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    
    '''

if __name__ == '__main__':
    data  = read_input()
    test()    
    start_time = time.perf_counter()
    print('\nResult for part 1:', part1(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(enh, img))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''