import os
from glob import glob
from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f'{f.__name__} took: {(te-ts):.4f} sec')
        return result
    return wrap

@timing
def read_input(input_file):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
        instructions = lines[0]
        network_nodes = lines[2::]
        network_graph = {node.split(" = ")[0]:
                            {"left": node.split(" = ")[1].split(", ")[0].strip("()"),
                            "right": node.split(" = ")[1].split(", ")[1].strip("()")
                            } for node in network_nodes}
    return instructions, network_graph

@timing
def pt1(input):
    curr_node = "AAA"
    instructions, network_nodes = input
    steps = 0
    i = 0
    while curr_node != 'ZZZ':
        #print("instructions to go: ", instructions[i::])
        if instructions[i] == 'L':
            next_node = network_nodes.get(curr_node).get("left")
        else:
            next_node = network_nodes.get(curr_node).get("right")
        steps +=1
        #print(f"curr_node: {curr_node}, next_node: {next_node}")
        if next_node == "ZZZ":
            break
        curr_node = next_node
        i+=1
        if i >= len(instructions):
            # repeat the instructions if ZZZ is not reached with the last instruction
            instructions += instructions
        
    print(f"Result Part 1: {steps}")

@timing
def pt2(input):
    instructions, network_nodes = input
    curr_nodes = [node for node in network_nodes.keys() if node.endswith("A")]
    print(f"starting nodes: {curr_nodes}")
    steps = 0
    i = 0
    while True:
        #print(f"\nstarting round {i}:")
        #print(f"starting with {len(instructions[i::])} instructions: {instructions[i::]}")
        if len(instructions[i::]) == 0:
            # repeat the instructions if the next node reached does not end on Z with the last instruction
            instructions += instructions
            #print(f"added new instructions: {instructions}")
        to_get = "left" if instructions[i] == 'L' else "right"
        next_nodes = []
        for curr_node in curr_nodes:
            next_node = network_nodes.get(curr_node).get(to_get)
            #print(f"curr_node: {curr_node}, next_node: {next_node}, which is {to_get}")
            next_nodes.append(next_node)
        curr_nodes = next_nodes
        i += 1
        steps +=1
        #print(f"next_nodes: {curr_nodes}")
        if all(node.endswith('Z') for node in curr_nodes):
            print("breaking, all nodes end on Z")
            break
        
        if i >= 10000:
            print("breaking, too many steps")
            print(f"ending with state: {curr_nodes}, steps: {steps}, {len(instructions[i::])} instructions left")
            break
        
        #print(f"{len(instructions[i::])} instrucions left: {instructions[i::]}")
    
    print(f"Result Part 2: {steps}")

def main():
    test_input_file = glob(os.path.join(os.path.dirname(__file__), "input", "test.txt"))[0]
    test_input_file2 = glob(os.path.join(os.path.dirname(__file__), "input", "test2.txt"))[0]
    test_input_filept2 = glob(os.path.join(os.path.dirname(__file__), "input", "testpt2.txt"))[0]
    input_file = glob(os.path.join(os.path.dirname(__file__), "input", "input.txt"))[0]
    # pt 1
    #pt1(read_input(test_input_file))
    #pt1(read_input(test_input_file2))
    #pt1(read_input(input_file))
    # pt 2
    pt2(read_input(test_input_filept2))
    pt2(read_input(input_file))

    
    

if __name__ == '__main__':
    main()
