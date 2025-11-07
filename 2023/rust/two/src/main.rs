use std::fs;
use std::io;
use regex::Regex;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn extract_number(round: &str, re: &Regex) -> u32 {
    match re.captures(round) {
        Some(captures) => {
            match &captures[1].parse::<u32>() {
                Ok(number) => {
                    return *number;
                },
                Err(error) => {
                    print!("Error while parsing: {}", error);
                    return 0;
                }

            }
        },
        None => {
            return 0
        }
    }
}

fn parse_game(round: &str) -> Option<[u32; 3]> {
    let re = Regex::new(r"([0-9]+) red").unwrap();
    let red = extract_number(round, &re);

    let re = Regex::new(r"([0-9]+) green").unwrap();
    let green = extract_number(round, &re);
    
    let re = Regex::new(r"([0-9]+) blue").unwrap();
    let blue = extract_number(round, &re);
    
    return Some([red, green, blue])
}

fn parse_line(line: &str) -> Option<Vec<[u32; 3]>> {
    
    match line.split(": ").last() {
        Some(game_string) => {
            let rounds: Vec<[u32; 3]> = game_string.split("; ")
                .filter_map(parse_game)
                .collect::<Vec<[u32; 3]>>();

            return Some(rounds)
        },
        None => {
            return None
        }
    }
}



fn is_possible(game: &Vec<[u32; 3]>, bag: &[u32; 3]) -> bool {
    for round in game {
        for i in 0..3 {
            if round[i] > bag[i] {
                return false
            }     
        }
    }

    return true
}

fn part_one() {
    let file_path = "input.txt";

    let lines = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let mut games: Vec<Vec<[u32; 3]>> = Vec::new();
    for line in lines {
        match parse_line(&line) {
            Some(rounds) => {
                games.push(rounds);
            },
            None => {
                println!("Error parsing game: {}", line)
            }
        }
    }

    let bag: [u32; 3] = [12, 13, 14];
    let mut id_sum = 0;
    for (i, game) in games.iter().enumerate() {
        if is_possible(game, &bag) {
            id_sum += i+1
        }
    }

    println!("{}", id_sum)
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