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

def part1(data:str)->int:
    """part1 Method for solving part 1.

    [extended_summary]

    Parameters
    ----------
    data : str
        The transmission coming in.

    Returns
    -------
    int
        Solution of part 1, sum of all version numbers in transmission.
    """
    
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