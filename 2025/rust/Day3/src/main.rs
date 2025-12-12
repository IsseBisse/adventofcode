use std::fs;
use std::io;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn max_index(values: &Vec<isize>) -> usize {
    let mut max_val = values[0];
    let mut max_idx = 0;

    for (idx, val) in values.iter().enumerate() {
        if *val > max_val {
            max_val = *val;
            max_idx = idx;
        }
    }

    max_idx
}

fn largest_joltage(bank: &str) -> isize {
    let bank_values = bank
        .chars()
        .map(|char| char.to_string().parse::<isize>().unwrap())
        .collect::<Vec<isize>>();

    let first_index = max_index(&bank_values[..bank_values.len()-1].to_vec());
    let second_index = max_index(&bank_values[first_index+1..].to_vec()) + first_index + 1;

    let joltage = bank_values[first_index] * 10 + bank_values[second_index];
    joltage
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let joltages = rows
        .iter()
        .map(|bank| largest_joltage(bank))
        .collect::<Vec<isize>>();

    let total_joltage: isize = joltages.iter().sum();
    println!("Total joltage: {}", total_joltage)
}

fn largest_joltage_two(bank: &str) -> isize {
    let bank_values = bank
        .chars()
        .map(|char| char.to_string().parse::<isize>().unwrap())
        .collect::<Vec<isize>>();
    
    let mut prev_index: isize = -1;
    let mut joltage: isize = 0;
    let base: isize = 10;
    for digits_left in (0..12).rev() {
        let start_idx = usize::try_from(prev_index+1).ok().unwrap();
        let values = bank_values[start_idx..bank_values.len()-digits_left].to_vec();
        let idx = max_index(&values) + start_idx;

        // println!("{:?}", values);
        // println!("{}", idx);

        prev_index = isize::try_from(idx).ok().unwrap();
        // let exp = digits_left - 1;     
        joltage += base.pow(digits_left.try_into().unwrap()) * bank_values[idx]
    } 

    // println!("{}", joltage);

    joltage
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let joltages = rows
        .iter()
        .map(|bank| largest_joltage_two(bank))
        .collect::<Vec<isize>>();

    let total_joltage: isize = joltages.iter().sum();
    println!("Total joltage: {}", total_joltage)
}

fn main() {
    // part_one();
    part_two();
}