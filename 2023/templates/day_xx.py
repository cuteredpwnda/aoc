import os
from glob import glob
from functools import wraps
from time import time

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
    pass

@timing
def pt1(input):
    print(f"Result Part 1: {None}")

@timing
def pt2(input):
    print(f"Result Part 2: {None}")

def main():
    test_input_file = glob(os.path.join(os.path.dirname(__file__), "input", "test.txt"))[0]
    input_file = glob(os.path.join(os.path.dirname(__file__), "input", "input.txt"))[0]
    # pt 1
    
    # pt 2
    
    

if __name__ == '__main__':
    main()
