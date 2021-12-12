import numpy as np

def read_input(file = 'input/raw_input.txt'):
    return np.genfromtxt(file, delimiter = '-')

def part1(b):    
    print(b)
    return 0

def getAdj(pt):
    y = pt[0]
    x = pt[1]
    return [(y-1, x), (y-1, x+1), (y, x+1), (y+1, x+1), (y+1, x), (y+1, x-1), (y, x-1), (y-1, x-1)]

def test():
    out = read_input(file='input/test_input.txt')
    part1(out)
    #m, res = part1(out)
    #print('Result for part 1: ', res, 'Matrix: \n', m)
    #m2, res2 = part2(out)
    #print('Result for part 2: ', res2, 'Matrix: \n', m2)

def part2(b):
    return 0

if __name__ == '__main__':
    input_matrix = read_input()
    test()
    #m, res = part1(input_matrix)
    #print('Result for part 1: ', res, 'Matrix: \n', m)
    #m2, res2 = part2(input_matrix)
    #print('Result for part 2: ', res2, 'Matrix: \n', m2)