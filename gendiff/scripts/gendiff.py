#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    description = 'Compares two configuration files and shows a difference.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format',
                        metavar='FORMAT', help='Set format of output')

    args = parser.parse_args()
    file_path1 = Path(args.first_file)
    file_path2 = Path(args.second_file)

    diff = generate_diff(file_path1, file_path2)

    if args.format == 'json':
        print(json.dumps(diff, indent=2))
    else:
        for key, value in diff.items():
            print(key, json.dumps(value, indent=2))


def generate_diff(file_path1, file_path2):
    data1 = load_json_data(file_path1)
    data2 = load_json_data(file_path2)

    return build_diff(data1, data2)


def load_json_data(file_path):
    with open(file_path) as file:
        return json.load(file)


def build_diff(obj1, obj2, path=""):
    diff = {}
    keys1 = set(obj1.keys())
    keys2 = set(obj2.keys())
    all_keys = sorted(keys1.union(keys2))

    for key in all_keys:
        new_path = f"{path}.{key}" if path else key

        if key in keys1 and key not in keys2:
            diff['- ' + new_path] = obj1[key]
        elif key in keys2 and key not in keys1:
            diff['+ ' + new_path] = obj2[key]
        elif obj1[key] != obj2[key]:
            if isinstance(obj1[key], dict) and isinstance(obj2[key], dict):
                nested_diff = build_diff(obj1[key], obj2[key], new_path)
                diff.update(nested_diff)
            else:
                diff['- ' + new_path] = obj1[key]
                diff['+ ' + new_path] = obj2[key]
        else:
            diff[new_path] = obj1[key]
    return diff


if __name__ == "__main__":
    main()
