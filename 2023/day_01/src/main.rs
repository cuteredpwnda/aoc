use std::env;
use std::fs;
use std::collections::HashMap;

fn collect_nums(digits: &Vec<Vec<u32>>) -> Vec<u32>{
    let numbers:Vec<u32> = digits.iter().map(|d| {
        let first = d.first().unwrap();
        let last = d.last().unwrap();
        let number = format!("{}{}", first, last);
        number.parse::<u32>().unwrap()
    }).collect();
    numbers
}

fn part_1(input: &str) {
    // for each line, parse the line and only keep the digits, collect digits into a vector for each line
    let digits:Vec<Vec<u32>> = input.lines().map(|line| {
        line.chars().filter_map(|c| c.to_digit(10)).map(|d| d as u32).collect()
    }).collect();
    //for each vector of digits, concatenate the first and last digit into one number
    let numbers = collect_nums(&digits);
    // add those numbers together
    let sum:u32 = numbers.iter().sum();
    println!("Sum: {}", sum);
}

fn part_2(input: &str){
    // create a map of digit words to their values
    let digit_words:HashMap<&str, u32> = [
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
    ].iter().cloned().collect();

    // parse each line into a vector and map each digit word to its value if possible
    let digits:Vec<Vec<u32>> = input.lines().map(|line| {
        // check if the line contains any digit words
        let contains_digit_words = digit_words.keys().any(|word| line.contains(word));
        // if the line contains digit words then replace first and last found digit word with its value
        if contains_digit_words {
            // find the digit words in the line
            // create a position map of the digit words
            let mut position_map:HashMap<usize, u32> = HashMap::new();
            for (word, _) in digit_words.iter() {
                if line.contains(word) {
                    // save the index of the first letter of the word
                    let indices: Vec<_> = line.match_indices(word).collect();
                    for (index, _) in indices {
                        position_map.insert(index, *digit_words.get(word).unwrap());
                    }
                }
                
            }
            // get the position of the remaining integers in the string and add the position and integer to the position map
            let mut position = 0;
            for c in line.chars() {
                if c.is_digit(10) {
                    position_map.insert(position, c.to_digit(10).unwrap() as u32);
                }
                position += 1;
            }
            // sort the position map by key
            let mut sorted_position_map:Vec<(&usize, &u32)> = position_map.iter().collect();
            sorted_position_map.sort_by(|a, b| a.0.cmp(b.0));
            // return the values of the sorted position map as a vector
            sorted_position_map.iter().map(|(_, value)| **value).collect()

        } else {
            // parse the line into a vector of digits (like in part 1)
            line.chars().filter_map(|c| c.to_digit(10)).map(|d| d as u32).collect()
        }
    }).collect();
    let numbers = collect_nums(&digits);
    // add those numbers together
    let sum:u32 = numbers.iter().sum();
    println!("Sum: {}", sum);
}

fn main() {
    // get parent directory of the current file
    let current_dir = env::current_dir().expect("Should have been able to get the current directory");
    // get the input folder
    let input_folder = format!("{}/input", current_dir.display());
    
    // read the test input
    let test_input_file = format!("{}/test_1.txt", input_folder);
    let test_input = fs::read_to_string(test_input_file).expect("Should have been able to read the file");
    println!("Test input: \n{}", test_input);
    part_1(&test_input);
    println!("Real input:");
    // read the real input
    let real_input_file = format!("{}/input_1.txt", input_folder);
    let real_input = fs::read_to_string(real_input_file).expect("Should have been able to read the file");
    part_1(&real_input);

    println!("\nPart 2");
    // read the test input
    let test_input_file = format!("{}/test_2.txt", input_folder);
    let test_input = fs::read_to_string(test_input_file).expect("Should have been able to read the file");
    println!("Test input: \n{}", test_input);
    part_2(&test_input);

    
    println!("Real input:");
    // read the real input
    let pt2_file = format!("{}/input_1.txt", input_folder);
    let pt_2_input = fs::read_to_string(pt2_file).expect("Should have been able to read the file");
    part_2(&pt_2_input);
}

