use std::env;
use std::fs;


fn part_1(input: &str) -> u32 {
    let mut result = String::new();
    // create a vector of all the lines with tuples (card number, winning numbers, my numbers)
    let lines = input.split("\n").map(|line| {
        let mut line_split = line.split(": ");
        let card_number = line_split.next().expect("Should have been able to get the card number");
        let numbers = line_split.next().expect("Should have been able to get the numbers");
        let mut numbers_split = numbers.split(" | ");
        let winning_numbers_raw = numbers_split.next().expect("Should have been able to get the winning numbers");
        let my_numbers_raw = numbers_split.next().expect("Should have been able to get my numbers");
        let winning_numbers_str = winning_numbers_raw.split_whitespace().collect::<Vec<&str>>();
        let my_numbers_str = my_numbers_raw.split_whitespace().collect::<Vec<&str>>();
        let winning_numbers = winning_numbers_str.iter().map(|s| s.parse().expect("parse error")).collect::<Vec<u32>>();
        let my_numbers = my_numbers_str.iter().map(|s| s.parse().expect("parse error")).collect::<Vec<u32>>();
        (card_number, winning_numbers, my_numbers)
    }).collect::<Vec<(&str, Vec<u32>, Vec<u32>)>>();
    
    // iterate over the lines and check the count of the winning numbers in my numbers
    let mut scratchbook = Vec::<(String, u32)>::new();
    for (card_number, winning_numbers, my_numbers) in lines {
        let mut count = 0;
        for number in winning_numbers {
            // check if the number is in my numbers
            if my_numbers.contains(&number) {
                count += 1;
            }            
        }
        result.push_str(&format!("{}: {}\n", card_number, count));
        let mut points = 0;
        if count > 0 {
            points = u32::pow(2, count-1);
        }
        
        scratchbook.push((card_number.to_string(), points));
    }
    // add the points together
    let mut total_points = 0;
    for (_, points) in scratchbook {
        total_points += points;
    }
    total_points
}

fn part_2(input: &str) -> u32{
    let mut result = String::new();
    // create a vector of all the lines with tuples (card number, winning numbers, my numbers)
    let lines = input.split("\n").map(|line| {
        let mut line_split = line.split(": ");
        let card_number = line_split.next().expect("Should have been able to get the card number");
        let numbers = line_split.next().expect("Should have been able to get the numbers");
        let mut numbers_split = numbers.split(" | ");
        let winning_numbers_raw = numbers_split.next().expect("Should have been able to get the winning numbers");
        let my_numbers_raw = numbers_split.next().expect("Should have been able to get my numbers");
        let winning_numbers_str = winning_numbers_raw.split_whitespace().collect::<Vec<&str>>();
        let my_numbers_str = my_numbers_raw.split_whitespace().collect::<Vec<&str>>();
        let winning_numbers = winning_numbers_str.iter().map(|s| s.parse().expect("parse error")).collect::<Vec<u32>>();
        let my_numbers = my_numbers_str.iter().map(|s| s.parse().expect("parse error")).collect::<Vec<u32>>();
        (card_number, winning_numbers, my_numbers)
    }).collect::<Vec<(&str, Vec<u32>, Vec<u32>)>>();
    
    //println!("lines: {:?}", lines);

    // iterate over the lines and check the count of the winning numbers in my numbers
    let mut scratchbook = Vec::<(String, u32, u32, u32)>::new();
    for (card_number, winning_numbers, my_numbers) in lines {
        let mut count = 0;
        for number in winning_numbers {
            // check if the number is in my numbers
            if my_numbers.contains(&number) {
                count += 1;
            }            
        }
        result.push_str(&format!("{}: {}\n", card_number, count));
        let mut points = 0;
        if count > 0 {
            points = u32::pow(2, count-1);
        }
        
        scratchbook.push((card_number.to_string(), count, points, 1));
    }

    for i in 0..scratchbook.len() {
        let count = scratchbook[i].1;
        let curr_amount = scratchbook[i].3;
        for j in 1..=count as usize{
            let index = i+j;            
            if index >= scratchbook.len() {
                break;
            }
            let mut amount = scratchbook[index].3;
            amount += 1*curr_amount;
            scratchbook[index].3 = amount;
        }
    }
    // sum of scratchbook amounts
    let mut total_points = 0;
    for (_, _, _, amount) in scratchbook {
        total_points += amount;
    }
    total_points
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

    // read the input
    let input_file = format!("{}/input.txt", input_folder);
    let input = fs::read_to_string(input_file).expect("Should have been able to read the file");
    println!("Solution for part 1: {}",part_1(&input));

    // read the pt 2 test input
    println!("Solution for test 2: {}",part_2(&test_input));
    // read the pt 2 input
    println!("Solution for test 2: {}",part_2(&input));
}
