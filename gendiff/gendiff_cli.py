import argparse
import json
import yaml
from pathlib import Path
from gendiff.format_stylish import format_diff


def main():
    description = 'Compares two configuration files and shows a difference.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', choices=['json', 'yaml', 'stylish'], default='stylish',
                        metavar='FORMAT', help='Set format of output')

    args = parser.parse_args()
    file_path1 = Path('test', 'fixtures', args.first_file)
    file_path2 = Path('test', 'fixtures', args.second_file)

    data1 = load_data(file_path1)
    data2 = load_data(file_path2)

    diff = generate_diff(data1, data2)

    if args.format == 'json':
        print(json.dumps(diff, indent=2))
    elif args.format == 'yaml':
        print(yaml.dump(diff, sort_keys=False))
    else:
        print(format_diff(diff))


def load_data(file_path):
    with open(file_path, 'r') as file:
        if file_path.suffix == '.json':
            return json.load(file)
        elif file_path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(file)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")


def generate_diff(obj1, obj2, path=""):
    diff = []

    for key in sorted(set(obj1.keys()) | set(obj2.keys())):
        new_path = f"{path}.{key}" if path else key

        if key in obj1 and key in obj2:
            if isinstance(obj1[key], dict) and isinstance(obj2[key], dict):
                nested_diff = generate_diff(obj1[key], obj2[key], new_path)
                if nested_diff:
                    diff.append({"key": key, "status": "nested", "children": nested_diff})
            elif obj1[key] == obj2[key]:
                value = obj1[key]
                if isinstance(value, str):
                    value = f'"{value}"'
                diff.append({"key": key, "status": "unchanged", "value": value})
            else:
                old_value = obj1[key]
                new_value = obj2[key]
                if isinstance(old_value, str):
                    old_value = f'"{old_value}"'
                if isinstance(new_value, str):
                    new_value = f'"{new_value}"'
                diff.append({"key": key, "status": "changed", "old_value": old_value, "new_value": new_value})
        elif key in obj1:
            value = obj1[key]
            if isinstance(value, str):
                value = f'"{value}"'
            if isinstance(obj1[key], dict):
                nested_diff = generate_diff(obj1[key], {}, new_path)
                if nested_diff:
                    diff.append({"key": key, "status": "nested", "children": nested_diff})
            else:
                diff.append({"key": key, "status": "removed", "value": value})
        else:
            value = obj2[key]
            if isinstance(value, str):
                value = f'"{value}"'
            if isinstance(obj2[key], dict):
                nested_diff = generate_diff({}, obj2[key], new_path)
                if nested_diff:
                    diff.append({"key": key, "status": "nested", "children": nested_diff})
            else:
                diff.append({"key": key, "status": "added", "value": value})

    return diff


if __name__ == '__main__':
    main()


















