import numpy as np
import time


def read_input(file = 'input/raw_input.txt'):
    data = [line for line in open(file).read().splitlines()]
    data.remove('')
    return data

def part1(data, steps = 10):
    polymer_template = data[0]
    pair_list = [(p.split(' -> ')[0], p.split(' -> ')[1]) for p in data[1:]]

    # create the polymer from template in steps
    i = 0
    polymer = polymer_template    
    for i in range(steps):
        res_poly = polymer[0]
        temp_poly = ''
        for j in range(len(polymer)-1):
            for poly in pair_list:
                if polymer[j:j+2] == poly[0]:
                    temp_poly = polymer[j] + poly[1] + polymer[j+1]
                    res_poly += temp_poly[1:]
        polymer = res_poly

    # get unique strings:
    unique = set(polymer)
    # get max occurence in string
    max_occ = max(polymer.count(char) for char in unique)
    min_occ = min(polymer.count(char) for char in unique)
    return max_occ-min_occ

def part2(data, steps):
    polymer_template = data[0]
    pair_list = [(p.split(' -> ')[0], p.split(' -> ')[1]) for p in data[1:]]
    unique_chars = set([p for p in [l[0][0] for l in pair_list]])

    bucket = {}
        
    for i in range(len(polymer_template) - 1):
        pair = polymer_template[i:i + 2]
        if pair not in bucket.keys():
            bucket[pair] = 1
        else:
            bucket[pair] += 1


    for pair, target in pair_list:
        if pair not in bucket.keys():
            bucket[pair] = 0


    for i in range(steps):
        op_list = []
        for pair, value in pair_list:
            if pair not in bucket.keys():
                continue
            cur_cnt = bucket[pair]
            op_list.append((pair, -cur_cnt))
            new = [pair[0] + value, value + pair[1]]
            for n in new:
                op_list.append((n, cur_cnt))
        
        for pair, op in op_list:
            if pair not in bucket.keys():
                bucket[pair] = op
            else:
                bucket[pair] += op

    count_dict = {}
    for k, v in bucket.items():
        for c in k:
            if c not in count_dict.keys():
                count_dict[c] = 0.5*v
            else:
                count_dict[c] += 0.5*v

    r = [polymer_template[:1], polymer_template[-1:]]
    for c in r:
        count_dict[c] +=0.5

    return int(max(count_dict.values()) - min(count_dict.values()))
     
def test():
    out = read_input(file='input/test_input.txt')
    start_time = time.perf_counter()
    print('Result for part 1 in test: ', part1(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time)*10**3:0.4f} ms")
    
    start_time = time.perf_counter()
    print('Result for part 2 in test: ', part2(out, 40))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time)*10**3:0.4f} ms")
    

if __name__ == '__main__':
    input_matrix = read_input()
    #test()
    
    start_time = time.perf_counter()
    print('Result for part 1: ', part1(input_matrix))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time)*10**3:0.4f} ms")
    
    start_time = time.perf_counter()
    print('Result for part 2: ', part2(input_matrix, 40))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time)*10**3:0.4f} ms")
    