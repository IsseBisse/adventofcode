use core::num;
use std::fs;
use std::io;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn parse(rows: Vec<String>) -> (Vec<Vec<isize>>, Vec<char>) {
    let numbers = rows[..rows.len()-1]
        .iter()
        .map(|row| {
            row
                .split_whitespace()
                .map(|part| part.parse::<isize>().unwrap())
                .collect::<Vec<isize>>()
        })
        .collect::<Vec<Vec<isize>>>();
    let operators = rows[rows.len()-1]
        .chars()
        .filter(|c| !c.is_whitespace())
        .collect::<Vec<char>>();

    let rows = numbers.len();
    let cols = numbers[0].len();

    let transposed = (0..cols)
        .map(|col| {
            (0..rows)
                .map(|row| numbers[row][col])
                .collect::<Vec<isize>>()
        })
        .collect::<Vec<Vec<isize>>>();

    // println!("{:?}", numbers);
    // println!("{:?}", operators);
    // println!("{:?}", transposed);

    (transposed, operators)
}

fn apply(numbers: Vec<isize>, operator: char) -> isize {
    if operator == '*' {
        numbers
            .into_iter()
            .reduce(|a, b| a * b)
            .unwrap()
    } else {
        numbers
            .into_iter()
            .reduce(|a, b| a + b)
            .unwrap()
    }
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let (transposed, operators) = parse(rows);
    let total: isize = transposed
        .into_iter()
        .zip(operators)
        .map(|(numbers, operator)| apply(numbers, operator))
        .sum();
    println!("{}", total)
}

fn parse_two(rows: Vec<String>) -> (Vec<Vec<isize>>, Vec<char>) {
    let transpose_rows = transpose(rows[..rows.len()-1].to_vec());

    let numbers = transpose_rows
        .split(|s| s.trim().is_empty())
        .filter(|group| !group.is_empty())
        .map(|group| {
            group
                .iter()
                .map(|string| string.trim().parse::<isize>().unwrap())
                .collect::<Vec<isize>>()
            })
        .collect::<Vec<Vec<isize>>>();

    // println!("{:?}", numbers);

    let operators = rows[rows.len()-1]
        .chars()
        .filter(|c| !c.is_whitespace())
        .collect::<Vec<char>>();

    (numbers, operators)
}

fn transpose(strings: Vec<String>) -> Vec<String>{
    let chars = strings
        .iter()
        .map(|string| string.chars().collect::<Vec<char>>())
        .collect::<Vec<Vec<char>>>();

    let rows = chars.len();
    let cols = chars[0].len();

    let transposed = (0..cols)
        .map(|col| {
            (0..rows)
                .map(|row| chars[row][col])
                .collect()
        })
        .collect::<Vec<String>>();

    // println!("{:?}", transposed);
    
    transposed
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let (transposed, operators) = parse_two(rows);
    let total: isize = transposed
        .into_iter()
        .zip(operators)
        .map(|(numbers, operator)| apply(numbers, operator))
        .sum();
    println!("{}", total)
}

fn main() {
    // part_one();
    part_two();
}