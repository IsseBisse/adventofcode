use std::fs;
use std::io;
use regex::Regex;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn is_valid_id(candidate: &str) -> bool {
    let re = Regex::new(r"(\d+)+").unwrap();
    re.is_match(candidate)
}

fn part_one() {
    let file_path = "smallInput.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let ids = rows[0]
        .split(",")
        .map(|part| part.split("-"))
        .flatten()
        .collect::<Vec<&str>>();
    let invalid_ids = ids
        .iter()
        .filter(|&&candidate| is_valid_id(candidate))
        .map(|&invalid_id| invalid_id.parse::<isize>().unwrap())
        .collect::<Vec<isize>>();
    let total_invalid: isize = invalid_ids.iter().sum();

    println!("{} is the sum of invalid ids", total_invalid)
}

fn part_two() {
    let file_path = "smallInput.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
}

fn main() {
    part_one();
    part_two();
}