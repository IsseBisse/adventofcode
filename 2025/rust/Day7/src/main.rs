use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;
use std::hash::Hash;
use std::io;
use std::ops::Add;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

#[derive(Hash, Eq, PartialEq, Copy, Clone, Debug)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn split(self) -> Vec<Self> {
        let left = self + Point { x:-1, y: 0 };
        let right = self + Point { x:1, y: 0 };
        vec![left, right]
    }

    fn next(self, others: &HashSet<Self>, max_y: i32) -> Self {
        let mut beam = self;
        while !others.contains(&beam) {
            beam = beam + Point { x: 0, y: 1 };

            if beam.y > max_y {
                break
            }
        }

        beam
    }
}

impl Add for Point {
    type Output = Self;
    
    fn add(self, other: Self) -> Self {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

fn parse(rows: &Vec<String>) -> (HashSet<Point>, Point) {
    let start_x = rows[0]
        .chars()
        .enumerate()
        .filter(|(_, c)| *c == 'S')
        .map(|(idx, _)| idx)
        .next()
        .unwrap();
    let start = Point{ x: start_x as i32, y: 0 };

    let splitters_vec = rows
        .iter()
        .enumerate()
        .map(|(row, string)| {
            string
                .chars()
                .enumerate()
                .filter(|(_, c)| *c == '^')
                .map(|(col, _)| Point{ x: col as i32, y: row as i32})
                .collect::<Vec<Point>>()
        })
        .flatten()
        .collect::<Vec<Point>>();

    let splitters = HashSet::from_iter(splitters_vec.into_iter());

    (splitters, start)
}

fn one_step(beams: HashSet<Point>, splitters: &HashSet<Point>) -> (HashSet<Point>, usize) {
    let mut num_splits: usize = 0;
    let new_beams = HashSet::from_iter(
        beams
        .into_iter()
        .map(|beam| {
            let new_beam = beam + Point { x:0, y:1 };

            if splitters.contains(&new_beam) {
                num_splits += 1;
                Point::split(new_beam)
            } else {
                vec![new_beam]
            }
        })
        .flatten()
    );

    (new_beams, num_splits)
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let (splitters, start) = parse(&rows);
    let mut beams = HashSet::new();
    beams.insert(start);
    
    let mut num_splits: usize = 0;
    let mut new_splits: usize = 0;
    for _ in 0..rows.len() {
        (beams, new_splits) = one_step(beams, &splitters);
        num_splits += new_splits;
    }

    // println!("{:?}", splitters);
    // println!("{} {}", start.x, start.y);
    println!("{}", num_splits);
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
    
    let num_rows = rows.len();
    let num_cols = rows[0].len();

    let (splitters, start) = parse(&rows);
    let mut num_timelines: HashMap<Point, usize> = HashMap::new();
    for y in (0..num_rows).rev() {
        let splitters_on_this_row = (0..num_cols)
            .map(|x| {
                Point { x: x as i32, y: y as i32 }
            })
            .filter(|p| splitters.contains(p));
            
            for incoming in splitters_on_this_row {
                let num_timelines_from_incoming = incoming
                    .split()
                    .iter()
                    .map(|outgoing| {
                        let next_split = outgoing.next(&splitters, num_rows as i32);
                        if num_timelines.contains_key(&next_split) {
                            *num_timelines.get(&next_split).unwrap()
                        } else {
                            1
                        }
                    })
                    .sum::<usize>();

                num_timelines.insert(incoming, num_timelines_from_incoming);
            }
    }
    
    let first_splitter = start.next(&splitters, num_rows as i32);
    
    println!("{}", num_timelines.get(&first_splitter).unwrap())
}

fn main() {
    // part_one();
    part_two();
}