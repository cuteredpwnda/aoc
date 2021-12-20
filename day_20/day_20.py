# -*- coding: utf-8 -*-
import time
import numpy as np

CHAR_MAP = {'.':0, '#':1}

def read_input(path_to_file:str = 'input/raw_input.txt') -> str:
    with open(path_to_file) as f:
        data = [lines.strip('\n') for lines in f.readlines()]
    enhancement = ''.join(data[:data.index('')])
    enhancement = np.array([CHAR_MAP[x] for x in enhancement])
    image = np.array([list(c) for c in data[data.index('')+1:]])
    image[image=='#'] = '1'
    image[image=='.'] = '0'
    return enhancement, image


def part1(enhancement:np.array, image:np.array, enhance_amount:int=2)->int:
    empty_char = 0

    def enhance_image(enhancement, image, empty_char=0):
        image = np.pad(image, 3, constant_values=empty_char)
        out_image = np.full_like(image, empty_char)
        ylen,xlen = image.shape
        for i in range(1,ylen-1):
            for j in range(1,xlen-1):
                idx = image[i-1:i+2, j-1:j+2].flatten()
                idx = int(''.join(map(str, idx)), 2)
                out_image[i,j] = enhancement[idx]
        return out_image[1:-1, 1:-1], enhancement[0] if empty_char == 0 else enhancement[511]

    for i in range(enhance_amount):
        image,empty_char = enhance_image(enhancement, image, empty_char)
        
    return (image=='1').sum()


def part2(enhancement:np.array, image:np.array, amount:int=50):
    return part1(enhancement, image, enhance_amount=amount)


def test():
    enh, img = read_input(path_to_file='input/test_input.txt')
    
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1(enh, img))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(enh, img))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    
    
    
def custom_print(matrix:np.array):
    for line in range(0, len(matrix)):
        lstr = ''.join(matrix[line, :])
        print(lstr)

if __name__ == '__main__':
    enh, img  = read_input()
    #test()
   
    start_time = time.perf_counter()
    print('\nResult for part 1: ', part1(enh, img))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(enh, img))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    