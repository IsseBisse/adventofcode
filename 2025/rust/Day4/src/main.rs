use std::fs;
use std::io;
use std::collections::HashSet;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct coord {
    x: isize,
    y: isize
}

impl coord {
    fn adjecent(&self) -> Vec<coord> {
        let adjacent = (-1..2)
            .map(|x| {
                (-1..2)
                    .map(|y| coord { x: self.x + x, y: self.y + y })
                    .filter(|coord| coord != self)
                    .collect::<Vec<coord>>()
            })
            .collect::<Vec<Vec<coord>>>()
            .into_iter()
            .flatten()
            .collect::<Vec<coord>>();
        adjacent
    }
}

fn get_forklift_available_coords(coords: &HashSet<coord>) -> Vec<coord> {
    let forklift_available_coords = coords
        .iter()
        .filter(|&coord| {
            let adjacent = coord.adjecent();
            let occupied_adjacent = adjacent
                .iter()
                .filter(|&adj_coord| coords.contains(adj_coord))
                .count();
            occupied_adjacent < 4        
        })
        .cloned()
        .collect::<Vec<coord>>();
    forklift_available_coords
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let mut coords = HashSet::new();
    for (y, row) in rows.iter().enumerate() {
        for (x, char) in row.chars().enumerate() {
            if char == '@' {
                coords.insert(coord { x: x.try_into().unwrap(), y: y.try_into().unwrap() });
            }
        }
    }

    let forklift_available_coords = get_forklift_available_coords(&coords);

    let total_available = forklift_available_coords.len();

    // println!("{:?}", forklift_available_coords);
    println!("{:?}", total_available);
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
    
    let mut coords = HashSet::new();
    for (y, row) in rows.iter().enumerate() {
        for (x, char) in row.chars().enumerate() {
            if char == '@' {
                coords.insert(coord { x: x.try_into().unwrap(), y: y.try_into().unwrap() });
            }
        }
    }

    let mut removed: usize = 0;
    while true {
        let forklift_available_coords = get_forklift_available_coords(&coords);

        if forklift_available_coords.len() == 0 {
            break
        }

        removed += forklift_available_coords.len();
        for available_coord in forklift_available_coords {
            coords.remove(&available_coord);
        }
    }

    // println!("{:?}", forklift_available_coords);
    println!("{:?}", removed);
}

fn main() {
    part_one();
    part_two();
}