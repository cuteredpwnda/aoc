# -*- coding: utf-8 -*-
import itertools
import time
import numpy as np
from functools import reduce
from itertools import permutations


def read_input(path_to_file:str = 'input/raw_input.txt') -> list:
    """read_input Read the input

    Reads the input from a file with specified path

    Parameters
    ----------
    path_to_file : str, optional
        Path to the file to be read, by default 'input/raw_input.txt'

    Returns
    -------
    list
        The files content as list.
    """

    with open(path_to_file) as f:
        data = list(map(eval, f.read().splitlines()))
    return data

def part1(data)->int:
    print(data)
    print(type(data))
    
    resulting_sum = reduce(addition, data)
    print(resulting_sum)
    return magnitude(resulting_sum)

def magnitude(x):
    # check magnitude
    # 3* magnitude of left element + 2*magnitude of the right element -> just a number
    if isinstance(x, int):
        return x
    return 3*magnitude(x[0]) + 2*magnitude(x[1])


def l_addition(fish_num, acc):
    global debug
    if debug: print('Doing a left addition with: {}'.format(fish_num))
    if acc is None:
        return fish_num
    if isinstance(fish_num, int):
        return fish_num + acc
    # recurse the leftmost part
    return [l_addition(fish_num[0], acc), fish_num[1]]

def r_addition(fish_num, acc):
    global debug
    if debug: print('Doing a right addition with: {}'.format(fish_num))
    if acc is None:
        return fish_num
    if isinstance(fish_num, int):
        return fish_num + acc
    # recurse the rightmost part
    return [fish_num[0], r_addition(fish_num[1], acc)]

def explode(fish_num, d:int=4):
    """explode explodes the subterm

        - explode when nested in 4 pairs
        - left value + the first regular number to the left
        - right value + the first regular number to the right
        - replace with 0

    Parameters
    ----------
    v : [type]
        [description]
    d : int, optional
        [description], by default 0

    Returns
    -------
    [type]
        [description]
    """
    global debug
    if debug: print('Doing an explosion with: {}'.format(fish_num))
    if isinstance(fish_num, int):
        return False, None, fish_num, None
    # everything already exploded
    if d==0: return True, fish_num[0], 0, fish_num[1]
    
    # if explosions need to happen
    a, b = fish_num
    exploded, l, a, r = explode(a, d-1)
    # check if explosion returns True, if yes add right to left
    if exploded:
        new_num = [a, l_addition(b, r)]
        return True, l, new_num, None
    # check right one
    exploded, l, b, r = explode(b, d-1)
    if exploded:
        new_num = [r_addition(a, l), b]
        return True, None, new_num, r
    # return everything
    return False, None, fish_num, None
    

def split(fish_num):
    """split splits the subterm

        - split leftmost if >10
        - replace with a new pair
        - left is regular number //2, right is a regular number /2 -> ceil

    Parameters
    ----------
    v : [type]
        [description]
    """
    global debug
    if debug: print('Splitting: {}'.format(fish_num))
    if isinstance(fish_num, int):
        if fish_num >= 10:
            return True, [fish_num//2, int(np.ceil(fish_num/2))]
        else:
            return False, fish_num

    # split parts
    a,b = fish_num
    split_up, a = split(a)
    if split_up:
        return True, [a, fish_num[1]]
    # split right part
    split_up, b = split(b)
    return split_up, [a, b]


def addition(a, b):
    global debug
    if debug: print('Doing an addition with: {} and {}'.format(a, b))
    # is just a reduction of a and b
    fish_num = [a,b]
    while True:
        # first explode
        exploded, _, fish_num, _ = explode(fish_num)
        if exploded:
            continue        
        # split it
        split_up, fish_num = split(fish_num)
        # if they are not to split up (nothing to do anymore), break
        if not split_up:
            break
    return fish_num


def part2(data:str):
    max_magnitude = 0
    
    # get each combination
    perm = list(itertools.permutations(data, 2))
    for item in perm:
        a = item[0]
        b = item[1]
        result = addition(a, b)
        curr_mag = magnitude(result)
        if curr_mag >= max_magnitude:
            max_magnitude = curr_mag
    print('Amount of permutations:', len(perm))
    return max_magnitude


def test():
    global debug
    debug = True
    out = read_input(path_to_file='input/test_input.txt')
    '''
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    
    debug = False
    
debug = False

if __name__ == '__main__':
    data = read_input()
    #test()

    '''
    start_time = time.perf_counter()
    print('\nResult for part 1: ', part1(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    