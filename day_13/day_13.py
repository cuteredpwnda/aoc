import numpy as np

def read_input(file = 'input/raw_input.txt'):
    data = [line for line in open(file).read().splitlines()]
    return data

def part1(b, stop_at_one=True):
    if stop_at_one: 
        b.remove('')
    points = [(int(s[0]), int(s[1])) for s in [elem.split(',') for elem in b if 'fold along' not in elem]]
    fold_instruction =  [elem for elem in b if 'fold along' in elem]

    max_y = max([y for y in [val[1] for val in points]])
    max_x = max([x for x in [val[0] for val in points]])

    m = np.zeros((max_y+1, max_x+1), dtype=str)
    m[m==''] = '.'

    for pt in points:
        m[pt[1], pt[0]] = '#'

    # now fold
    i = 1
    for fold_ins in fold_instruction:
        line_to_fold = int(fold_ins.split('=')[1])
        if fold_ins.split('=')[0][-1] == 'y':
            top = m[:line_to_fold, :]
            bottom = m[line_to_fold+1:, :]
            # "invert" bottom
            bottom_inv = np.flipud(bottom)
            m = np.where(bottom_inv != '.', bottom_inv, top)
        if fold_ins.split('=')[0][-1] == 'x':
            left = m[:, line_to_fold+1:]
            right = m[:, :line_to_fold]
            # "invert" left
            left_inv = np.fliplr(left)
            m = np.where(left_inv != '.', left_inv, right)
        dot_count = (m == '#').sum()
        i+=1
        if stop_at_one:
            break
    return m, dot_count

def part2(b):
    m, res = part1(b, stop_at_one=False)
    m[m =='#'] =  u"\u2588"
    for line in range(0, len(m)):
        lstr = ''.join(m[line, :])
        print(lstr)
    return m, res 

def test():
    out = read_input(file='input/test_input.txt')
    _, res = part1(out)
    print('Result for part 1 in test: ', res)    
    part2(out)

if __name__ == '__main__':
    input_matrix = read_input()
    test()
    m, res = part1(input_matrix)
    print('Result for part 1: ', res)
    part2(input_matrix)