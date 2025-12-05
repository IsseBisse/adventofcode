use std::fs;
use std::io;
use std::ops::Range;
use std::cmp::max;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn parse(rows: Vec<String>) -> (Vec<Range<i64>>, Vec<i64>) {
    let middle_index = rows
        .iter()
        .enumerate()
        .filter(|(_, row)| *row == "")
        .map(|(idx, _)| idx)
        .collect::<Vec<usize>>()[0];

    let ranges = rows[..middle_index]
        .iter()
        .map(|row| {
            let values = row
                .split("-")
                .map(|val| val.parse::<i64>().unwrap())
                .collect::<Vec<i64>>();
            values[0]..values[1]+1
        })
        .collect::<Vec<Range<i64>>>();

    let values = rows[middle_index+1..]
        .iter()
        .map(|row| row.parse::<i64>().unwrap())
        .collect::<Vec<i64>>();

    (ranges, values)
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let (ranges, values) = parse(rows);

    let num_fresh = values
        .iter()
        .filter(|val| {
            ranges
                .iter()
                .any(|range| range.contains(val))
        })
        .count();

    println!("{:?}", ranges);
    println!("{:?}", values);
    println!("{}", num_fresh);
}

fn merge_ranges(mut ranges: Vec<Range<i64>>) -> Vec<Range<i64>> {
    ranges.sort_by(|a, b| (a.start).cmp(&b.start));

    let mut merged_ranges = vec![ranges[0].clone()];
    let mut curr_idx: usize = 0;
    for range in ranges.iter().skip(1) {
        if merged_ranges[curr_idx].contains(&range.start) {
            merged_ranges[curr_idx].end = max(merged_ranges[curr_idx].end, range.end);   
        } else {
            merged_ranges.push(range.clone());
            curr_idx += 1;
        }
    }
    
    merged_ranges
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
    
    let (ranges, _) = parse(rows);
    let merged_ranges = merge_ranges(ranges.clone());

    let total_length = merged_ranges
        .iter()
        .map(|range| range.end - range.start)
        .sum::<i64>();

    // println!("{:?}", ranges);
    // println!("{:?}", merged_ranges);
    println!("{}", total_length)
}

fn main() {
    // part_one();
    part_two();
}