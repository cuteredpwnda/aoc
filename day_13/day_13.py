import numpy as np

def read_input(file = 'input/raw_input.txt'):
    data = [line for line in open(file).read().splitlines()]
    return data

def part1(b, stop_at_one=True):
    if stop_at_one: 
        b.remove('')
    points = [(int(s[0]), int(s[1])) for s in [elem.split(',') for elem in b if 'fold along' not in elem]]
    fold_instruction =  [elem for elem in b if 'fold along' in elem]
    #print('Points (x,y): ', points)
    #print('Where to fold (x,y): ', fold_instruction)

    max_y = max([y for y in [val[1] for val in points]])
    max_x = max([x for x in [val[0] for val in points]])

    #print(max_x, max_y)
    # create a matrix(y, x):
    m = np.zeros((max_y+1, max_x+1), dtype=str)
    m[m==''] = '.'

    for pt in points:
        m[pt[1], pt[0]] = '#'

    #print(m)
    
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
            #print('Result of folding: \n', m)
        if fold_ins.split('=')[0][-1] == 'x':
            left = m[:, line_to_fold+1:]
            right = m[:, :line_to_fold]
            # "invert" right
            right_inv = np.fliplr(right)
            #print('Bottom part inv:\n',bottom_inv)
            m = np.where(right_inv != '.', right_inv, left)
            #print('Result of folding: \n', m)
        dot_count = (m == '#').sum()
        print('Dots visible after fold {}: {}'.format(i, dot_count))
        i+=1
        if stop_at_one:
            break
    return m, dot_count

def part2(b):
    m, res = part1(b, stop_at_one=False)
    f = open("output.txt", "w")
    m[m =='#'] =  u"\u2588"
    m = np.fliplr(m)
    for line in range(0, len(m)):
        lstr = ''.join(m[line, :])
        print(lstr)
        f.writelines(lstr+'\n')
    f.close()
    return m, res 

def test():
    out = read_input(file='input/test_input.txt')
    print('Result for part 1: ', part1(input_matrix))
    #print(part2(out))
    #print('Result for part 2: ', res2, 'Matrix: \n', m2)

if __name__ == '__main__':
    input_matrix = read_input()
    #test()
    m, res = part1(input_matrix)
    print('Result for part 1: ', res)
    part2(input_matrix)