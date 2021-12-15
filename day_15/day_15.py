import numpy as np
import time


def read_input(file = 'input/raw_input.txt'):
    return np.pad(np.genfromtxt(file, delimiter = 1), pad_width=1, mode='constant', constant_values = np.inf)

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
    x_list = list(zip(np.where(data<=9)[0],np.where(data<=9)[1]))
    adj_graph = {pt:getAdj(pt,data) for pt in x_list}
    #print(adj_graph)
    path = dijkstra(adj_graph, (1,1), ((len(data)-2), len(data[0])-2))[::-1]
    print(path)
    cost=0
    for node in path[1:]:
        y = node[0]
        x = node[1]
        cost += data[y,x]
    return int(cost)

# with end node
def dijkstra(graph, initial, end_node):
    path = {}
    adj_node = {}
    queue = []
    
    shortest_path = [end_node]

    for node in graph:
        #print(node)
        path[node] = np.inf
        adj_node[node] = None
        queue.append(node)
    
    path[initial] = 0

    while queue:
        key_min = queue[0]
        min_val = path[key_min]
        for n in range(1, len(queue)):
            if path[queue[n]] < min_val:
                key_min = queue[n]  
                min_val = path[key_min]
        cur = key_min
        queue.remove(cur)
        
        
        for i in graph[cur]:
            alternate = graph[cur][i] + path[cur]
            if path[i] > alternate:
                path[i] = alternate
                adj_node[i] = cur
                
    x = end_node
    while True:
        x = adj_node[x]
        if x is None:
            print("")
            break
        shortest_path.append(x)
    return shortest_path

def part2(data):
    return 0
     
def test():
    out = read_input(file='input/test_input.txt')
    start_time = time.perf_counter()
    print('Result for part 1 in test: ', part1(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    start_time = time.perf_counter()
    print('Result for part 2 in test: ', part2(out, 40))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''    

if __name__ == '__main__':
    input_matrix = read_input()
    test()
    
    start_time = time.perf_counter()
    print('Result for part 1: ', part1(input_matrix))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    start_time = time.perf_counter()
    print('Result for part 2: ', part2(input_matrix, 40))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''