use std::fs;
use std::io;
use std::error::Error;
use std::num::ParseIntError;
use regex::Regex;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.split("\r\n\r\n").map(String::from).collect())
}

struct Range {
    dest_start: i32,
    source_start: i32,
    len: i32
}

struct RangeMapper {
    ranges: Vec<Range>
}

impl RangeMapper {
    fn new(ranges: Vec<Range>) -> Self {
        RangeMapper { ranges }
    }

    fn map(&self, value: i32) {
        
    }
}

fn parse_range_mapper(string: &String) -> Result<RangeMapper, ParseIntError> {
    let re = Regex::new(r"\d+").unwrap();
    
    let mut ranges: Vec<Range>;
    for line in string.lines().skip(1) {
        let range: Result<Vec<i32>, _> = re.find_iter(line)
            .map(|m| m.as_str().parse::<i32>())
            .collect();

        ranges.push(Range {dest_start: range?[0], source_start: range?[1], len: range?[2]} )
    }

    return Ok(RangeMapper::new(ranges))
}

fn parse_input(rows: Vec<String>) -> io::Result<(Vec<i32>, Vec<RangeMapper>)> {
    let re = Regex::new(r"\d+").unwrap();
    let seeds: Result<Vec<i32>, _> = re.find_iter(rows[0])
        .map(|m| m.as_str().parse::<i32>())
        .collect();

    let mut range_mappers: Vec<RangeMapper>;
    for row in rows.iter().skip(1) {
        let range_mapper = parse_range_mapper(row);
        range_mappers.push(range_mapper?);
    }

    return Ok((seeds?, range_mappers))
}

fn part_one() {
    let file_path = "smallInput.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let (seeds, range_mappers) = parse_input(rows).unwrap_or_else(|error| {
        println!("Error parsing input: {}", error);
        std::process::exit(1)
    });

    println!("{}", seeds[0]);
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