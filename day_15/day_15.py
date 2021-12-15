from types import new_class
import numpy as np
import time
from heapdict import heapdict

def read_input(file = 'input/raw_input.txt'):
    return np.genfromtxt(file, delimiter = 1)

def getAdj(pt, m):
    y = pt[0]
    x = pt[1]
    v = m[y,x]
    adj_dist = {(y-1, x):m[y-1,x], # down
                (y, x+1):m[y,x+1], # right
                (y, x-1):m[y,x-1], # left
                (y+1, x):m[y+1,x]  # up
                }
    # filter all infs
    return {k:v for k,v in adj_dist.items() if abs(v) <= 9}

def part1(data):
    data = np.pad(data, pad_width=1, mode='constant', constant_values = np.inf)
    print('Shape of the matrix:', data.shape)
    x_list = list(zip(np.where(data<=9)[0],np.where(data<=9)[1]))
    print('Positions in graph:', len(x_list))
    adj_graph = {pt:getAdj(pt,data) for pt in x_list}
    print('Keys in graph:', len(adj_graph.keys()))
    max_y, max_x = data.shape
    cost = dijkstra(adj_graph, (1,1), (max_y-1, max_x-1), data)
    return int(cost)

def dijkstra(graph, initial, end_node, matrix):
    queue = heapdict()    
    init_y, init_x = initial
    max_y, max_x = end_node
    #shortest= [[-1 for _ in range(max_y)] for _ in range(max_x)]
    #shortest[0][0] = 0
    shortest = np.zeros_like(matrix[1:-1, 1:-1])
    shortest[shortest==0] = -1
    shortest[0,0] = 0
    
    queue[(init_y,init_x)] = 0
    visited = set()

    while queue:
        node, d = queue.popitem()
        y_node, x_node = node
        visited.add(node)
        neigbors = []
        for n in graph.get(node):
            neigbors.append(n)
        for k in neigbors:
            k_y, k_x = k
            if (init_y <= k_y < max_y and init_x <= k_x < max_x and k not in visited):
                new_best = shortest[y_node-1, x_node-1] + matrix[k_y, k_x]
                if new_best < shortest[k_y-1, k_x-1] or shortest[k_y-1, k_x-1] == -1:
                            shortest[k_y-1, k_x-1] = new_best
                            queue[k] = new_best
    return int(shortest[-1][-1])

def part2(data, resize=5):
    # make the array bigger owo
    v_stacked = data

    for i in range(1, resize):
        v_stacked = np.vstack((v_stacked,data+i))
        v_stacked[v_stacked>9] %=9
    
    stacked = v_stacked

    for i in range(1, resize):
        stacked = np.hstack((stacked,v_stacked+i))
        stacked[stacked>9] %=9
    return part1(stacked)
     
def test():
    out = read_input(file='input/test_input.txt')
    
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    
    
    
if __name__ == '__main__':
    input_matrix = read_input()
    #test()
    
    start_time = time.perf_counter()
    print('\nResult for part 1: ', part1(input_matrix))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(input_matrix))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")