use std::collections::HashSet;
use std::collections::HashMap;
use std::fs;

fn parse_input(file_path: &str) -> (Coord, Coord, HashMap<Coord, [Option<Coord>; 4]>) {
    let contents = fs::read_to_string(file_path).unwrap();
    
    let mut maze: HashMap<Coord, char> = HashMap::new();
    let mut start: Coord = Coord::new(0, 0);
    let mut end: Coord = Coord::new(0, 0);
    for (y, row) in contents.lines().enumerate() {
        for (x, char) in row.chars().enumerate() {
            maze.insert(Coord::new(x as i32, y as i32), char);
            
            if char == 'S' {
                start = Coord::new(x as i32, y as i32);
            } else if char == 'E' {
                end = Coord::new(x as i32, y as i32);
            }
        }
    }

    let graph = create_graph(maze);

    (start, end, graph)
}

fn find_next_node<'a>(maze: &HashMap<Coord, char>, nodes: &'a Vec<Coord>, prev_start: &Coord, current_start: Coord) -> Option<Coord> {
    if *maze.get(&current_start).unwrap() == '#' {
        return None
    }

    let mut current = current_start;
    let mut prev = prev_start;
    while !nodes.contains(current) {
        for adj in current.adjacent() {
            if *maze.get(&adj).unwrap() == '#' {
                continue
            }

            if adj == prev {
                continue;
            }

            prev = current;
            current = adj
        }
    }

    return Some(current)
}

fn create_graph(maze: &HashMap<Coord, char>) -> HashMap<Coord, [Option<Coord>; 4]>{
    let mut nodes: Vec<Coord> = Vec::new();

    for (pos, val) in maze {
        if *val == '#' {
            continue
        }

        let adj = pos.adjacent();
        let num_open_adj = adj.iter()
            .filter(|c| *maze.get(c).unwrap() != '#')
            .collect::<Vec<&Coord>>()
            .len();
        if num_open_adj > 2 {
            // Coord is an intersection
            nodes.push(*pos);
        }
    }

    let mut graph: HashMap<Coord, [Option<Coord>; 4]> = HashMap::new();
    for node in nodes {
        let adj = node.adjacent();
        
        let connected_nodes = adj
            .map(|coord| find_next_node(&maze, &nodes, &node, coord));

        graph.insert(node, connected_nodes);
    }

    graph
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

    fn adjacent(&self) -> [Coord; 4] {
        [
            Coord::new(self.x+1, self.y),
            Coord::new(self.x, self.y+1),
            Coord::new(self.x-1, self.y),
            Coord::new(self.x, self.y-1),
        ]
    }
}


fn part_one() {
    let file_path = "input.txt";

    let (start, end, wall_map) = parse_input(file_path);
    let nodes = create_graph(wall_map);
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