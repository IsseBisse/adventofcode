use std::fs;

fn get_input(filename: &str) -> Vec<i32> {
    let contents = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");

    let numbers: Vec<i32> = contents
        .split_whitespace()
        .map(|s| s.parse().expect("parse error"))
        .collect();

    return numbers;
}

fn count_depth_increases(depths: Vec<i32>) -> i32 {
    let mut num_depth_increases = 0;
    let mut previous_depth = -1;
    for depth in depths {
        if previous_depth >= 0 && depth > previous_depth {
            num_depth_increases += 1;
        }

        previous_depth = depth;
    } 

    return num_depth_increases;
}

fn part_one() {
    let depths = get_input("input.txt");

    let num_depth_increases = count_depth_increases(depths);

    println!("Number of depth increases: {:?}", num_depth_increases);
}

fn part_two() {
    let depths = get_input("input.txt");
    let mut sum_depths: Vec<i32> = Vec::new();

    for i in 0..depths.len()-2 {
        sum_depths.push(depths[i..i+3].iter().sum());
    }

    let num_depth_increases = count_depth_increases(sum_depths);

    println!("Number of summed depth increases: {:?}", num_depth_increases);
}

fn main() {
    part_one();
    part_two();
}