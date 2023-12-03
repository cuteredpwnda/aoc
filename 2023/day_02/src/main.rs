use std::env;
use std::fs;
use std::collections::HashMap;

fn part_1(input: &str) -> u32 {
    /* for each line, parse the line and collect digits and color pairs into a vector for each line
    create a hashmap of the bags and their contents
    get the game number by splitting on a colon, split this substring on a whitespace and take the last element as game no., -> u32
    split on commas to get the records for each game, then split on whitespace to get the number of bags and the color -> (u32, &str)
    */
    let mut games: HashMap<u32, HashMap<&str, u32>> = HashMap::new();
    
    for line in input.lines() {
        let game_no = line.split(": ").next().unwrap().split_whitespace().last().unwrap().parse::<u32>().unwrap();
        let records_str = line.split(": ").last().unwrap();
        let sets: Vec<&str> = records_str.split("; ").collect();
        // create this games hashmap
        let mut game:HashMap<&str, u32> = [
            ("red", 0),
            ("green", 0),
            ("blue", 0)].iter().cloned().collect();
        for set in sets.iter() {
            //split up the set into the different colors pulled
            let set = set.split(", ");
            for item in set {
                // get the number of bags pulled
                let num_bags = item.split_whitespace().next().unwrap().parse::<u32>().unwrap();
                // get the color of the bag pulled
                let color = item.split_whitespace().last().unwrap();
                // if this sets num_bags is greater than the current num_bags for this color, update the num_bags for this color
                let current_num_bags = *game.get(color).unwrap();
                if num_bags > current_num_bags {
                    game.insert(color, num_bags);
                }
            }
        }
        games.insert(game_no, game);
    }

    // check if each game is possible
    let max_values:HashMap<&str, u32> = [
        ("red", 12),
        ("green", 13),
        ("blue", 14)].iter().cloned().collect();

    let possible_games:Vec<u32> = games.iter().filter_map(|(game_no, game)| {
        let is_possible = check_if_game_is_possible(game, &max_values);
        if is_possible {
            Some(*game_no)
        } else {
            None
        }
    }).collect();
    // sum up the possible games' ids and return the sum
    possible_games.iter().sum()
}

fn check_if_game_is_possible(game:&HashMap<&str, u32>, max_values:&HashMap<&str, u32>) -> bool{
    let mut is_possible = true;
    for (color, num_bags) in game.iter() {
        let max_num_bags = *max_values.get(color).unwrap();
        if num_bags > &max_num_bags {
            is_possible = false;
        }
    }
    is_possible
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

    // read the real input
    let input_file = format!("{}/input.txt", input_folder);
    let input = fs::read_to_string(input_file).expect("Should have been able to read the file");
    println!("Solution for real input: {}",part_1(&input));
}
