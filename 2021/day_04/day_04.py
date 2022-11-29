import numpy as np
import time

# create a fish with (name, internal_timer, age)
# initial value of internal timer at creation is 2 

def test():
    return 0

def calculate(data):
    return 0


def test_part2():      
    return 0

def calculate_part2(data):    
    return 0


if __name__ == '__main__':    
    
    start_time = time.perf_counter()
    test()
    finish_time = time.perf_counter()
    print(f"Calculated test in {finish_time - start_time:0.4f} seconds")
    
    with open('input/raw_input.txt') as f:
        data = f.readline().split(',')
    data = [int(x) for x in data]
    
    
    start_time = time.perf_counter()
    calculate(data)
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {finish_time - start_time:0.4f} seconds")
    
    start_time = time.perf_counter() 
    res = test_part2()   
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {finish_time - start_time:0.4f} seconds")
    
    start_time = time.perf_counter()
    res = calculate_part2(data)
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {finish_time - start_time:0.4f} seconds")
