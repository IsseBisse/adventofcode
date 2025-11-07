use std::fs;
use std::io;

fn parse_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn calibration_value(line: &str) -> Option<u32> {
    let mut value_string = String::new();
    for c in line.chars() {
        if c.is_numeric() {
            value_string.push(c);
            break;
        }
    }

    for c in line.chars().rev() {
        if c.is_numeric() {
            value_string.push(c);
            break;
        }
    }

    if value_string.len() != 2 {
        return None;
    }

    match value_string.parse::<u32>() {
        Ok(value) => return Some(value),
        Err(_) => return None
    }
}

fn part_one() {
    let file_path = "input.txt";

    let rows = parse_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let mut values: Vec<u32> = Vec::new();
    for row in rows {
        match calibration_value(&row) {
            Some(number) => values.push(number),
            None => println!("No number found!")
        }
    }

    let sum: u32 = values.iter().sum();
    println!("{}", sum)
}

fn part_two() {

}

fn main() {
    part_one();
}