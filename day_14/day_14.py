import numpy as np

def read_input(file = 'input/raw_input.txt'):
    data = [line for line in open(file).read().splitlines()]
    return data

def part1(b):
    print(b)
    return 0

def part2(b):
    return 0

def test():
    out = read_input(file='input/test_input.txt')
    part1(out)
    #print('Result for part 1 in test: ', res)    
    #part2(out)

if __name__ == '__main__':
    input_matrix = read_input()
    test()
    #m, res = part1(input_matrix)
    #print('Result for part 1: ', res)
    #part2(input_matrix)