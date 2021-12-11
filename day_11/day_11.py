import numpy as np

def read_input(file = 'input/raw_input.txt'):
    #return np.genfromtxt(file, delimiter = 1)
    return np.pad(np.genfromtxt(file, delimiter = 1), pad_width=1, mode='constant', constant_values = np.nan)

def part1(b):    
    flash_counter = 0
    # each step
    i = 0    
    while (i < 100):
        b, flash_counter, _ = step(b, flash_counter)
        i+=1
    return b, flash_counter

def getAdj(pt):
    y = pt[0]
    x = pt[1]
    t = (y-1, x)
    tr = (y-1, x+1)
    r = (y, x+1)
    br = (y+1, x+1)
    b = (y+1, x)
    bl = (y+1, x-1)
    l = (y, x-1)
    tl = (y-1, x-1)
    return [t, tr, r, br, b, bl, l, tl]

def step(b, flash_counter, all_flashed = False):
    b += 1
    x_list = list(zip(np.where(b>=10)[0],np.where(b>=10)[1]))
    flashed = x_list
    for x in x_list:
        adj = getAdj(x)
        for pt in adj:
            if pt not in flashed:
                b[pt[0]][pt[1]] += 1
                if b[pt[0]][pt[1]] > 9:
                    flashed.append(pt)
    
    flash_counter += len(flashed)

    filled_rows = len(b)-2
    filled_cols = len(b[0])-2
    if len(flashed) ==  filled_rows*filled_cols:
        all_flashed = True

    for p in flashed:
        b[p[0], p[1]] = 0
    return b, flash_counter, all_flashed

def test():
    out = read_input(file='input/test_input.txt')
    #m, res = part1(out)
    #print('Result for part 1: ', res, 'Matrix: \n', m)
    m2, res2 = part2(out)
    print('Result for part 2: ', res2, 'Matrix: \n', m2)

def part2(b):
    flash_counter = 0
    i = 0
    all_flashed = False  
    while (not all_flashed):
        b, flash_counter, all_flashed = step(b, flash_counter)
        i+=1
    return b, i

if __name__ == '__main__':
    input_matrix = read_input()
    #test()
    #m, res = part1(input_matrix)
    #print('Result for part 1: ', res, 'Matrix: \n', m)
    m2, res2 = part2(input_matrix)
    print('Result for part 2: ', res2, 'Matrix: \n', m2)