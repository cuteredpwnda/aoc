use std::env;
use std::fs;
use std::collections::HashMap;

fn parse_input(input: &str){
    let mut lines = input.lines();
    // parse the seeds into a list of integers
    // seeds are in the first input line
    let seeds_line = lines.next();
    let seeds_str = seeds_line.unwrap().split(": ").last().unwrap();
    let mut seeds_vec = Vec::<u32>::new();
    for seed_str in seeds_str.split(" ") {
        let seed:u32 = seed_str.parse().expect("parse error");
        seeds_vec.push(seed);
    }
    println!("seeds: {:?}", seeds_vec);

    // parse each soil map into a HashMap with their name as key and a HashMap for their respective values

    let mut map_lines = Vec::<&str>::new();
    let next_lines = lines.collect::<Vec<&str>>();
    println!("next lines:\n {:?}", next_lines);
    for map_line in next_lines{
        println!("next map lines:\n {:?}", map_line)
    }

    
}
fn part_1(input: &str) -> u32{
    parse_input(&input);
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
    println!("Part 1 Test solution: {}", part_1(&test_input))
}
