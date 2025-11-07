use std::collections::HashSet;
use std::collections::HashMap;
use std::hash::Hash;
use std::hash::Hasher;
use std::fs;
use std::vec;

fn parse_input(file_path: &str) -> (Coord, Coord, HashSet<Coord>) {
    let contents = fs::read_to_string(file_path).unwrap();
    
    let mut wall_map: HashSet<Coord> = HashSet::new();
    let mut start: Coord = Coord::new(0, 0);
    let mut end: Coord = Coord::new(0, 0);
    for (y, row) in contents.lines().enumerate() {
        for (x, char) in row.chars().enumerate() {
            if char == 'S' {
                start = Coord::new(x as i32, y as i32);
            } else if char == 'E' {
                end = Coord::new(x as i32, y as i32);
            } else if char == '#' {
                wall_map.insert(Coord::new(x as i32, y as i32));
            }
        }
    }

    (start, end, wall_map)
}

#[derive(Clone, Copy, Eq, Hash, PartialEq)]
struct Coord {
    x: i32,
    y: i32,
}

impl Coord {
    fn new(x: i32, y: i32) -> Self {
        Coord{ x, y }
    }

    fn add(&self, other: Coord) -> Coord {
        Coord::new(self.x + other.x, self.y + other.y)
    }

    fn sub(&self, other: Coord) -> Coord {
        Coord::new(self.x - other.x, self.y - other.y)
    }

    fn turn_right(&self) -> Coord {
        Coord::new(self.y, -self.x)
    }
    
    fn turn_left(&self) -> Coord {
        Coord::new(-self.y, self.x)
    }
}

#[derive(Clone, Copy)]
struct Point {
    pos: Coord,
    dir: Coord,
    cost: usize,
}

impl PartialEq for Point {
    fn eq(&self, other: &Self) -> bool {
        self.pos.x == other.pos.x &&
        self.pos.y == other.pos.y &&
        self.dir.x == other.dir.x &&
        self.dir.y == other.dir.y
    }
}

impl Eq for Point {}

impl Hash for Point {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.pos.x.hash(state);
        self.pos.y.hash(state);
        self.dir.x.hash(state);
        self.dir.y.hash(state);
    }
}

#[derive(Eq, PartialEq)]
enum Direction {
    Forward,
    Right,
    Left
}

impl Point {
    fn new(pos: Coord, dir: Coord, cost: usize) -> Self {
        Point{ pos, dir, cost }
    }

    fn step(&self, dir: Direction) -> Point {
        if dir == Direction::Forward {
            return Point::new(self.pos.add(self.dir), self.dir, self.cost+1)
        } else if dir == Direction::Right {
            let new_dir = self.dir.turn_right();
            return Point::new(self.pos.add(new_dir), new_dir, self.cost+1001)

        } else {
            let new_dir = self.dir.turn_left();
            return Point::new(self.pos.add(new_dir), new_dir, self.cost+1001)
        }
    }

    fn adjacent(&self) -> Vec<Point> {
        let directions = vec![Coord::new(1, 0), Coord::new(-1, 0), Coord::new(0, 1), Coord::new(0, -1)];
        let points = directions.iter()
            .map(|dir| Point::new(self.pos.sub(*dir), *dir, 0))
            .collect::<Vec<Point>>();
        points
    }
}

fn path_finder(start: Coord, end: Coord, wall_map: HashSet<Coord>) -> (HashMap<Point, usize>, Point) {
    let mut node_costs: HashMap<Point, usize> = HashMap::new();

    let start_point = Point::new(start, Coord::new(1, 0), 0);
    let mut points_to_check: Vec<Point> = vec![start_point];
    while points_to_check.len() > 0 {
        let current = points_to_check.pop().unwrap();

        let candidates: Vec<Point> = vec![
            current.step(Direction::Forward),
            current.step(Direction::Left),
            current.step(Direction::Right),
            ];

        for cand in candidates {
            if !wall_map.contains(&cand.pos) && &cand.cost < node_costs.get(&cand).unwrap_or(&usize::MAX) {
                points_to_check.push(cand);
                node_costs.insert(cand, cand.cost);
            }
        }
    }

    let end_cost = node_costs.iter()
        .filter(|(point, _)| point.pos == end)
        .map(|(_, cost)| cost)
        .min()
        .unwrap_or(&usize::MAX);

    let end_point = node_costs.clone().into_iter()
        .filter(|(point, cost)| point.pos == end && cost == end_cost)
        .map(|(point, _)| point)
        .collect::<Vec<Point>>();

    (node_costs.clone(), end_point[0])
}

fn part_one() {
    let file_path = "input.txt";

    let (start, end, wall_map) = parse_input(file_path);
    let (node_costs, end_point) = path_finder(start, end, wall_map);
    println!("{}", node_costs.get(&end_point).unwrap())
}

fn num_seats(node_costs: HashMap<Point, usize>, end: Point, start: Coord) -> usize {
    let mut best_path_coords: HashSet<Coord> = HashSet::new();
    best_path_coords.insert(end.pos);

    let mut visited: Vec<Point> = Vec::new();
    let mut points_to_check: Vec<Point> = vec![end];
    while let Some(current) = points_to_check.pop() {
        visited.push(current);
        let adjacent = current.adjacent();

        let min_cost = adjacent.iter().map(|adj| node_costs.get(&adj).unwrap_or(&usize::MAX)).min().unwrap();
        for adj in adjacent {
            if visited.contains(&adj) {
                continue
            }

            if let Some(cost) = node_costs.get(&adj) {
                if cost == min_cost {
                    points_to_check.push(adj);
                    best_path_coords.insert(adj.pos);
                }
            }
        }
    }

    return best_path_coords.len()
}

fn part_two() {
    let file_path = "smallInput.txt";

    let (start, end, wall_map) = parse_input(file_path);
    let (node_costs, end_point) = path_finder(start, end, wall_map);
    let seats = num_seats(node_costs, end_point, start);
    println!("{}", seats)
}

fn main() {
    // part_one();
    part_two();
}