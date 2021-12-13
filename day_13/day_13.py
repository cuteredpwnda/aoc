import numpy as np

def read_input(file = 'input/raw_input.txt'):
    data = [line.split("-") for line in open(file).read().splitlines()]
    return data

def part1(b):    
    return 0


def part2(b):
    return 0

def test():
    out = read_input(file='input/test_input.txt')
    print(part1(out))
    #m, res = part1(out)
    #print('Result for part 1: ', res, 'Matrix: \n', m)
    print(part2(out))
    #print('Result for part 2: ', res2, 'Matrix: \n', m2)

if __name__ == '__main__':
    input_matrix = read_input()
    #test()
    #m, res = part1(input_matrix)
    print('Result for part 1: ', part1(input_matrix))
    #m2, res2 = part2(input_matrix)
    print('Result for part 2: ', part2(input_matrix))