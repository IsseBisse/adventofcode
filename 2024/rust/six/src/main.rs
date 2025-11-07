use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;
use std::io;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

struct BlockMap {
    map: Vec<Vec<bool>>,
    max: Coord,
}

impl BlockMap {
    fn new(map: Vec<Vec<bool>>, max: Coord) -> Self {
        BlockMap{ map, max }
    }

    fn is_blocked(&self, coord: &Coord) -> bool {
        if !self.is_inside(&coord) {
            return false
        }

        self.map[coord.y as usize][coord.x as usize]
    }

    fn is_inside(&self, coord: &Coord) -> bool {
        if coord.x < 0 || coord.y < 0 {
            return false
        }

        if coord.x >= self.max.x || coord.y >= self.max.y {
            return false
        }

        true
    }
}

#[derive(Copy, Clone, Eq, Hash, PartialEq)]
struct Coord {
    x: isize,
    y: isize,
}

impl Coord {
    fn new(x: isize, y: isize) -> Self {
        Coord { x: x, y: y}
    }

}

fn add(first: &Coord, second: &Coord) -> Coord {
    Coord::new(first.x+second.x, first.y+second.y)
}

fn parse_row(row: &str) -> (Vec<bool>, Option<isize>) {
    let mut map_row: Vec<bool> = Vec::new();
    let mut start_x: Option<isize> = None;

    for (i, char) in row.chars().enumerate() {
        if char == '#' {
            map_row.push(true);
        } else if char == '^' {
            start_x = Some(i as isize);
        } else {
            map_row.push(false);
        }    
    }

    (map_row, start_x)
}

fn parse(rows: Vec<String>) -> (BlockMap, Coord) {
    let mut map: Vec<Vec<bool>> = Vec::new();
    let mut start: Coord = Coord::new(-1, -1);
    
    for (start_y, row) in rows.iter().enumerate() {
        let (new_row, start_x) = parse_row(row);
        map.push(new_row);

        if let Some(x) = start_x {
            start = Coord::new(x, start_y as isize)
        }   
    }

    let max = Coord::new(map[0].len() as isize, map.len() as isize);

    (BlockMap::new(map, max), start)
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let directions: [Coord; 4] = [
        Coord::new(0, -1),
        Coord::new(1, 0),
        Coord::new(0, 1),
        Coord::new(-1, 0)
    ];
    let (blocked_map, mut point) = parse(rows);
    let mut visited_map: Vec<Vec<usize>> = blocked_map.map.clone().into_iter()
        .map(|row| {
            row.into_iter().map(|b| b as usize).collect()
    }).collect();
    let mut dir_idx: usize = 0;
    let mut points_visted: HashSet<Coord> = HashSet::new();
    points_visted.insert(point);
    while blocked_map.is_inside(&point) {
        let dir = &directions[dir_idx % 4];
        let new_point = add(&point, dir);

        if blocked_map.is_blocked(&new_point) {
            dir_idx += 1;
        } else {
            point = new_point;
            if blocked_map.is_inside(&point) {
                points_visted.insert(point);
                visited_map[point.y as usize][point.x as usize] = 2
            }
        }

        if dir_idx > 10000 {
            break
        }
    }

    for row in visited_map {
        for visited in row {
            if visited == 1 {
                print!("#")
            } else if visited == 2 {
                print!("X")
            } else {
                print!(".")
            }
        }
        println!("")
    }

    println!("{}", points_visted.len())
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