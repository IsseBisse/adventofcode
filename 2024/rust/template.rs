use std::fs;
use std::io;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn part_one() {
    let file_path = "smallInput.txt";

    let rows = parse_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
}

fn part_two() {
    let file_path = "smallInput.txt";

    let rows = parse_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
}

fn main() {
    part_one();
    part_two();
}