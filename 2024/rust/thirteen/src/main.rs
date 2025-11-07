use std::fs;
use std::cmp;
use regex::Regex;

fn read_input(file_path: &str) -> Vec<[[i32; 2]; 3]>{
    let contents = fs::read_to_string(file_path).unwrap();

    let re = Regex::new(r"Button A: X\+(\d+), Y\+(\d+)\r\nButton B: X\+(\d+), Y\+(\d+)\r\nPrize: X=(\d+), Y=(\d+)").unwrap();
    //let re = Regex::new(r"X\+(\d+), Y\+(\d+)").unwrap();
    let machines = re.captures_iter(contents.as_str())
        .map(|c| c.extract())
        .map(|(_, [ax, ay, bx, by, tx, ty])| {
            [[ax.parse::<i32>().unwrap(), 
            ay.parse::<i32>().unwrap()], 
            [bx.parse::<i32>().unwrap(), 
            by.parse::<i32>().unwrap()], 
            [tx.parse::<i32>().unwrap(), 
            ty.parse::<i32>().unwrap()]]
        })
        .collect::<Vec<[[i32; 2]; 3]>>();
    
    machines
}


const COST: [i32; 2] = [3, 1];
fn solve(machine: &[[i32; 2]; 3]) -> Option<i32> {
    let a = machine[0];
    let b = machine[1];
    let target = machine[2];

    
    let mut min_cost: i32 = 1000;
    for btn_a_press in 1..101 {
        let a_x = btn_a_press*a[0];
        if !((target[0] - a_x) % b[0] == 0){
            continue;
        } 
        
        let btn_b_press = (target[0] - a_x) / b[0];
        let res_y = btn_a_press*a[1] + btn_b_press*b[1];

        if res_y == target[1] {
            let cost = COST[0]*btn_a_press + COST[1]*btn_b_press;
            min_cost = cmp::min(cost, min_cost)
        }        
    }

    if min_cost < 1000 {
        return Some(min_cost)
    } else {
        return None
    }
}


fn part_one() {
    let file_path = "input.txt";

    let machines = read_input(file_path);
    let costs = machines.iter()
        .filter_map(|m| solve(m))
        .collect::<Vec<i32>>();
    println!("{}", costs.iter().sum::<i32>())
}


fn read_input_two(file_path: &str) -> Vec<[[i64; 2]; 3]>{
    let contents = fs::read_to_string(file_path).unwrap();

    let re = Regex::new(r"Button A: X\+(\d+), Y\+(\d+)\r\nButton B: X\+(\d+), Y\+(\d+)\r\nPrize: X=(\d+), Y=(\d+)").unwrap();
    //let re = Regex::new(r"X\+(\d+), Y\+(\d+)").unwrap();
    let machines = re.captures_iter(contents.as_str())
        .map(|c| c.extract())
        .map(|(_, [ax, ay, bx, by, tx, ty])| {
            [[ax.parse::<i64>().unwrap(), 
            ay.parse::<i64>().unwrap()], 
            [bx.parse::<i64>().unwrap(), 
            by.parse::<i64>().unwrap()], 
            [tx.parse::<i64>().unwrap() + 10000000000000, 
            ty.parse::<i64>().unwrap() + 10000000000000]]
        })
        .collect::<Vec<[[i64; 2]; 3]>>();
    
    machines
}


fn o1_solve(machine: &[[i64; 2]; 3]) -> Option<i64> {
    let a = machine[0];
    let b = machine[1];
    let t = machine[2];

    let num = a[1]*t[0] - a[0]*t[1];
    let div = a[1]*b[0] - a[0]*b[1];

    if num % div != 0 {
        return None
    }

    let btn_b_press = num / div;
    if ((t[0] - btn_b_press*b[0]) % a[0]) != 0 {
        return None
    }

    let btn_a_press = (t[0] - btn_b_press*b[0]) / a[0];

    return Some(COST[0] as i64*btn_a_press + COST[1] as i64*btn_b_press)
}


fn part_two() {
    let file_path = "input.txt";
    // let file_path = "input.txt";

    let machines = read_input_two(file_path);
    let costs = machines.iter()
        .filter_map(|m| o1_solve(m))
        .collect::<Vec<i64>>();
    println!("{}", costs.iter().sum::<i64>());
}

fn main() {
    // part_one();
    part_two();
}