use core::num;
use std::fs;
use std::io;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn parse(row: &str) -> Vec<i32> {
    let numbers: Vec<i32> = row.split_whitespace().map(|num| num.parse::<i32>().unwrap()).collect();
    numbers
}

const MIN_DIFFERENCE: i32 = 1;
const MAX_DIFFERENCE: i32 = 3;

struct CheckResult {
    is_increasing: bool,
    is_safe_difference: bool
}

fn check(first: i32, second: i32) -> CheckResult {
    CheckResult{
        is_increasing: first < second,
        is_safe_difference: (MIN_DIFFERENCE..=MAX_DIFFERENCE).contains(&(first - second).abs())
    }
}

fn is_safe(report: &[i32]) -> bool {
    let CheckResult {is_increasing: first_increasing, is_safe_difference: first_safe} = check(report[0], report[1]);
    if !first_safe {
        return false
    }

    report[1..].windows(2).all(|window| {
        let CheckResult {is_increasing, is_safe_difference} = check(window[0], window[1]);
        first_increasing == is_increasing && is_safe_difference
    })
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let reports: Vec<Vec<i32>> = rows.iter().map(|row| parse(row)).collect();
    let num_safe_reports = reports.iter()
        .filter(|&report| is_safe(report))
        .count();
    println!("{}", num_safe_reports)
}

fn permutate(report: &[i32]) -> Vec<Vec<i32>> {
    let mut result = Vec::new();
    
    result.push(report.to_vec());

    for i in 0..report.len() {
        let mut new_perm = report.to_vec();
        new_perm.remove(i);
        result.push(new_perm);
    }

    result
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });


    let reports: Vec<Vec<i32>> = rows.iter().map(|row| parse(row)).collect();

    let permutations: Vec<Vec<Vec<i32>>> = reports.iter().map(|report| permutate(report)).collect();
    let num_safe_reports = permutations.iter()
        .filter(|permutations| {
            permutations.iter().any(|report| is_safe(report))
        })
        .count();
    println!("{}", num_safe_reports)
}

fn main() {
    part_one();
    part_two();
}