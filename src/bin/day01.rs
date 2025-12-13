use glob::glob;
use std::collections::HashMap;
use std::ffi::OsString;
use std::fs;

fn read_inputs(day_path: &str) -> HashMap<String, String> {
    let mut glob_string: String = String::from(day_path);
    glob_string.push_str("/*.txt");

    let inputs = glob(&glob_string);

    let mut result: HashMap<String, String> = HashMap::new();
    for entry in inputs.unwrap() {
        match entry {
            Ok(path) => {
                let content = fs::read_to_string(&path).expect("we just found the path on fs");
                result.insert(
                    OsString::from(path.file_name().unwrap())
                        .into_string()
                        .unwrap(),
                    content,
                );
            }
            Err(e) => eprintln!("{:?}", e),
        }
    }

    result
}

const START: i64 = 50;

fn part1() {
    let inputs = read_inputs("./src/day01");
    let my_input: &String = inputs.get("puzzle.txt").unwrap();

    let swapped_string: String = my_input.replace("L", "-").replace("R", "");
    let sample_input_list: Vec<i64> = swapped_string
        .split("\n")
        .map(|str_val| str_val.parse::<i64>().unwrap())
        .collect();

    let mut tracker = START;
    let mut zero_counter: i64 = 0;
    for i in sample_input_list {
        tracker += i;
        if tracker % 100 == 0 {
            zero_counter += 1;
        }
    }
    println!("{}", zero_counter)
}

fn part2() {
    let inputs = read_inputs("./src/day01");
    let my_input: &String = inputs.get("puzzle.txt").unwrap();

    let swapped_string: String = my_input.replace("L", "-").replace("R", "");
    let sample_input_list: Vec<i64> = swapped_string
        .split("\n")
        .map(|str_val| str_val.parse::<i64>().unwrap())
        .collect();

    let mut tracker = START;
    let mut zero_counter: i64 = 0;
    for i in sample_input_list {
        let mut next_tracker = tracker + i;

        zero_counter += ((tracker / 100) - (next_tracker / 100)).abs();

        // RUST: no floored division, so we need to add 1 to compensate if next_tracker is negative and division will be subject to rounding
        if next_tracker < 0 && (next_tracker % 100 != 0) {
            zero_counter += 1;
        }

        next_tracker = next_tracker.rem_euclid(100);

        if i < 0 {
            if tracker == 0 {
                zero_counter -= 1;
            }
            if next_tracker == 0 {
                zero_counter += 1;
            }
        }
        tracker = next_tracker;
    }
    println!("{}", zero_counter)
}

fn main() {
    part1();
    part2();
}
