# -*- coding: utf-8 -*-
import time
import numpy as np

def read_input(path_to_file:str = 'input/raw_input.txt') -> str:
    with open(path_to_file) as f:
        data = [lines.strip('\n') for lines in f.readlines()]
    return data


def part1(enhancement:np.array, image:np.array, enhance_amount:int=2)->int:
    
    return 0


def part2(enhancement:np.array, image:np.array, amount:int=50):
    return part1(enhancement, image, enhance_amount=amount)


def test():
    enh, img = read_input(path_to_file='input/test_input.txt')
    
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1(enh, img))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(enh, img))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    
    '''

if __name__ == '__main__':
    data  = read_input()
    test()
    
    '''
    start_time = time.perf_counter()
    print('\nResult for part 1: ', part1(enh, img))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(enh, img))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''