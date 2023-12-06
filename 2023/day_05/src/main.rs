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

    // parse each soil map into a HashMap with their name as key and a HashMap for their respective values
    let next_lines = lines.collect::<Vec<&str>>();
    let empty_lines_indices: Vec<_> = next_lines.iter().enumerate().filter_map(|(i, &x)| if x.is_empty() { Some(i) } else { None }).collect();
    //println!("next lines: {:?}", next_lines);

    let mut parsed_soil_maps = HashMap::<String, HashMap::<u32, HashMap::<u32, u32>>>::new();

    for i in 0..next_lines.len() {
        if i > empty_lines_indices.len()-1 {
            break;
        }
        let start = empty_lines_indices[i];
        let end = if i == empty_lines_indices.len() - 1 {
            next_lines.len()
        } else {
            empty_lines_indices[i + 1]
        };
        let map_lines = next_lines[start+1..end].to_vec();
        let mut map_name = String::new();
        let mut seed_to_soil_map = HashMap::<u32, HashMap::<u32, u32>>::new();
        for (j, map_line) in map_lines.iter().enumerate() {
            if j == 0{
                map_name = map_line.split(":").next().unwrap().to_string();
                continue;
            }
            else {
                let mut seed_to_soil_line_map = HashMap::<u32, u32>::new();
                let line_vec = map_line.split(" ").collect::<Vec<&str>>();
                let destination_range_start:u32 = line_vec[0].parse().expect("parse error");                
                let source_range_start:u32 = line_vec[1].parse().expect("parse error");
                let range_length:u32 = line_vec[2].parse().expect("parse error");
                for x in 0..destination_range_start {
                    if !seed_to_soil_line_map.contains_key(&x){
                        seed_to_soil_line_map.insert(x, x);
                        // first is the line number, second is the map for that line
                        seed_to_soil_map.insert(1, seed_to_soil_line_map.clone());
                    }
                }
                
                for x in destination_range_start..source_range_start {
                    if !seed_to_soil_line_map.contains_key(&x){
                        seed_to_soil_line_map.insert(x, x+range_length);
                        seed_to_soil_map.insert(1, seed_to_soil_line_map.clone());
                    }
                }
                for x in source_range_start..source_range_start+range_length {
                    if !seed_to_soil_line_map.contains_key(&x){
                        seed_to_soil_line_map.insert(x, destination_range_start + (x as u32 - source_range_start));
                        seed_to_soil_map.insert(1, seed_to_soil_line_map.clone());
                    }
                }
                for x in 0..100{
                    if !seed_to_soil_line_map.contains_key(&x){
                        seed_to_soil_line_map.insert(x, x);
                        seed_to_soil_map.insert(1, seed_to_soil_line_map.clone());
                    }
                }
            }
        }
        parsed_soil_maps.insert(map_name.clone(), seed_to_soil_map);
    }
    //println!("parsed_soil_maps keys: {:?}", parsed_soil_maps.keys());
    //println!("seed to soil map for pt 1: {:?}", parsed_soil_maps.get("seed-to-soil map").unwrap());

    // debugging
    for key in parsed_soil_maps.keys() {
        debug_print(parsed_soil_maps.clone(), &key);
    }
    

    // map the gardeners plan
    println!("seeds: {:?}", seeds_vec);
    /*
    let mut gardeners_plan = HashMap::<u32, (u32, u32, u32, u32, u32, u32)>::new();
    for (i, seed) in seeds_vec.iter().enumerate() {
        let m = &parsed_soil_maps;
        let a = m.get("seed-to-soil map").unwrap().get(&1).unwrap().get(seed).unwrap();
        let b = m.get("soil-to-fertilizer map").unwrap().get(&1).unwrap().get(a).unwrap();
        let c = m.get("fertilizer-to-water map").unwrap().get(&1).unwrap().get(b).unwrap();
        let d = m.get("water-to-light map").unwrap().get(&1).unwrap().get(c).unwrap();
        let e = m.get("light-to-temperature map").unwrap().get(&1).unwrap().get(d).unwrap();
        let f = m.get("temperature-to-humidity map").unwrap().get(&1).unwrap().get(e).unwrap();
        let g = m.get("humidity-to-location map").unwrap().get(&1).unwrap().get(f).unwrap();

        let tuple = (a, b, c, d, e, f, g);
        println!("tuple: {:?}", tuple);
        //gardeners_plan(seed, tuple)        
    }
    */
}

fn debug_print(parsed_soil_maps:HashMap::<String, HashMap::<u32, HashMap::<u32, u32>>>, key: &str){
    let max_key =  parsed_soil_maps.get(key).unwrap().keys().max().unwrap();
    println!("\nDebugging: {}, #{}", key, max_key);
    println!("seed\tsoil");
    for i in 0..=99{
        
        let soil = parsed_soil_maps.get(key).unwrap().get(&max_key).unwrap().get(&i).unwrap();
        println!("{}\t{}", i, soil);
    }
    /*
    for i in 0..=1{
        let soil = parsed_soil_maps.get(key).unwrap().get(&1).unwrap().get(&i).unwrap();
        println!("{}\t{}", i, soil);
    }
    println!("...\t...");
    for i in 48..=51{
        let soil = parsed_soil_maps.get(key).unwrap().get(&1).unwrap().get(&i).unwrap();
        println!("{}\t{}", i, soil);
    }
    println!("...\t...");
    for i in 96..=99{
        let soil = parsed_soil_maps.get(key).unwrap().get(&1).unwrap().get(&i).unwrap();
        println!("{}\t{}", i, soil);
    }
    */
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
