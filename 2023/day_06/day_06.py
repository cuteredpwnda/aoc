import os
from glob import glob
import numpy as np
from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f'{f.__name__} took: {(te-ts):.4f} sec')
        return result
    return wrap

@timing
def read_input(input_file) -> list:
    with open(input_file, 'r') as f:
        input = f.read().splitlines()
        # zip the two lists together
        return list(zip(map(int, [x for x in input[0].split("  ")[3::] if x != '']),
                              map(int,  [x for x in input[1].split("  ")[1::] if x != ''])))
@timing
def read_input_pt2(input_file) -> list:
    with open(input_file, 'r') as f:
        input = f.read().splitlines()
        return [[int(input[0].split(": ")[-1].replace(" ", "")), int(input[1].split(": ")[-1].replace(" ", ""))]]

@timing
def calc_races(input, p=1):
    results = []
    for part in input:
        t = part[0]
        d = part[1]
        winners = []
        for t_x in [x for x in range(0, t)]:
            d_travelled = (t-t_x)*t_x
            if d_travelled > d:
                winners.append(t_x)
        results.append(len(winners))
    res = np.prod(results)
    print(f"Result Part {p}: {res}")

        
def main():
    input_file = glob(os.path.join(os.path.dirname(__file__), "input", "input.txt"))[0]
    input = read_input(input_file)
    calc_races(input)

    # pt 2 test
    input = read_input_pt2(input_file)
    calc_races(input, p=2)


if __name__ == '__main__':
    main()
