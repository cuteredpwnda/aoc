from types import new_class
import numpy as np
import time
from heapdict import heapdict

def read_input(file = 'input/raw_input.txt'):
    return np.genfromtxt(file, dtype=str)

def part1(data):
    print(data)
    # encode header
    version = data[:3]
    standard_header = []

    return 0

def part2(data):
    return 0
     
def test():
    out = read_input(file='input/test_input.txt')
    
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
    input_matrix = read_input()
    test()
    '''
    start_time = time.perf_counter()
    print('\nResult for part 1: ', part1(input_matrix))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(input_matrix))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''