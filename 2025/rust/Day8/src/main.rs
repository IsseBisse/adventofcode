use std::fs;
use std::io;
use std::cmp::Ordering;
use std::collections::BTreeSet;
use std::collections::HashMap;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

#[derive(Hash, Eq, PartialEq, Copy, Clone, Debug)]
struct Point {
    x: i32,
    y: i32,
    z: i32,
    
    connections: Vec<Point>
}

impl Point {
    fn distance(&self, other: &Self) -> f64 {
        let dx = (self.x - other.x) as f64;
        let dy = (self.y - other.y) as f64;
        let dz = (self.z - other.z) as f64;
        (dx * dx + dy * dy + dz * dz).sqrt()
    }
}

#[derive(Debug)]
struct PointPair {
    p1: Point,
    p2: Point,
    distance: f64,
}

impl PointPair {
    fn new(p1: Point, p2: Point) -> Self {
        let distance = p1.distance(&p2);
        PointPair { p1, p2, distance }
    }
}

impl Eq for PointPair {}

impl PartialEq for PointPair {
    fn eq(&self, other: &Self) -> bool {
        self.distance == other.distance
    }
}

impl Ord for PointPair {
    fn cmp(&self, other: &Self) -> Ordering {
        // Use total_cmp for proper f64 comparison
        self.distance.total_cmp(&other.distance)
    }
}

impl PartialOrd for PointPair {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn parse(rows: &Vec<String>) -> Vec<Point> {
    rows
        .iter()
        .map(|s| {
            let values = s
                .split(",")
                .map(|sub_s| sub_s.parse::<i32>().unwrap())
                .collect::<Vec<i32>>();
            Point { x: values[0], y: values[1], z: values[2] }
        })
        .collect::<Vec<Point>>()
}

fn part_one() {
    let file_path = "smallInput.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let points = parse(&rows);

    let mut pairs = BTreeSet::new();
    for i in 0..points.len() {
        for j in (i + 1)..points.len() {
            pairs.insert(PointPair::new(points[i], points[j]));
        }
    }

    let mut last_circuit_idx: usize = 0;
    let mut circuits: HashMap<Point, usize> = HashMap::new();
    for pair in pairs.iter().take(10) {
        if circuits.contains_key(&pair.p1) && circuits.contains_key(&pair.p2) {
            let new_idx = circuits[&pair.p1];
            let old_idx = circuits[&pair.p2];

            let old_keys_to_update = circuits
                .keys()
                .filter(|&p| circuits[p] == old_idx)
                .collect::<Vec<&Point>>();

            for point in old_keys_to_update {
                *circuits.get_mut(point).unwrap() = new_idx;
            }

        } else if circuits.contains_key(&pair.p1) {
            let circuit_idx = circuits[&pair.p1];
            circuits.insert(pair.p2, circuit_idx);

        } else if circuits.contains_key(&pair.p2) {
            let circuit_idx = circuits[&pair.p2];
            circuits.insert(pair.p1, circuit_idx);

        } else {
            circuits.insert(pair.p1, last_circuit_idx);
            circuits.insert(pair.p2, last_circuit_idx);
            last_circuit_idx += 1;
        }
    }

    for (point, idx) in circuits.keys().zip(circuits.values()) {
        println!("{:?}, {}", point, idx);
    }

    let mut circuit_sizes: Vec<usize> = vec![0; last_circuit_idx];
    for &circuit_idx in circuits.values() {
        println!("{}", circuit_idx);
        circuit_sizes[circuit_idx] += 1;
    }

    println!("{:?}", circuit_sizes);
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