use std::fs;
use std::io;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn parse(row: &str) -> Vec<char> {
    row.chars().collect::<Vec<char>>()
}

const DIRECTIONS: [(i32, i32); 8] = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, -1),
    (1, 1),
    (-1, -1),
    (-1, 1),
];

const PATTERN: [char; 3] = ['M', 'A', 'S'];


fn count_xmas(row: usize, col: usize, chars: &Vec<Vec<char>>) -> usize {
    DIRECTIONS.iter()
        .filter(|(r_offset, c_offset)| is_mas(row, col, *r_offset, *c_offset, chars))
        .count()
}

fn is_mas(row: usize, col: usize, r_offset: i32, c_offset: i32, chars: &Vec<Vec<char>>) -> bool {
    for i in 0..3 {
        let r = row as i32 + r_offset*(i+1);
        let c = col as i32 + c_offset*(i+1);

        if r < 0 || c < 0 {
            return false
        }

        if !match_char(chars, r as usize,c as usize, PATTERN[i as usize]) {
            return false
        }
    } 

    return true}

fn match_char(chars: &Vec<Vec<char>>, row: usize, col: usize, pattern_char: char) -> bool {
    match chars.get(row).and_then(|r| r.get(col)) {
        Some(&c) => c == pattern_char,
        None => false
    }
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let chars = rows.iter()
        .map(|row| parse(row))
        .collect::<Vec<Vec<char>>>();

    let mut xmax_count: usize = 0;
    for (row_idx, row) in chars.iter().enumerate() {
        for (col_idx, char) in row.iter().enumerate() {
            if *char == 'X' {
                xmax_count += count_xmas(row_idx, col_idx, &chars);
            }
        }
    }
    println!("{}", xmax_count)
}

const CROSS_DIRECTIONS: [(i32, i32); 4] = [
    (-1, -1),
    (-1, 1),
    (1, 1),
    (1, -1),
];

fn is_x_mas(row: usize, col: usize, chars: &Vec<Vec<char>>) -> bool {
    let mut corner_char: Vec<char> = Vec::new();
    for (r_offset, c_offset) in CROSS_DIRECTIONS {
        match get_cross_char(row, col, r_offset, c_offset, chars) {
            Some(char) => corner_char.push(char),
            None => return false,
        }
    }
    let corners: String = corner_char.iter().collect();
    
    corners == "MMSS" || corners == "SMMS" || corners == "SSMM" || corners == "MSSM"
}

fn get_cross_char(row: usize, col: usize, r_offset: i32, c_offset: i32, chars: &Vec<Vec<char>>) -> Option<char> {
    let r = row as i32 + r_offset;
    let c = col as i32 + c_offset;
    if r < 0 || c < 0 {
        return None
    }

    let row = chars.get(r as usize)?;
    let char = row.get(c as usize)?;
    Some(*char)
} 


fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
    
    let chars = rows.iter()
        .map(|row| parse(row))
        .collect::<Vec<Vec<char>>>();

    let mut xmax_count: usize = 0;
    for (row_idx, row) in chars.iter().enumerate() {
        for (col_idx, char) in row.iter().enumerate() {
            if *char == 'A' && is_x_mas(row_idx, col_idx, &chars){
                xmax_count += 1;
            }
        }
    }
    println!("{}", xmax_count)
}

fn main() {
    part_one();
    part_two();
}