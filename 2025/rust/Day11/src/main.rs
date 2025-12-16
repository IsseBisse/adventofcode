use core::num;
use std::fs;
use std::io;

use std::collections::HashMap;

fn read_input(file_path: &str) -> io::Result<Vec<String>> {
    let contents = fs::read_to_string(file_path)?;
    Ok(contents.lines().map(String::from).collect())
}

fn parse(row: String) -> (String, Vec<String>) {
    let parts = row.split(" ").collect::<Vec<&str>>();
    
    let node = parts[0][..parts[0].len()-1].to_string();
    let conn = parts[1..]
        .iter()
        .map(|s| s.to_string())
        .collect::<Vec<String>>();

    (node, conn)
}

fn part_one() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });

    let mut connections = HashMap::new();
    for row in rows {
        let (node, conn) = parse(row);
        connections.insert(node, conn);
    }

    let mut paths_to_out = 0;
    let mut current_nodes = vec!["you".to_string()];
    while current_nodes.len() > 0 {
        let mut new_nodes = Vec::new();
        for node in current_nodes {
            if node == "out" {
                paths_to_out += 1;
                continue;
            }

            let mut conn = connections[&node].clone();
            new_nodes.append(&mut conn);
        }

        current_nodes = new_nodes;
    }

    // println!("{:?}", connections);
    println!("{}", paths_to_out)
}

#[derive(PartialEq, Eq, Hash)]
struct Node {
    key: String,
    passed_dac: bool,
    passed_fft: bool,
}

fn part_two() {
    let file_path = "input.txt";

    let rows = read_input(file_path).unwrap_or_else(|error| {
        println!("Error reading file: {}", error);
        std::process::exit(1)
    });
    
    let mut connections = HashMap::new();
    for row in rows {
        let (node, conn) = parse(row);
        connections.insert(node, conn);
    }

    // println!("{:?}", connections);

    let mut paths_to_out = 0;
    let start = Node { key: "svr".to_string(), passed_dac: false, passed_fft: false };
    let mut current_nodes = vec![(start, 1 as usize)];
    while current_nodes.len() > 0 {
        let mut new_nodes: HashMap<Node, usize> = HashMap::new();
        for (mut node, num_paths) in current_nodes {
            if node.key == "out" {
                if node.passed_dac && node.passed_fft {
                    paths_to_out += num_paths;
                }
                continue;
            }

            if node.key == "dac" {
                node.passed_dac = true;
            }
            if node.key == "fft" {
                node.passed_fft = true;
            }

            let conn = connections[&node.key]
                .iter()
                .map(|n| Node { 
                    key: n.clone(), 
                    passed_dac: node.passed_dac, 
                    passed_fft: node.passed_fft, 
                })
                .collect::<Vec<Node>>();
            
            for c in conn {
                new_nodes.entry(c).and_modify(|v| *v += num_paths).or_insert(num_paths);
            }
        }

        current_nodes = new_nodes
            .into_iter()
            .collect::<Vec<(Node, usize)>>();
        // println!("{}", current_nodes.len());
    }

    // println!("{:?}", connections);
    println!("{}", paths_to_out)
}

fn main() {
    // part_one();
    part_two();
}