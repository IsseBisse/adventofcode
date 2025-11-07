use std::collections::{HashMap, HashSet};
use std::fs;
use std::fmt;


fn parse_input(file_path: &str) -> (Warehouse, Vec<char>) {
    let input = fs::read_to_string(file_path).unwrap();
    let parts = input.split("\r\n\r\n")
        .collect::<Vec<&str>>();
    
    let moves = parts[1].replace("\r\n", "").chars().collect::<Vec<char>>();

    let mut walls: HashSet<[i32; 2]> = HashSet::new();
    let mut boxes: HashSet<[i32; 2]> = HashSet::new();
    let mut robot: [i32; 2] = [0, 0];
    let mut dim: [i32; 2] = [0, 0];

    for (y, row) in parts[0].to_string().lines().enumerate() {
        dim = [row.len() as i32, y as i32 + 1];

        for (x, char) in row.chars().enumerate() {
            if char == '#' {
                walls.insert([x as i32, y as i32]);
            } else if char == '@' {
                robot = [x as i32, y as i32];
            } else if char == 'O' {
                boxes.insert([x as i32, y as i32]);
            }
        }
    }
    let warehouse = Warehouse::new(robot, boxes, walls, dim);

    (warehouse, moves)
}

struct Warehouse {
    robot: [i32; 2],
    boxes: HashSet<[i32; 2]>,
    walls: HashSet<[i32; 2]>,
    dim: [i32; 2],
}

fn add(first: &[i32; 2], second: &[i32; 2]) -> [i32; 2] {
    [first[0] + second[0], first[1] + second[1]]
}

fn sub(first: &[i32; 2], second: &[i32; 2]) -> [i32; 2] {
    [first[0] - second[0], first[1] - second[1]]
}

impl Warehouse {
    fn new(robot: [i32; 2], boxes: HashSet<[i32; 2]>, walls: HashSet<[i32; 2]>, dim: [i32; 2]) -> Self {
        Warehouse{ robot, boxes, walls, dim} 
    }

    fn box_sum(&self) -> i32 {
        let mut sum: i32 = 0;
        for w_box in &self.boxes {
            sum += w_box[0] + 100*w_box[1]
        }
        sum
    }

    fn move_robot(&mut self, dir_char: char) {
        let directions: HashMap<char, [i32; 2]> = HashMap::from([
            ('^', [0, -1]),
            ('v', [0, 1]),
            ('>', [1, 0]),
            ('<', [-1, 0]),
        ]);
        let direction = directions[&dir_char]; 
        
        // Look ahead
        let mut current_position = add(&self.robot, &direction);
        let mut passed_boxes: Vec<[i32; 2]> = Vec::new();
        while self.boxes.contains(&current_position) {            
            passed_boxes.push(current_position);
            current_position = add(&current_position, &direction);
        }
        // Move one step extra if we didn't "hit" a wall
        if !self.walls.contains(&current_position) {
            current_position = add(&current_position, &direction);
        }

        // Move passed boxes
        let mut new_passed_boxes: Vec<[i32; 2]> = Vec::new();
        for passed_box in passed_boxes {
            current_position = sub(&current_position, &direction);
            self.boxes.remove(&passed_box);
            new_passed_boxes.push(current_position);
        }
        for passed_box in new_passed_boxes {
            self.boxes.insert(passed_box);
        }

        // Update robot position
        current_position = sub(&current_position, &direction);
        self.robot = current_position;
    }
}

impl fmt::Display for Warehouse {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        for y in 0..self.dim[1] {
            for x in 0..self.dim[0] {
                let pos = &[x, y];

                if self.boxes.contains(pos) {
                    write!(f, "O");
                } else if self.walls.contains(pos) {
                    write!(f, "#");
                } else if &self.robot == pos {
                    write!(f, "@");
                } else {
                    write!(f, ".");
                }
            }

            writeln!(f, "");
        }

        Ok(())
    }
}

fn part_one() {
    let file_path = "input.txt";

    let (mut warehouse, moves) = parse_input(file_path);
    //println!("{}", warehouse);
    for dir_char in moves {
        warehouse.move_robot(dir_char);
    }
    //println!("{}", warehouse);
    println!("{}", warehouse.box_sum())
}

fn part_two() {

}

fn main() {
    part_one();
    part_two();
}