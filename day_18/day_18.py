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
        data = f.readlines()
    data = [line.strip('\n') for line in data]
    return data

def part1(data:str)->int:
    # addition
    print(data)

    # explode when nested in 4 pairs
    # left value + the first regular number to the left
    # right value + the first regular number to the right
    # replace with 0


    # split leftmost if >10
    # replace with a new pair
    # left is regular number //2, right is a regular number /2 -> ceil

    # reduce

    # check magnitude
    # 3* magnitude of left element + 2*magnitude of the right element -> just a number
    return 0


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
    
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''