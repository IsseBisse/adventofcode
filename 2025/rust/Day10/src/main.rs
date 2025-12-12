use std::fs;
use std::io;
use std::collections::HashMap;
use std::collections::HashSet;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn parse_target(s: &str) -> u32 {
    let mut target: u32 = 0;
    for (idx, char) in s.chars().enumerate() {
        if char == '#' {
            target += 1 << (idx - 1)
        }
    }
    target
}

fn parse_button(s: &str) -> u32 {
    let numbers = s.get(1..s.len()-1).unwrap();
    let bits = numbers
        .split(",")
        .map(|p| p.parse::<u32>().unwrap())
        .collect::<Vec<u32>>();

    let mut button: u32 = 0;
    for b in bits {
        button += 1 << b
    }
    button
}

fn parse_joltage(s: &str) -> Vec<u32> {
    let numbers = s.get(1..s.len()-1).unwrap();
    numbers
        .split(",")
        .map(|p| p.parse::<u32>().unwrap())
        .collect::<Vec<u32>>()
}

fn parse(row: &String) -> (u32, Vec<u32>) {
    let parts = row.split(" ").collect::<Vec<&str>>();

    let target_string = parts[0];
    let target = parse_target(target_string);

    let buttons_string = parts[1..parts.len()-1].to_vec();
    let buttons = buttons_string
        .iter()
        .map(|&s| parse_button(s))
        .collect::<Vec<u32>>();

    (target, buttons)
}

fn press(state: &u32, buttons: &Vec<u32>) -> Vec<u32> {
    buttons
        .iter()
        .map(|b| state ^ b)
        .collect::<Vec<u32>>()
}

fn find_fewest_total_presses(target: &u32, buttons: &Vec<u32>) -> u32 {
    let mut current_states = HashSet::new();
    current_states.insert(0 as u32);

    let mut all_visited_states: HashMap<u32, u32> = HashMap::new();
    all_visited_states.insert(0, 0);

    let mut presses: u32 = 1;
    while current_states.len() > 0 {
        let new_states = current_states
            .iter()
            .flat_map(|state| {
                press(state, &buttons)
            })
            .collect::<Vec<u32>>();

        let mut new_unvisited_states = HashSet::new();
        for state in new_states {
            if !all_visited_states.contains_key(&state) {
                all_visited_states.insert(state, presses);
                new_unvisited_states.insert(state);
            }
        }

        if all_visited_states.contains_key(&target) {
            // println!("{:?}", all_visited_states);
            return all_visited_states[&target]
        }

        current_states = new_unvisited_states;
        presses += 1;
    }

    0
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let (targets, buttons): (Vec<u32>, Vec<Vec<u32>>) = rows
        .iter()
        .map(|row| parse(row))
        .unzip();

    let total_presses = targets
        .iter()
        .zip(buttons)
        .map(|(t, b)| find_fewest_total_presses(t, &b))
        .sum::<u32>();

    println!("Total button presses: {}", total_presses);
}


fn parse_two(row: &String) -> (Vec<Vec<u32>>, Vec<u32>) {
    let parts = row.split(" ").collect::<Vec<&str>>();
    
    let buttons_string = parts[1..parts.len()-1].to_vec();
    let buttons = buttons_string
        .iter()
        .map(|&s| parse_joltage(s))
        .collect::<Vec<Vec<u32>>>();

    let joltage_string = parts[parts.len()-1];
    let joltage = parse_joltage(joltage_string);

    (buttons, joltage)
}

fn to_joltage(button: &Vec<u32>, length: u32) -> Vec<u32> {
    let mut joltage: Vec<u32> = vec![0; length as usize];
    for &bit in button {
        joltage[bit as usize] = 1;
    }
    joltage
}

fn add(a: &Vec<u32>, b: &Vec<u32>) -> Vec<u32> {
    a
        .iter()
        .zip(b)
        .map(|(first, second)| first + second)
        .collect::<Vec<u32>>()
}

fn any_gt(a: &Vec<u32>, b: &Vec<u32>) -> bool {
    a
        .iter()
        .zip(b)
        .any(|(first, second)| first > second)
}

fn find_fewest_total_presses_two(target: &Vec<u32>, buttons: &Vec<Vec<u32>>) -> u32 {
    let mut current_states = HashSet::new();
    let start_state: Vec<u32> = vec![0; target.len()];
    current_states.insert(start_state);

    let mut all_visited_states: HashMap<Vec<u32>, u32> = HashMap::new();
    let start_state: Vec<u32> = vec![0; target.len()];
    all_visited_states.insert(start_state, 0);

    let mut presses: u32 = 1;
    while current_states.len() > 0 {
        let new_states = current_states
            .iter()
            .flat_map(|state| {
                buttons
                    .iter()
                    .map(|b| add(state, b))
            })
            .collect::<Vec<Vec<u32>>>();

        let mut new_unvisited_states = HashSet::new();
        for state in new_states.iter() {
            if !all_visited_states.contains_key(state) {
                all_visited_states.insert(state.to_vec(), presses);

                if !any_gt(state, target) {
                    new_unvisited_states.insert(state.to_vec());
                }
            }
        }

        if all_visited_states.contains_key(target) {
            // println!("{:?}", all_visited_states);
            return all_visited_states[target]
        }

        current_states = new_unvisited_states;
        presses += 1;
    }

    0
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
    
    let mut buttons = Vec::with_capacity(rows.len());
    let mut joltages = Vec::with_capacity(rows.len());

    for row in &rows {
        let (button, j) = parse_two(row);
        let button_joltages = button
            .iter()
            .map(|b| to_joltage(b, j.len() as u32))
            .collect::<Vec<Vec<u32>>>();
        buttons.push(button_joltages);
        joltages.push(j);

        // println!("{:?}", buttons);
        // println!("{:?}", joltages);
    }
    
    let total_presses = joltages
        .iter()
        .zip(buttons)
        .map(|(j, b)| find_fewest_total_presses_two(j, &b))
        .sum::<u32>();
    println!("Total button presses: {}", total_presses);
}

fn main() {
    // part_one();
    part_two();
}