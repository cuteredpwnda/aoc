# -*- coding: utf-8 -*-
import time
import numpy as np
from itertools import product

def read_input(path_to_file:str = 'input/raw_input.txt') -> str:
    """read_input Read the input

    Reads the input from a file with specified path

    Parameters
    ----------
    path_to_file : str, optional
        Path to the file to be read, by default 'input/raw_input.txt'

    Returns
    -------
    str
        The files content as string.
    """

    with open(path_to_file) as f:
        data = f.readlines()[0].strip('\n')
    return data

def read_test_res(path_to_file:str = 'input/test_result.txt'):
    with open(path_to_file) as f:
        data = f.readlines()[0].split('|')
    return data

# panic button
panic = 0

def part1(data:str)->int:
    data = data.split(':')[-1]
    data = data.split(',')
    x_range = [int(x) for x in data[0].split('=')[-1].split('..')]
    y_range = [int(x) for x in data[1].split('=')[-1].split('..')]

    # draw the target area
    max_x = max(x_range)
    min_x = min(x_range)
    max_y = max(y_range)
    min_y = min(y_range)
    print(max_x, min_x, max_y, min_y)

    velocities = {}
    
    for vel_x in range(0, max_x+1):
        for vel_y in range(max(abs(min_y), abs(max_y)), min_y-1, -1):
            new_x = 0
            new_y = 0
            curr_vel_x = vel_x
            curr_vel_y = vel_y
            # calc
            while ((new_x <= max_x+1) and (min_y-1 <= new_y)):
                new_x += curr_vel_x
                new_y += curr_vel_y
                
                curr_vel_x -= 1
                curr_vel_y -= 1
                
                if curr_vel_x <= 0:
                    curr_vel_x = 0
                
                # if target field is reached
                if ((min_x <= new_x <= max_x) and (min_y <= new_y <= max_y)):
                    velocities[(vel_x, vel_y)] = (vel_y * (vel_y+1))//2

    return max(velocities.values()), len(velocities.keys())

def part1_shitty(data:str)->int:
    global panic

    data = data.split(':')[-1]
    data = data.split(',')
    x_range = [int(x) for x in data[0].split('=')[-1].split('..')]
    y_range = [int(x) for x in data[1].split('=')[-1].split('..')]

    # draw the target area
    max_x = max(x_range)+1
    min_x = min(x_range)
    max_y = abs(min(y_range))+1
    min_y = abs(max(y_range))
    field = np.empty((max_y,max_x), dtype = str)
    field.fill('.')
    # declare target area
    for row in range(min_y, max_y):
        for col in range(min_x, max_x):
            field[row,col] = 'T' 
    min_to_T = min_x
    max_to_T = max_x

    # declare the trajectory variables
    start_point = (0,0)
    field[start_point] = 'S'
    print("Original field:")
    custom_print(field)

    # y,x
    a_vec = [1, -1]
    v_vec = [0, 0]
    print('Startpoint, a, v:', start_point, a_vec, v_vec)

    # pad the field
    padding = 1000
    padded = np.pad(field, pad_width=padding, mode='constant', constant_values = '.')
    padded_start = (start_point[0]+padding, start_point[1]+padding)
    print('Padded start:', padded_start)
    print('Padded matrix dim:', padded.shape)

    # to be in the target area the v_vec must be [0,0] and the content of the field must be 'T'

    def step(pt:tuple[int, int], curr_v:np.array, m:np.array):
        global panic
        
        if curr_v[0] > 200:
            print('This is very fast, probably an error:')
            panic = 1
            return pt, curr_v, m

        new_y = pt[0]+curr_v[0]
        new_x = pt[1]+curr_v[1]
        new_pt = (new_y, new_x)
        if new_pt[0] >= padded.shape[0] or new_pt[1] >= padded.shape[1]:
            #print('Out of bounds, will never reach.')
            panic = 1
            return pt, curr_v, m

        # if below any T, can not reach anymore
        if new_y > max(np.where(m=='T')[0]):
            #print('Below any target y-position, you will never reach the target.')
            panic = 1
            return pt, curr_v, m

        # calculate the new values
        new_v = np.add(curr_v, a_vec)
        if new_v[1] < 0:
            new_v[1] = 0
        
        else:
            m[pt_probe] = '#'
            m[padded_start] = 'S'
        return new_pt, new_v, m

    # init velocity list
    #v_start_list = [[-2,7]]
    v_range = (-50, max_to_T+1)
    v_start_list = [pt for pt in list(product(range(v_range[0], v_range[1]), repeat=2)) if (pt[1]>=min_to_T and pt[0]<=0)][::-1]
    #v_start_list = [(-60, min_to_T)]

    print(v_start_list)
    print(len(v_start_list))
    success_points:set = set()
    probe_max_y:dict = {x : 0 for x in v_start_list}
    print(len(probe_max_y.keys()))
    
    for v_start in v_start_list:
        #print('Testing with:', v_start)
        # init for looping
        pt_probe = padded_start
        v_probe = v_start
        panic = 0
        probe_max_y[v_start] = pt_probe[0]
        
        while (panic!=1):
            # check if better one has been found
            print('Current successful throws:', success_points, 'best throw found:', any(x[0] < v_start[0] for x in success_points), end='\r')
            if any(x[0] < v_start[0] for x in success_points) :
                    print('Found the best throw{}!'.format(np.add(pt_probe, -padding)))
                    break
            # check if above target
            if v_probe[1]==0 and v_probe[0]<= padding + min_y:
                print('Will reach the target!{}!'.format(np.add(pt_probe, -padding)))
                success_points.add(v_start)
                continue
            #print('Values before stepping:\ncoords of probe: {}, velocity of probe: {}'.format(pt_probe, v_probe))
            pt_probe, v_probe, padded = step(pt_probe, v_probe, padded)
            
                
            if pt_probe[0] < probe_max_y[v_start]:
                probe_max_y[v_start] = pt_probe[0]
            if padded[pt_probe] == 'T':
                padded[pt_probe] = '#'
                success_points.add(v_start)
                #print('Size before yeeting:', len(v_start_list))
                #v_start_list = [v for v in v_start_list if v[0]<=v_start]
                #print('Size after yeeting:', len(v_start_list))
                print('Successfully reached the target at{}!'.format(np.add(pt_probe, -padding)))
                continue

    success_max_y = {k:v for k,v in probe_max_y.items() if k in success_points}
    print(success_max_y)
    print('Maximal height reached:', padding - min(success_max_y.values()))
    return 0


def custom_print(matrix:np.array):
    for line in range(0, len(matrix)):
        lstr = ''.join(matrix[line, :])
        print(lstr)

def part2(data:str):
    return 0


def test():
    out = read_input(path_to_file='input/test_input.txt')
    
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")

    # shitty pt 1
    '''
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1_shitty(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")

    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    
    '''
    
if __name__ == '__main__':
    data = read_input()
    test()
    
    start_time = time.perf_counter()
    p1, p2 = part1(data)
    print('\nResult for part 1: ', p1)
    print('\nResult for part 2: ', p2)
    finish_time = time.perf_counter()
    print(f"Calculated both parts in {(finish_time - start_time):0.4f}s")
    