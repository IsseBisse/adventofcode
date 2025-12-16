use std::fs;
use std::io;
use fancy_regex::Regex;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn is_valid_id(candidate: &str) -> bool {
    let length = candidate.len();
    if length % 2 != 0 {
        false
    } else {
        candidate[..length/2] == candidate[length/2..]
    }
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let ids = rows[0]
        .split(",")
        .map(|part| part.split("-").collect::<Vec<&str>>())
        .collect::<Vec<Vec<&str>>>();
    let invalid_ids = ids
        .iter()
        .map(|range| {
            let start = range[0].parse::<isize>().unwrap();
            let end = range[1].parse::<isize>().unwrap();
            (start..end)
                .filter(|candidate| is_valid_id(&candidate.to_string()))
        })
        .flatten()
        .collect::<Vec<isize>>();
    let total_invalid: isize = invalid_ids.iter().sum();

    println!("{} is the sum of invalid ids", total_invalid)
}

fn is_repeating_sequence(candidate: &str, num_repeats: usize) -> bool {
    let length = candidate.len();
    if length % num_repeats != 0 {
        false
    } else {
        let chunk_size = length / num_repeats;
        let parts = candidate
            .chars()
            .collect::<Vec<char>>()
            .chunks(chunk_size)
            .map(|chunk| chunk.iter().collect())
            .collect::<Vec<String>>();
        parts
            .windows(2)
            .all(|w| w[0] == w[1])
    }
}

fn is_valid_id_two(candidate: &str) -> bool {
    (2..candidate.len()+1)
        .any(|num_repeats| is_repeating_sequence(candidate, num_repeats))
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let ids = rows[0]
        .split(",")
        .map(|part| part.split("-").collect::<Vec<&str>>())
        .collect::<Vec<Vec<&str>>>();
    let invalid_ids = ids
        .iter()
        .map(|range| {
            let start = range[0].parse::<isize>().unwrap();
            let end = range[1].parse::<isize>().unwrap();
            (start..end+1)
                .filter(|candidate| is_valid_id_two(&candidate.to_string()))
        })
        .flatten()
        .collect::<Vec<isize>>();
    let total_invalid: isize = invalid_ids.iter().sum();

    println!("{} is the sum of invalid ids", total_invalid)
}

fn main() {
    // part_one();
    part_two();
}