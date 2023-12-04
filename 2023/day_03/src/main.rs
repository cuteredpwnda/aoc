use std::env;
use std::fs;
use array2d::Array2D;

fn parse_to_matrix(input:&str) -> Array2D<char>{
    let rows = input.split("\n").map(|line| {
        line.chars().collect::<Vec<char>>()
    }).collect::<Vec<Vec<char>>>();
    let matrix = Array2D::from_rows(&rows).expect("Should have been able to create matrix");
    matrix
}

fn check_neighbors(matrix:&Array2D<char>){
    
    // get indices of all numbers, iterate full matrix and check if the current index is a number
    let mut part_number_indices = Vec::<(i32, i32)>::new();
    for (j, columns_iter) in matrix.columns_iter().enumerate() {
        for (i, value) in columns_iter.enumerate() {
            if value.is_digit(10) {
                part_number_indices.push((i as i32, j as i32));
            }
        }
    }
    // sort the indices by the first value
    part_number_indices.sort_by(|a, b| a.0.cmp(&b.0));

    // iterate over the indices and check the neighbors of each index
    let mut candidates_indices = Vec::<(i32, i32)>::new();
    for (i, j) in part_number_indices {
        let mut neighbors = Vec::<char>::new();
        // check the neighbors
        for x in i-1..i+2 {
            for y in j-1..j+2 {
                if x < 0 || y < 0 {
                    continue;
                }
                if x >= matrix.num_columns() as i32 || y >= matrix.num_rows() as i32 {
                    continue;
                }
                if x == i && y == j {
                    continue;
                }
                if let Some(value) = matrix.get(x as usize, y as usize) {
                    neighbors.push(*value);
                }
            }
        }
        // remove all '.' from the neighbors
        neighbors.retain(|&x| x != '.');
        // keep only those with neighbors that are not numbers
        neighbors.retain(|&x| !x.is_digit(10));
        if neighbors.len() >= 1 {
            println!("Found a candidate at: ({}, {})", i, j);
            candidates_indices.push((i, j));
        }
    }

    // combine part numbers by combining the digits that are next to each other row by row
    let mut part_numbers = Vec::<String>::new();
    for (index, columns_iter) in matrix.columns_iter().enumerate(){
        let mut part_number_vec = Vec::<String>::new();
        for (i, value) in columns_iter.enumerate() {
            if value.is_digit(10) {                
                part_number_vec.push(*value);
                // check the neighbors
                for x in i+1..matrix.num_columns() {
                    if let Some(value) = matrix.get(x, index) {
                        if value.is_digit(10) {
                            part_number_vec.push(*value);
                        } else {
                            break;
                        }
                    }
                }
                part_numbers.push(part_number);
            }
        }
    }
    println!("Part numbers: {:?}", part_numbers);
}

fn part_1(input:&str) -> u32 {
    let matrix = parse_to_matrix(input);
    check_neighbors(&matrix);
    0   
}

fn main() {
    // get parent directory of the current file
    let current_dir = env::current_dir().expect("Should have been able to get the current directory");
    // get the input folder
    let input_folder = format!("{}/input", current_dir.display());
    
    // read the test input
    let test_input_file = format!("{}/test_1.txt", input_folder);
    let test_input = fs::read_to_string(test_input_file).expect("Should have been able to read the file");
    println!("Solution for test: {}",part_1(&test_input));
}
