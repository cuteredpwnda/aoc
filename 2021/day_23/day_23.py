# -*- coding: utf-8 -*-
import time
import numpy as np

def read_input(path_to_file:str = 'input/raw_input.txt') -> str:
    with open(path_to_file) as f:
        data = f.read()
    return data


A,B,C,D = 'ABCD'

AMPHIPODS = {'A': 1,
            'B' : 10,
            'C' : 100,
            'D' : 1000}
HALLWAYDOORS = {1:2,
                2:4,
                3:6,
                4:8}
DOORS = {2,4,6,8}

TARGETS = dict(zip(''.join(AMPHIPODS.keys()), tuple(sorted(list(DOORS)))))


def legal_moves(state):
    for i in range(1, 5):
        index_t = 0
        try:
            while state[i][index_t] is None: index_t+=1
        except IndexError:
            # room is empty
            continue
        states = list(map(list, state))
        amphipod = states[i][index_t]
        # check for bottom ones being already correct
        if TARGETS[amphipod] == (-1,2,4,6,8)[i] and all(amphipod==other for other in state[i][index_t]): continue
        steps = index_t
        states[i][index_t] = None
        legal_locations = []
        for j in range(HALLWAYDOORS[i]):
            if j not in DOORS:
                legal_locations.append(j)
            if states[0][j] is not None:
                legal_locations.clear()
        for j in range(HALLWAYDOORS[i], 11):
            if states[0][j] is not None:
                break
            if j not in DOORS:
                legal_locations.append(j)
        between_state = list(map(tuple, states))
        hallway = state[0]
        for p in legal_locations:
            hallways = list(hallway)
            hallways[p]=amphipod
            between_state[0] = tuple(hallways)
            yield tuple(between_state), ((1+steps+abs(p-HALLWAYDOORS[i]))*AMPHIPODS[amphipod])
    
    # now into the room
    for j, amp in enumerate(state[0]):
        if amphipod is None: continue
        room = 'ABCD'.index(amphipod)
        room_set = set(state[room])
        room_set.discard(None)
        if room_set and {amphipod} != room_set: # illegal to go here
            continue
        if j<TARGETS[amphipod]:
            s1 = slice(j+1,TARGETS[amphipod]+1)
        else: s1 = slice(TARGETS[amphipod], j)
        # check for clear path
        for t in state[0][s1]:
            if t is not None:
                break

        steps = abs(j-TARGETS[amp])
        states = list(map(list,state))
        states[0][j] = None  # Remove from hallway
        room_list = states[room]
        for index_t,val in reversed(list(enumerate(room_list))):
            if val is None: break
        assert room_list[index_t] is None  # check if legal
        room_list[index_t]=amp
        steps+=1+index_t
        yield tuple(map(tuple,states)),steps*AMPHIPODS[amp]



def part1(data):
    letters = [c for c in data if c.isalpha()]
    rows = letters[:4],letters[4:]
    print(rows)   

    initial_state = ((None,)*11,) + tuple(zip(*rows))
    print(initial_state)

    ROOM_SIZE = len(initial_state[1])

    target_state = (
        (None,)*11,
        (A,)*ROOM_SIZE,
        (B,)*ROOM_SIZE,
        (C,)*ROOM_SIZE,
        (D,)*ROOM_SIZE
    )

    def steps_needed(state):
        if state == target_state: return 0
        all_costs = [float('inf')]
        for new_state, new_cost in legal_moves(state):
            all_costs.append(new_cost + steps_needed(new_state))
        return min(all_costs)

    return steps_needed(initial_state)


def part2(data):
    return 0

def test():
    data = read_input(path_to_file='input/test_input.txt')
    
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    '''
    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    
    '''

if __name__ == '__main__':
    data  = read_input()
    test()
    '''
    start_time = time.perf_counter()
    print('\nResult for part 1:', part1(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''