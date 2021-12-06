import numpy as np
import time

# create a fish with (name, internal_timer, age)
# initial value of internal timer at creation is 2 
class lanternfish:
    name = 'Lampenbert'
    id = 1
    internal_timer = 2
    age = 0
    double_time = 7
    fish_tuple = (name, internal_timer, age)

    def __init__(self, fish_id, internal_timer=2, age=0):
        self.name += str(fish_id)
        self.id += 1
        self.internal_timer = internal_timer
        self.age = age
        self.fish_tuple = (self.name, self.internal_timer, self.age)

    def next_day(self):
        if (self.internal_timer == 0):
            self.age += 1
            self.internal_timer = 6
            return lanternfish('#{}_spawn_@day_{}'.format(self.id,self.age), 9, 0)
        else:
            self.internal_timer -=1
            self.age += 1
            return None

def test(duration):
    test_data = [3,4,3,1,2]
    # create fish array
    fish_array = []
    i = 1
    for timer in test_data:
        fish_array.append(lanternfish(i, timer, 0))
        i+=1
    
    for i in range(1,duration+1):
        for bert in fish_array:
            new_fish = bert.next_day()
            if new_fish:
                fish_array.append(new_fish)
    print('After {} days there are {} lanternfish'.format(duration, len(fish_array)))    
    

def calculate(duration):
    # read initial state
    with open('input/raw_input.txt') as f:
        data = f.readline().split(',')
    
    # convert to int
    data = [int(x) for x in data]

    # create fish array
    fish_array = []
    i = 1
    for timer in data:
        fish_array.append(lanternfish(i, timer, 0))
        i+=1
    
    for i in range(1,duration+1):
        for bert in fish_array:
            new_fish = bert.next_day()
            if new_fish:
                fish_array.append(new_fish)
    print('After {} days there are {} lanternfish'.format(duration, len(fish_array)))


def new_fish(st, d):
        fish_array = [st.count(i) for i in range(7)]
        pufferfish = [0, 0]
        # calculate the fish growth
        for i in range(d):
            daddy = pufferfish.pop(0)
            kid = fish_array.pop(0)
            pufferfish.append(kid)
            fish_array.append(kid + daddy)
        return sum(fish_array)+sum(pufferfish)

def test_part2(test_data,duration):      
    # calculate the fish growth
    return new_fish(test_data, duration)

def calculate_part2(data, duration):    
    return new_fish(data, duration)


if __name__ == '__main__':
    '''
    start_time = time.perf_counter()
    test(200)
    finish_time = time.perf_counter()
    print(f"Calculated test in {finish_time - start_time:0.4f} seconds")
    
    start_time = time.perf_counter()
    calculate(80)
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {finish_time - start_time:0.4f} seconds")
    '''

    with open('input/raw_input.txt') as f:
        data = f.readline().split(',')
    data = [int(x) for x in data]
    
    start_time = time.perf_counter()    
    test_data = [3,4,3,1,2]
    res = test_part2(test_data, 80)   
    finish_time = time.perf_counter()
    print('After {} days there are {} lanternfish'.format(80, res)) 
    print(f"Calculated part 2 in {finish_time - start_time:0.4f} seconds")

    start_time = time.perf_counter()
    res = calculate_part2(data, 256)
    finish_time = time.perf_counter()
    print('After {} days there are {} lanternfish'.format(256, res)) 
    print(f"Calculated part 2 in {finish_time - start_time:0.4f} seconds")