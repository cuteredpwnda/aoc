import numpy as np

def read_input(file = 'input/raw_input.txt'):
    data = [line.split("-") for line in open(file).read().splitlines()]
    return data

def part1(b):    
    graph = {}

    for x, y in b:
        if x in graph.keys():
            graph[x].append(y)
        else:
            graph[x] = [y]
        if y in graph.keys():
            graph[y].append(x)
        else:
            graph[y] = [x]


    counter = {}
    for x, y in b:
        counter[x] = 0
        counter[y] = 0


    def can_continue(node, visited_list):
        if node.isupper():
            return True
        if visited_list.count(node) >= 1:
            return False
        return True


    def find(node, visited_list):
        for x, y in b:
            if x == node:
                if can_continue(y, visited_list):
                    yield y
            if y == node:
                if can_continue(x, visited_list):
                    yield x

    found = []
    def search(node, visited_list):
        visited_list.append(node)
        if node == "end":
            found.append([x for x in visited_list])
        new_nodes = find(node, visited_list)
        for new_node in new_nodes:
            found.append(search(new_node, visited_list))
            visited_list.pop(-1)

    search('start', [])
    return len(list(filter(None, found)))


def part2(b):
    def can_continue_2(node, visited_list):
        if node.isupper():
            return True
        if visited_list.count(node) < 1:
            return True
        for item in visited_list:
            if item.islower() and visited_list.count(item) > 1:
                return False
        if node not in ['start', 'end']:
            return True
        return False

    def find(node, visited_list):
        for x, y in b:
            if x == node:
                if can_continue_2(y, visited_list):
                    yield y
            if y == node:
                if can_continue_2(x, visited_list):
                    yield x

    def search_2(node, visited_list):
        visited_list.append(node)
        if node == "end":
            return 1
        new_nodes = find(node, visited_list)
        count = 0
        for new_node in new_nodes:
            count += search_2(new_node, visited_list)
            visited_list.pop(-1)
        return count

    return search_2('start', [])

def test():
    out = read_input(file='input/test_input.txt')
    print(part1(out))
    #m, res = part1(out)
    #print('Result for part 1: ', res, 'Matrix: \n', m)
    print(part2(out))
    #print('Result for part 2: ', res2, 'Matrix: \n', m2)

if __name__ == '__main__':
    input_matrix = read_input()
    #test()
    #m, res = part1(input_matrix)
    print('Result for part 1: ', part1(input_matrix))
    #m2, res2 = part2(input_matrix)
    print('Result for part 2: ', part2(input_matrix))