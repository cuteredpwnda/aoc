import os
from glob import glob
from functools import wraps
from time import time
import numpy as np

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f'{f.__name__} took: {((te-ts))*1000:.4f} ms')
        return result
    return wrap

@timing
def read_input(input_file):
    with open(input_file, 'r') as f:
        input = f.read().splitlines()
    return input

def get_sequences(line):
    numbers = [int(x) for x in line.split(' ')]
    step_size = np.inf
    extrapolate_set = [numbers]
    steps = [step_size for _ in range(len(numbers))]
    while not all(x == 0 for x in steps):
        sequences = []
        curr_steps = []
        iter_numbers = zip(numbers[0:], numbers[1:])
        for number_tuple in iter_numbers:
            step_size = number_tuple[1] - number_tuple[0]
            sequences.append(step_size)
            curr_steps.append(step_size)
            # set the generated sequence as new input
            numbers = sequences
        steps = curr_steps
        extrapolate_set.append(sequences)
    return extrapolate_set

def extrapolate(extrapolate_set, pt_2=False, test=False):
    if pt_2: extrapolate_set = [s[::-1] for s in extrapolate_set]
    # add a zero to the last sequence    
    extrapolate_set[-1].append(0)
    extrapolate_set = extrapolate_set[::-1]
    # extrapolate up to the first sequence
    finish_len = len(extrapolate_set[-1]) + 1
    for i in range(len(extrapolate_set)):
        if len(extrapolate_set[i]) == finish_len:
            break
        # add the sum of the last number of the sequence before and the current last number of the sequence
        curr_last = extrapolate_set[i][-1]
        prev_last = extrapolate_set[i+1][-1]
        if not pt_2:
            extrapolate_set[i+1].append(np.sum([curr_last, prev_last]))
        else:
            extrapolate_set[i+1].append(prev_last - curr_last)
    if pt_2: extrapolate_set = [s[::-1] for s in extrapolate_set]
    if test: cool_print(extrapolate_set)
    return extrapolate_set

def cool_print(extrapolate_set):
    print_set = extrapolate_set[::-1]
    for i in range(len(extrapolate_set)):
        num = print_set[i]
        # pad num to be the same length as the longest number
        num = [str(x).rjust(3, " ") for x in num]
        # insert i*2 spaces before the sequence
        print("  "*i+f"{num}".replace("[", "").replace("]", "").replace(",", "").replace("'", ""))

@timing
def pt1(input, test=False):
    last_elements = [extrapolate(get_sequences(x), test)[-1][-1] for x in input]
    print(f"Result Part 1: {np.sum(last_elements)}")

@timing
def pt2(input, test=False):
    last_elements = [extrapolate(get_sequences(x), True, test)[-1][0] for x in input]
    print(f"Result Part 2: {np.sum(last_elements)}")


def main():
    test_input_file = glob(os.path.join(os.path.dirname(__file__), "input", "test.txt"))[0]
    input_file = glob(os.path.join(os.path.dirname(__file__), "input", "input.txt"))[0]
    # pt 1
    pt1(read_input(test_input_file), True)
    pt1(read_input(input_file))
    
    # pt 2
    pt2(read_input(test_input_file), True)
    pt2(read_input(input_file))
    
    

if __name__ == '__main__':
    main()
