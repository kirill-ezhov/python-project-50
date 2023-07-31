import json
import yaml
import os

def parse_file(filepath):
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath) as file:
        try:
            if ext == '.json':
                return json.load(file)
            elif ext in ('.yml', '.yaml'):
                return yaml.safe_load(file)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            raise ValueError(f"Error parsing file: {e}")