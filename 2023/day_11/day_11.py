import os
from glob import glob
from functools import wraps
from time import time
import numpy as np

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f'{f.__name__} took: {((te-ts))*1000:.4f} ms')
        return result
    return wrap

@timing
def read_input(input_file) -> np.ndarray:
    
    with open(input_file, "r") as f:
        lines=f.readlines()
        n = len(lines)
        m = len(lines[0])-1 # -1 to remove newline char
        in_array = np.zeros((n,m), dtype=np.str_)
        for j, line in enumerate(lines):
            for i, char in enumerate(line.strip()):
                in_array[j][i] = char
    return in_array

def mprint(matrix: np.ndarray):
    for row in matrix:
        print("".join(row))

@timing
def pt1(input, enlarge_by=1):
    # create expanded matrix
    expanded_input = input.copy()
    # find expanding rows and columns

    expanding_rows = []
    for i, row in enumerate(input):
        if not "#" in row:
            expanding_rows.append(i)

    # add a row for each expanding row next to the row to be expanded
    rows_expanded = 0
    for row in expanding_rows:
        for i in range(enlarge_by-1):
            expanded_input = np.insert(expanded_input, row+1+rows_expanded, ".", axis=0)
            rows_expanded += 1
        
    expanding_cols = []
    for i, col in enumerate(expanded_input.T):
        if not "#" in col:
            expanding_cols.append(i)
    # add a col for each expanding col next to the col to be expanded
    cols_expanded = 0
    for col in expanding_cols:
        for i in range(enlarge_by-1):
            expanded_input = np.insert(expanded_input, col+1+cols_expanded, ".", axis=1)
            cols_expanded += 1

    # find the galaxies in the input, store their coordinates
    galaxy_coords = np.column_stack(np.where(expanded_input == "#"))
    
    # replace the galaxies with numbers
    for i, coord in enumerate(galaxy_coords):
        expanded_input[coord[0]][coord[1]] = i+1
    
    # create adjecency matrix with ints being nodes and . being edges
    adj_matrix = np.zeros((len(galaxy_coords), len(galaxy_coords)), dtype=np.int_)
    for i, coord in enumerate(galaxy_coords):
        # calculate distance to the each galaxy
        for j, coord2 in enumerate(galaxy_coords):
            if i == j:
                continue
            else:
                adj_matrix[i][j] = abs(coord[0]-coord2[0]) + abs(coord[1]-coord2[1])

    # get the sum between all galaxies (//2 to remove duplicates)
    print(f"Result Part 1: {adj_matrix.sum()//2}")

@timing
def pt2(input):
    # find empty rows
    expanding_rows = []
    for i, row in enumerate(input):
        if not "#" in row:
            expanding_rows.append(i)
    # find empty cols
    expanding_cols = []
    for i, col in enumerate(input.T):
        if not "#" in col:
            expanding_cols.append(i)
    # find the galaxies in the input, store their coordinates
    galaxy_coords = np.column_stack(np.where(input == "#"))
    # create adjecency matrix with ints being nodes and . being edges
    adj_matrix = np.zeros((len(galaxy_coords), len(galaxy_coords)), dtype=np.int_)
    adj_matrix_old = np.zeros((len(galaxy_coords), len(galaxy_coords)), dtype=np.int_)
    
    for i, coord in enumerate(galaxy_coords):
        # calculate distance to the each galaxy
        for j, coord2 in enumerate(galaxy_coords):
            if i == j:
                continue
            else:
                # amount of empty cols and rows between the two galaxies
                cols_between = range(coord[1]+1, coord2[1])
                print(f"cols between: {cols_between}")
                empty_cols = len([col for col in expanding_cols if col in cols_between])
                rows_between = range(coord[0]+1, coord2[0])
                print(f"rows between: {cols_between}")
                empty_rows = len([row for row in expanding_rows if row in rows_between])
                curr_dist = abs(coord[0]-coord2[0]) + abs(coord[1]-coord2[1])
                adj_matrix_old[i][j] = curr_dist
                adj_matrix[i][j] = curr_dist - (empty_rows + empty_cols) + 10*(empty_rows + empty_cols)
                print(f"empty cols: {empty_cols}, empty rows: {empty_rows} between {i+1} and {j+1}")
                print(f"curr_dist: {adj_matrix_old[i][j]}, new_dist: {adj_matrix[i][j]}")

    print(f"Result Part 2: {adj_matrix.sum()//2}")

def main():
    test_input_file = glob(os.path.join(os.path.dirname(__file__), "input", "test.txt"))[0]
    input_file = glob(os.path.join(os.path.dirname(__file__), "input", "input.txt"))[0]
    # pt 1
    pt1(read_input(test_input_file))
    pt1(read_input(input_file))    
    # pt 2
    #pt1(read_input(test_input_file), enlarge_by=10)
    pt2(read_input(test_input_file))

if __name__ == '__main__':
    main()
