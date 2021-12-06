import numpy as np
import time

# create a fish with (name, internal_timer, age)
# initial value of internal timer at creation is 2 
class lanternfish:
    name = 'Lampenbert'
    internal_timer = 2
    age = 0
    double_time = 7
    fish_tuple = (name, internal_timer, age)

    def __init__(self, fish_id, internal_timer=2, age=0):
        self.name = 'Lampenbert #{}'.format(fish_id)
        self.internal_timer = internal_timer
        self.age = age
        self.fish_tuple = (self.name, self.internal_timer, self.age)

    def next_day(self):
        if (self.internal_timer == 0):
            self.age += 1
            self.internal_timer = 6
            return lanternfish('_spawn_@day_'.format(self.age), 9, 0)
        else:
            self.internal_timer -=1
            self.age += 1
            return None
        

def test():
    test_data = [3,4,3,1,2]
    # create fish array
    fish_array = []
    i = 1
    for timer in test_data:
        fish_array.append(lanternfish(i, timer, 0))
        i+=1
    
    fish_timers = [x.internal_timer for x in fish_array]
    print('Initial state: {}'.format(fish_timers))

    duration = 18
    
    for i in range(1,duration+1):
        for bert in fish_array:
            new_fish = bert.next_day()
            if new_fish:
                fish_array.append(new_fish)
        fish_timers = [x.internal_timer for x in fish_array]
        print('After {} days: {}'.format(i, fish_timers))
    

def main():
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

    duration = 80
    
    for i in range(1,duration+1):
        for bert in fish_array:
            new_fish = bert.next_day()
            if new_fish:
                fish_array.append(new_fish)
    print('After {} days there are {} lanternfish'.format(duration, len(fish_array)))
    

if __name__ == '__main__':
    #test()
    start_time = time.perf_counter()
    main()
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {finish_time - start_time:0.4f} seconds")