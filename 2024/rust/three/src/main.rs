use std::fs;
use regex::Regex;

fn read_input(file_path: &str) -> String {
    let contents = fs::read_to_string(file_path).unwrap();
    contents
}

fn find_mul(code: &str) -> Vec<(i32, i32)> {
    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();

    let pairs: Vec<(i32, i32)> = re.captures_iter(code)
        .map(|cap| (
            cap[1].parse().unwrap(),
            cap[2].parse().unwrap()
        ))
        .collect();
    pairs
}
 
fn part_one() {
    let file_path = "input.txt";
    let code = read_input(file_path);
    let pairs = find_mul(&code);
    let result: i32 = pairs.iter()
        .map(|(first, second)| first*second)
        .sum();
    println!("{}", result)
}

fn find_enabled(code: &str) -> String {
    let mut enabled_parts = code.split("don't()")
        .map(|part| {
            // Get enabled code, i.e. everything after first "do()"
            part.split("do()")
                .skip(1)
                .collect::<Vec<&str>>()
                .join("")
        })
        .collect::<Vec<String>>();

    let first_part = code.split("don't()").next().unwrap_or("");
    // .push adds last but it doesn't matter here
    enabled_parts.push(first_part.to_string());

    enabled_parts.join("")
}

fn part_two() {
    let file_path = "input.txt";
    let code = read_input(file_path);
    let enabled_code = find_enabled(&code);

    let pairs = find_mul(&enabled_code);
    let result: i32 = pairs.iter()
        .map(|(first, second)| first*second)
        .sum();
    println!("{}", result)
}

fn main() {
    part_one();
    part_two();
}