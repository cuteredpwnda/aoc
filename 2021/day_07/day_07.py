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
    return sum(fuel)

def calculate_part2(data):
    start_time = time.perf_counter()
    middle = round(sum(data)//len(data))
    fuel = [round((abs(x-middle)*(abs(x-middle)+1))/2) for x in data]
    finish_time = time.perf_counter()
    timer = (finish_time-start_time)*10**(6)
    return sum(fuel), timer

# credits https://www.reddit.com/r/adventofcode/comments/rar7ty/comment/hnk6gz0/
def optimal_solution(): 
    x = np.fromfile(open('input/raw_input.txt'), int, sep=',')
    start_time = time.perf_counter()
    res_1 = sum(abs(x - np.median(x)))
    finish_time = time.perf_counter()
    timer = (finish_time-start_time)*10**(6)
    print(f"Calculated part 1 in {timer:0.4f} microseconds (optimal)")
    fuel = lambda d: d*(d+1)/2
    start_time = time.perf_counter()
    res_2 = min(sum(fuel(abs(x - np.floor(np.mean(x))))),
            sum(fuel(abs(x - np.ceil(np.mean(x))))))
    finish_time = time.perf_counter()
    timer = (finish_time-start_time)*10**(6)
    print(f"Calculated part 2 in {timer:0.4f} microseconds (optimal)")
    return res_1, res_2


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
    res, timer = calculate_part2(data)
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {timer:0.4f} microseconds")

    start_time = time.perf_counter()
    res_1, res_2 = optimal_solution()
    finish_time = time.perf_counter()
    print(res_1, res_2)
