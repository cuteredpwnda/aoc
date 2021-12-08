import numpy as np
import itertools

# create a fish with (name, internal_timer, age)
# initial value of internal timer at creation is 2 

class seven_segment_display:
    

    def __init__(self):
        self.number = 8
        # fully populated matrix
        self.matrix = np.full((7,6), '.')
        self.character_list = ['a', 'b', 'c', 'd' ,'e', 'f', 'g']

    numberdict = {  0: {"a","b","c","e","f","g"},
                    1: {"c","f"},
                    2: {"a","c","d","e","g"},
                    3: {"a","c","d","f","g"},
                    4: {"b","c","d","f"},
                    5: {"a","b","d","f","g"},
                    6: {"a","b","d","e","f","g"},
                    7: {"a","c","f"},
                    8: {"a","b","c","d","e","f","g"},
                    9: {"a","b","c","d","f","g"}}
    segments = "abcdefg"

    def show(self):
        for row in self.matrix:
            print(row)

def read_input(file = 'input/raw_input.txt'):
    with open(file) as f:
        data = f.readlines()
    input_list = [(set(x[0].split(' ')), x[1].strip('\n').split(' ')) for x in [y.split(' | ') for y in data]]
    return input_list


def part1(input_list):
    # split the second tuple entry and count chars
    split_output_value = ((x[0], x[1].split(' ')) for x in input_list)
    #print(split_output_value)
    # get the thing representing easy values:
    unique_numbers = []
    for v in split_output_value:
        for d in v[1]:
            # 1 : length = 2
            if (len(d) == 2): unique_numbers.append(1)
            # 4 : length = 4
            if (len(d) == 4): unique_numbers.append(4)
            # 7 : length = 3
            if (len(d) == 3): unique_numbers.append(7)
            # 8 : length = 7
            if (len(d) == 7): unique_numbers.append(8)
    print(len(unique_numbers))
    return unique_numbers

def test():
    input= [(set(['acedgfb','cdfbe','gcdfa','fbcad','dab','cefabd','cdfgeb','eafb','cagedb','ab']), ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf'])]
    print(type(input[0]))
    print(part2(input))

def part2(input_list):
    print(input_list)
    output_list = []
    display = seven_segment_display()
    for (input, output) in input_list:
        for cfg in itertools.permutations(display.segments):
            # mapping
            input_map = {new:display.segments[i] for i, new in enumerate(cfg)}
            for digit in input:
                found_bool = True
                out = set(map(lambda x: input_map[x], digit))
                # check if in displays number dict
                if not any(out==a for a in display.numberdict.values()):
                    found_bool = False
                    break
            if found_bool:
                break
        
        # mapping found -> compare to output
        output_value_list = []
        for digit in output:
            output_map = set(map(lambda x: input_map[x], digit))
            for k, v in display.numberdict.items():
                if v == output_map:
                    output_value_list.append(str(k))
                    break
        output_list.append(int(''.join(output_value_list)))
    return sum(output_list)

if __name__ == '__main__':    
    input_list = read_input()
    #part1(input_list)
    #test()
    print('sum of all elements in part2: {}'.format(part2(input_list)))

    
