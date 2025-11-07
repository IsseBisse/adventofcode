use std::cmp::Ordering;
use std::collections::HashMap;
use std::fs;

fn read_input(file_path: &str) -> String {
    let contents = fs::read_to_string(file_path).unwrap();
    contents
}

fn parse(rows: String) -> (HashMap<i32, Vec<i32>> ,Vec<Vec<i32>>) {
    let (rule_rows, manual_rows) = rows.split_once("\r\n\r\n").unwrap();

    let mut rules: HashMap<i32, Vec<i32>> = HashMap::new();
    for row in rule_rows.lines() {
        let rule_parts = row.split_once("|").unwrap();
        let key = rule_parts.1.parse::<i32>().unwrap();
        let value = rule_parts.0.parse::<i32>().unwrap();

        // Push to vector if it exist, otherwise create new vector
        rules.entry(key).or_insert_with(Vec::new).push(value);
    }

    let manuals = manual_rows.lines()
        .map(|row| {
            return row.split(",").map(|s| s.parse::<i32>().unwrap()).collect::<Vec<i32>>();
        })
        .collect::<Vec<Vec<i32>>>();

    return (rules, manuals);
}

fn follows_rules(manual: &Vec<i32>, rules: &HashMap<i32, Vec<i32>>) -> bool {
    let mut not_allowed_after: Vec<i32> = Vec::new();
    for num in manual {
        if not_allowed_after.contains(&num) {
            return false
        }

        if let Some(source_vec) = rules.get(&num) {
            not_allowed_after.extend_from_slice(source_vec);
        }
    }

    true
}

fn part_one() {
    let file_path = "input.txt";
    let input = read_input(file_path);

    let (rules, manuals) = parse(input);

    let allowed_manuals = manuals.into_iter()
        .filter(|m| follows_rules(m, &rules))
        .collect::<Vec<Vec<i32>>>();

    let middle_numbers_sum: i32 = allowed_manuals.into_iter()
        .map(|m| m[m.len()/2])
        .sum();

    println!("{}", middle_numbers_sum)
}

fn rule_comparator(rules: &HashMap<i32, Vec<i32>>) -> impl Fn(&i32, &i32) -> Ordering + '_ {
    move |first: &i32, second: &i32| -> Ordering {
        if let Some(first_must_be_after) = rules.get(first) {
            if first_must_be_after.contains(second) {
                return Ordering::Greater            }
        }

        if let Some(second_must_be_after) = rules.get(second) {
            if second_must_be_after.contains(first) {
                return Ordering::Less
            }
        }

        Ordering::Equal
    }
}

fn part_two() {
    let file_path = "input.txt";
    let input = read_input(file_path);

    let (rules, manuals) = parse(input);

    let incorrect_manuals = manuals.into_iter()
        .filter(|m| !follows_rules(m, &rules))
        .collect::<Vec<Vec<i32>>>();

    let sorted_manuals = incorrect_manuals.into_iter()
        .map(|mut m| {
            m.sort_by(rule_comparator(&rules));
            return m;
        })
        .collect::<Vec<Vec<i32>>>();

    let middle_numbers_sum: i32 = sorted_manuals.into_iter()
        .map(|m| m[m.len()/2])
        .sum();

    println!("{}", middle_numbers_sum)
}

fn main() {
    part_one();
    part_two();
}