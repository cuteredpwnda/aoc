use std::env;
use std::fs;
use array2d::Array2D;
use std::collections::HashMap;

fn parse_to_matrix(input:&str) -> Array2D<char>{
    let rows = input.split("\n").map(|line| {
        line.chars().collect::<Vec<char>>()
    }).collect::<Vec<Vec<char>>>();
    let matrix = Array2D::from_rows(&rows).expect("Should have been able to create matrix");
    matrix
}

fn check_neighbors(matrix:&Array2D<char>){
   // create a hashmap with the part numbers as keys and the neigbors as list of values
    let mut neighbors:HashMap<u32,Vec<char>> = HashMap::new();
    // extract the part numbers from the matrix
    for row in 0..matrix.num_rows() as i32 {
        for col in 0..matrix.num_columns() as i32 {
            let curr_elem = matrix[(row as usize, col as usize)];
            let mut part_number_vec:Vec<u32> = Vec::new();
            // get all the neighbors into a vector
            let mut neighbor_list:Vec<char> = Vec::new();
            if curr_elem.is_digit(10) {
                println!("curr_elem: {}", curr_elem);
                let curr_digit = curr_elem.to_digit(10).unwrap();
                part_number_vec.push(curr_digit);
                // add the neighbors to the neighbor_list
                for i in -1..=1 as i32{
                    for j in -1..=1 as i32{
                        if i == 0 && j == 0 ||
                            row+i >= matrix.num_rows() as i32 ||
                            col+j >= matrix.num_columns() as i32 ||
                            row+i < 0 ||
                            col+j < 0 {
                            continue;
                        }
                        else {
                            let neighbor_index = ((row+i) as usize, (col+j) as usize);
                            let neighbor = matrix[neighbor_index];                        
                            if !neighbor.is_digit(10) && neighbor != '.' {
                            neighbor_list.push(neighbor);
                            }
                        }
                    }
                }
            } else { // stop here and combine the part numbers into a u32
                println!("found stop character: {}\n combining current part_number {:?}", curr_elem, part_number_vec);
                let mut part_number:u32 = 0;
                for digit in &part_number_vec {
                    part_number = part_number * 10 + digit;
                }
                neighbors.insert(part_number, neighbor_list);
                // clear the part_number_vec
                part_number_vec = Vec::new();
            }
        }
    }
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
