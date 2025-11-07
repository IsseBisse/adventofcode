use std::fs;

fn get_input(filename: &str) -> Vec<i32> {
    let contents = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");

    let numbers: Vec<i32> = contents
        .split_whitespace()
        .map(|s| s.parse().expect("parse error"))
        .collect();

    return numbers;
}

fn part_one() {

}

fn part_two() {

}

fn main() {
    part_one();
    part_two();
}