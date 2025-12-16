use std::fs;
use std::io;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

#[derive(Debug)]
struct Shape {
    dots: [bool; 9],
    area: usize
}

impl Shape {
    fn new(dots_str: &String) -> Self {
        let mut dots = [false; 9];
        
        for (i, ch) in dots_str.chars().enumerate() {
            if i >= 9 {
                break;
            }
            dots[i] = ch == '#';
        }
        
        let area = dots
            .iter()
            .map(|&d| d as usize)
            .sum::<usize>();

        Shape { dots: dots, area: area }
    }
}

#[derive(Debug)]
struct Grid {
    dim: (usize, usize),
    shapes: [usize; 6]
}

impl Grid {
    fn new(grid_str: &String) -> Self {
        let parts = grid_str
            .split(" ")
            .collect::<Vec<&str>>();
        
        let dim_parts = parts[0][..parts[0].len()-1]
            .split("x")
            .collect::<Vec<&str>>();
        let dim = (
            dim_parts[0].parse::<usize>().unwrap(),
            dim_parts[1].parse::<usize>().unwrap()
        );


        let mut shapes: [usize; 6] = [0; 6];
        
        for (i, str) in parts[1..].iter().enumerate() {
            if i >= 9 {
                break;
            }
            shapes[i] = str.parse::<usize>().unwrap();
        }

        Grid { dim, shapes } 
    }
}

fn parse(rows: Vec<String>) -> (Vec<Shape>, Vec<Grid>) {
    let shapes = rows[..30]
        .chunks(5)
        .map(|s| {
            Shape::new(&s[1..4].join(""))
        })
        .collect::<Vec<Shape>>();

    let grids = rows[30..]
        .iter()
        .map(|r| Grid::new(r))
        .collect::<Vec<Grid>>();

    (shapes, grids)
}

fn check(shapes: &Vec<Shape>, grid: &Grid) -> Option<bool> {
    let num_shapes = grid.shapes.iter().sum::<usize>();
    
    let (x_dim, y_dim) = grid.dim;
    let num_grids = (x_dim / 3) * (y_dim / 3);

    if num_grids >= num_shapes {
        return Some(true)
    }

    let num_occupied_squared = grid.shapes
        .iter()
        .enumerate()
        .map(|(idx, num_shapes)| num_shapes * shapes[idx].area)
        .sum::<usize>();

    let area = x_dim * y_dim;
    if num_occupied_squared >= area {
        return Some(false)
    }

    None
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let (shapes, grids) = parse(rows);
    let mut num_fittable_grids: usize = 0;
    let mut num_unknown_grids: usize = 0;
    for grid in grids {
        match check(&shapes, &grid) {
            Some(res) => num_fittable_grids += res as usize,
            None => num_unknown_grids += 1
        }
    }

    println!("Number of fittable grids {}", num_fittable_grids);
    println!("Number of unknown grids {}", num_unknown_grids);
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