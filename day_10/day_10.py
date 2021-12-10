import numpy as np
from operator import mul

SCORE_DICT = {  ')' : 3, 
                ']' : 57,
                '}' : 1197,
                '>' : 25137}

SCORE_DICT_PT2 = {  ')' : 1, 
                    ']' : 2,
                    '}' : 3,
                    '>' : 4}

OPENING = ('(', '[', '{', '<')
CLOSING = (')', ']', '}', '>')

CORR = dict(zip(OPENING, CLOSING))

def read_input(file = 'input/raw_input.txt'):
    return np.genfromtxt(file, dtype=str)

def part1(b):
    balance_list = []
    expressions_list = []
    for line in b:
        score, expr = check(line)
        balance_list.append(score)
        expressions_list.append(expr)
    
    count_tuples = [(x, balance_list.count(x)) for x in set(balance_list)]
    return sum(x*y for x, y in count_tuples), expressions_list

def check(expression):
    brackets = ['()', '{}', '[]', '<>']
    while any(x in expression for x in brackets):
        for br in brackets:
            expression = expression.replace(br, '')
    # now find the closing that does not match
    if any(x in expression for x in CLOSING):        
        mismatched = [x for x in expression if x in CLOSING][0]
        #print('Found: ', mismatched)
        #print('Expected: ', CORR[expression[expression.index(mismatched)-1]])
        return SCORE_DICT[mismatched], ''
    else: return 0, expression

def test():
    out = read_input(file='input/test_input.txt')
    score, expr_list = part1(out)
    print('Result for part 1: ', score)
    print('Result for part 2: ', part2(expr_list))

def multiple(lst, curr = 0):
                if lst:
                    curr = curr*5+lst.pop(0)
                    return multiple(lst, curr)
                else: 
                    return curr

def part2(expr_ls):
    winner_list = []
    for expr in expr_ls:
        if expr:
            rev = ''.join([CORR[x] for x in  expr[::-1]])
            rev_score = [SCORE_DICT_PT2[x] for x in rev]
            winner_list.append(multiple(rev_score))
    return sorted(winner_list)[len(winner_list)//2]
    

def bfs(x:int,y:int, input_matrix:np.ndarray):
    start = [(x, y)]
    queue = start
    visited = set()
    while(queue):
        (curr_x, curr_y) = start.pop(0)
        if ((curr_x, curr_y) in visited or input_matrix[curr_x][curr_y] >= 9):
            continue
        visited.add((curr_x, curr_y))
        # add elements in order up, down, left, right
        queue.append((curr_x, curr_y-1))
        queue.append((curr_x, curr_y+1))
        queue.append((curr_x-1, curr_y))
        queue.append((curr_x+1, curr_y))
    return visited

if __name__ == '__main__':
    input_matrix = read_input()
    #test()
    p1, for_p2 = part1(input_matrix)
    p2 = part2(for_p2)
    print('Result for part 1: ', p1)
    print('Result for part 2: ', p2)