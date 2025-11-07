use std::collections::HashMap;
use std::fs;
use std::io;

use regex::Regex;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn parse(row: &str) -> ([i32; 2], [i32; 2]) {
    let re = Regex::new(r"(-*\d+),(-*\d+)").unwrap();
    let robot = re.captures_iter(row)
        .map(|c| c.extract())
        .map(|(_, [x, y])| {
            [x.parse::<i32>().unwrap(),
            y.parse::<i32>().unwrap()]
        })
        .collect::<Vec<[i32; 2]>>();

    (robot[0], robot[1])
}

fn modulo(a: i32, b: i32) -> i32 {
    return ((a % b) + b) % b
}

//const DIM: [i32; 2] = [7, 11];
const DIM: [i32; 2] = [101, 103];
fn calculate_position(pos: &[i32; 2], vel: &[i32; 2], steps: i32) -> [i32; 2] {
    let x: i32 = modulo(pos[0] + vel[0] * steps,  DIM[0]);
    let y: i32 = modulo(pos[1] + vel[1] * steps,  DIM[1]);
    [x, y]
}

#[derive(Eq, Hash, PartialEq)]
enum Quadrant {
    First,
    Second,
    Third,
    Fourth
}
fn quadrant(position: &[i32; 2]) -> Option<Quadrant> {
    let x_divider: i32 = DIM[0] / 2;
    let y_divider: i32 = DIM[1] / 2;

    if position[0] < x_divider {
        if position[1] < y_divider {
            return Some(Quadrant::First)
        } else if position[1] > y_divider {
            return Some(Quadrant::Third)
        }
    } else if position[0] > x_divider {
        if position[1] < y_divider {
            return Some(Quadrant::Second)
        } else if position[1] > y_divider {
            return Some(Quadrant::Fourth)
        }
    }

    None
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let robots = rows.iter()
        .map(|row| parse(row))
        .collect::<Vec<([i32; 2], [i32; 2])>>();

    let positions = robots.iter()
        .map(|(pos, vel)| calculate_position(pos, vel, 100))
        .collect::<Vec<[i32; 2]>>();

    let quadrant_counts: HashMap<Quadrant, usize> = positions.iter()
        .filter_map(|pos| quadrant(pos))
        .fold(HashMap::new(), |mut acc, item| {
            *acc.entry(item).or_insert(0) += 1;
            acc
        });

    let safety_factor: usize = quadrant_counts.iter()
        .map(|(_, count)| count)
        .product();

    println!("{}", safety_factor);
}

fn variance(positions: &Vec<[i32; 2]>, axis: usize) -> f32 {
    let mean: f32 = positions.iter()
        .map(|pos| pos[axis])
        .sum::<i32>() as f32 / positions.len() as f32;
    
    let var = positions.iter()
        .map(|pos| (pos[axis] as f32 - mean).powf(2.0))
        .sum::<f32>() / positions.len() as f32;

    var
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let robots = rows.iter()
        .map(|row| parse(row))
        .collect::<Vec<([i32; 2], [i32; 2])>>();
    for steps in 1..10000 {
        let positions = robots.iter()
            .map(|(pos, vel)| calculate_position(pos, vel, steps))
            .collect::<Vec<[i32; 2]>>();

        let var_x = variance(&positions, 0);
        let var_y = variance(&positions, 1);

        if var_x < 500.0 && var_y < 500.0 {
            println!("{}: {}, {}", steps, var_x, var_y)
        }
    }

    println!("Done!")
}

fn main() {
    //part_one();
    part_two();
}