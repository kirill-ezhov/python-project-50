#!/usr/bin/env python3
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', metavar='FORMAT', help='Set format of output')

    args = parser.parse_args()
    file_path1 = args.first_file
    file_path2 = args.second_file

    diff = generate_diff(file_path1, file_path2)

    if args.format == 'json':
        print(json.dumps(diff, indent=2))
    else:
        print("{")
        for key, value in diff.items():
            print(f"  {key}: {json.dumps(value, indent=2)[1:-1]}")
        print("}")


def generate_diff(file_path1, file_path2):
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

    with open(file_path1) as file1, open(file_path2) as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)

    diff = build_diff(data1, data2)
    return diff

if __name__ == "__main__":
    main()
