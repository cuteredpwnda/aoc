import numpy as np
import time

# create a fish with (name, internal_timer, age)
# initial value of internal timer at creation is 2 

def test():
    hor_pos = [16,1,2,0,4,2,7,1,2,14]
    sorted_pos = sorted(hor_pos)
    median = sorted_pos[len(sorted_pos)//2]
    fuel = [abs(x-median) for x in sorted_pos]
    fuel_sum = sum(fuel)
    print(fuel_sum)

def calculate(data):
    sorted_pos = sorted(data)
    median = sorted_pos[len(sorted_pos)//2]
    fuel = [abs(x-median) for x in sorted_pos]
    fuel_sum = sum(fuel)
    print(fuel_sum)


def test_part2():      
    hor_pos = [16,1,2,0,4,2,7,1,2,14]
    middle = round(sum(hor_pos)/len(hor_pos))
    fuel = [round((abs(x-middle)*(abs(x-middle)+1))/2) for x in hor_pos]
    fuel_sum = sum(fuel)
    print(fuel_sum)

def calculate_part2(data):    
    middle = round(sum(data)//len(data))
    print(middle)
    fuel = [round((abs(x-middle)*(abs(x-middle)+1))/2) for x in data]
    fuel_sum = sum(fuel)
    print(fuel_sum)


if __name__ == '__main__':    
    
    '''
    start_time = time.perf_counter()
    test()
    finish_time = time.perf_counter()
    print(f"Calculated test in {finish_time - start_time:0.4f} seconds")
    '''
    
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
