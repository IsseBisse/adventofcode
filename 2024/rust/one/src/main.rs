use std::fs;
use std::io;
use std::collections::HashMap;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn parse(row: &str) -> (i32, i32) {
    let split = row.split_whitespace().collect::<Vec<&str>>();
    let left = split[0].parse::<i32>().unwrap();
    let right = split[1].parse::<i32>().unwrap();
    (left, right)
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let (mut left, mut right): (Vec<i32>, Vec<i32>) = rows.iter()
        .map(|row| parse(row))
        .unzip();

    left.sort();
    right.sort();

    let dist: i32 = left.into_iter()
            .zip(right)
            .map(|(l, r)| (l-r).abs())
            .sum();
    println!("{}", dist);
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
    
    let (left, right): (Vec<i32>, Vec<i32>) = rows.iter()
        .map(|row| parse(row))
        .unzip();

    let mut scores: HashMap<i32, i32> = HashMap::new();
    for num in right {
        *scores.entry(num).or_insert(0) += 1;
    }

    let score: i32 = left.iter().map(|num| *num * *scores.entry(*num).or_insert(0)).sum();
    println!("{}", score)
}

fn main() {
    part_one();
    part_two();
}