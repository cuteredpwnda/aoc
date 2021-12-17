# -*- coding: utf-8 -*-
import time
import numpy as np

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

# panic button
panic = 0

def part1(data:str)->int:
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
    padding = 8
    padded = np.pad(field, pad_width=padding, mode='constant', constant_values = '.')
    padded_start = (start_point[0]+padding, start_point[1]+padding)
    print('Padded start:', padded_start)

    # to be in the target area the v_vec must be [0,0] and the content of the field must be 'T'

    def step(pt:tuple[int, int], curr_v:np.array, m:np.array, current_padding:int):
        global panic
        if curr_v[0] > 50:
            print('This is very fast, probably an error:')
            panic = 1
            return pt, curr_v, m, current_padding

        new_y = pt[0]+curr_v[0]
        new_x = pt[1]+curr_v[1]
        new_pt = (new_y, new_x)

        # if below any T, can not reach anymore
        if new_y > max(np.where(m=='T')[0]):
            print('Below any target y-position, you will never reach the target.')
            panic = 1
            return pt, curr_v, m, current_padding

        # calculate the new values
        new_v = np.add(curr_v, a_vec)
        if new_v[1] < 0:
            new_v[1] = 0

        # check if still in bounds
        if new_y >= m.shape[0] or new_x >= m.shape[1]:
            new_pad = max(new_v) + 1
            print(current_padding)
            m = np.pad(m, pad_width=new_pad, mode='constant', constant_values = '.')            
        else:
            m[pt_probe] = '#'
            m[padded_start] = 'S'
            new_pad = 0
        return new_pt, new_v, m, current_padding+new_pad
    
    
   

    # init velocity list
    v_start_list = [[-2,7]]
    # start velocity and pt:
    for v_start in v_start_list:
        # init for looping
        pt_probe = padded_start
        v_probe = v_start
        while (panic!=1):
            pt_probe, v_probe, padded, padding = step(pt_probe, v_probe, padded, padding)
            print('New Positon:', pt_probe, 'New speed:', v_probe)
            #custom_print(padded)
            if padded[pt_probe] == 'T':
                padded[pt_probe] = '#'
                custom_print(padded)
                print('Successfully reached the target at{}!'.format(np.add(pt_probe, -padding)))
                continue

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
    '''
    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    
    '''
    
if __name__ == '__main__':
    data = read_input()
    test()

    '''
    start_time = time.perf_counter()
    print('\nResult for part 1: ', part1(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    '''
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''