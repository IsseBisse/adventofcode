use std::collections::HashSet;
use std::fs;
use std::io;
use std::cmp;

use std::cmp::Ordering;
use std::collections::BTreeSet;
use std::collections::HashMap;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

#[derive(Hash, Eq, PartialEq, Copy, Clone, Debug)]
struct Point {
    x: i64,
    y: i64,
}

impl Point {
    fn area(&self, other: &Self) -> i64 {
        let dx = (self.x - other.x).abs() + 1;
        let dy = (self.y - other.y).abs() + 1;
        dx * dy
    }

    fn line(&self, other: &Self) -> Vec<Point> {
        if self.x == other.x {
            let start = cmp::min(self.y, other.y);
            let end = cmp::max(self.y, other.y);
            (start..end+1)
                .map(|y| Point { x: self.x, y: y })
                .collect::<Vec<Point>>()
        } else {
            let start = cmp::min(self.x, other.x);
            let end = cmp::max(self.x, other.x);
            (start..end+1)
                .map(|x| Point { x: x, y: self.y })
                .collect::<Vec<Point>>()
        }
    }

    fn adjacent(&self) -> Vec<Point> {
        (-1..2)
            .flat_map(|y_offset| {
                (-1..2)
                    .map(move |x_offset| Point { x: self.x + x_offset, y: self.y + y_offset })
            })
            .filter(|p| p != self)
            .collect::<Vec<Point>>()
    }
}

#[derive(Debug)]
struct PointPair {
    p1: Point,
    p2: Point,
    area: i64,
}

impl PointPair {
    fn new(p1: Point, p2: Point) -> Self {
        let area = p1.area(&p2);
        PointPair { p1, p2, area }
    }
}

impl Eq for PointPair {}

impl PartialEq for PointPair {
    fn eq(&self, other: &Self) -> bool {
        self.area == other.area
    }
}

impl Ord for PointPair {
    fn cmp(&self, other: &Self) -> Ordering {
        self.area.cmp(&other.area)
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
                .map(|sub_s| sub_s.parse::<i64>().unwrap())
                .collect::<Vec<i64>>();
            Point { x: values[0], y: values[1] }
        })
        .collect::<Vec<Point>>()
}

fn part_one() {
    let file_path = "input.txt";

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

        for pair in pairs.iter().rev().take(1) {
            println!("{:?} {:?} {}", pair.p1, pair.p2, pair.area);
        }
}

fn print(allowed_points: &HashMap<i64, HashSet<i64>>) {
    for y in 0..15 {
        let line: String = (0..15)
            .map(|x| {
                if allowed_points.contains_key(&y) {
                    if allowed_points[&y].contains(&x) {
                        '#'
                    } else {
                        '.'
                    }
                } else {
                    '.'
                }

            })
            .collect();
        println!("{}", line);
    }
}

fn is_inside(pair: &PointPair, perimeter: &HashMap<i64, HashSet<i64>>) -> bool {
    let y_start = cmp::min(pair.p1.y, pair.p2.y) + 1;
    let y_end = cmp::max(pair.p1.y, pair.p2.y);
    let x_start = cmp::min(pair.p1.x, pair.p2.x) + 1;
    let x_end = cmp::max(pair.p1.x, pair.p2.x);

    for y in y_start..y_end {
        if !perimeter.contains_key(&y) {
            continue;
        }

        for &x in perimeter[&y].iter() {
            if x_start <= x && x_end >= x {
                println!("({}, {}) on perimeter", x, y);
                return false
            }
        }
    }
    
    true
}

fn part_two() {
    let file_path = "smallInput.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let points = parse(&rows);
    // TODO: Use HashMap<x, Vec<y>> for efficiency
    let mut perimeter: HashMap<i64, HashSet<i64>> = HashMap::new();
    for w in points.windows(2) {
        let first = w[0];
        let second = w[1];

        let line = first.line(&second);
        for p in line {
            perimeter.entry(p.y).or_default().insert(p.x);
        }
    }

    let last_line = points[0].line(&points[points.len()-1]);
    for p in last_line{
        perimeter.entry(p.y).or_default().insert(p.x);
    }

    print(&perimeter);

    let mut pairs = BTreeSet::new();
    for i in 0..points.len() {
        for j in (i + 1)..points.len() {
            pairs.insert(PointPair::new(points[i], points[j]));
        }
    }

    for pair in pairs.iter().rev() {
        println!("{:?} {:?} {}", pair.p1, pair.p2, pair.area);
       
        if is_inside(pair, &perimeter) {
            // println!("{:?} {:?} {}", pair.p1, pair.p2, pair.area);
            println!("Inside")        
        }
    }
    // let mut candidates = vec![Point { x: points[0].x + 1, y: points[0].y + 1}];
    // let mut laps = 0;
    // while candidates.len() > 0 {
    //     let current = candidates.pop().unwrap();
    //     allowed_points.insert(current);
    //     let adjacent = current.adjacent();

    //     for point in adjacent {
    //         if !allowed_points.contains(&point) {
    //             candidates.push(point);
    //         }
    //     }

    //     // print(&allowed_points);
    //     // laps += 1;

    //     // if laps > 3 {
    //     //     break;
    //     // }
    // }

    // print(&allowed_points);

    // println!("{:?}", allowed_points);



}

fn main() {
    // part_one();
    part_two();
}