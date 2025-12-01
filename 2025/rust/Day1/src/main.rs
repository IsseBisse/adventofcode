use std::fs;
use std::io;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn parse_row(row: &str) -> isize {
    let sign = if row.chars().nth(0).unwrap() == 'R' { 1 } else { -1 };
    let value = row[1..].parse::<isize>().unwrap(); 
    sign * value
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let rotations = rows
        .iter()
        .map(|row| parse_row(row))
        .collect::<Vec<isize>>();

    let initial_position = 50;
    let positions = rotations
        .iter()
        .scan(initial_position, |state, &change| {
            *state += change;
            Some(*state)
        })
        .collect::<Vec<isize>>();

    println!("{:?}", positions);

    let num_zero_stops = positions
        .iter()
        .filter(|&&position| position % 100 == 0)
        .count();

    println!("Dial made {} stops at zero", num_zero_stops)
}

fn count_zero_crossings(prev: isize, current: isize) -> isize {
    (prev.div_euclid(100) - current.div_euclid(100)).abs()
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
    
    let rotations = rows
        .iter()
        .map(|row| parse_row(row))
        .collect::<Vec<isize>>();

    let mut positions: Vec<isize> = vec![50];
    let mut later_positions = rotations
        .iter()
        .scan(50, |state, &change| {
            *state += change;
            Some(*state)
        })
        .collect::<Vec<isize>>();
    positions.append(&mut later_positions);
    
    // println!("{:?}", positions);

    let zero_crossings: isize = positions
        .windows(2)
        .map(|window| {
            let prev = window[0];
            let current = window[1];
            count_zero_crossings(prev, current)
        })
        .sum();

    println!("Dial passed zero {} times", zero_crossings)
}

fn main() {
    // part_one();
    part_two();
}