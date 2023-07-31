import json
import os
import yaml

from gendiff.gendiff_cli import build_diff
from gendiff.parse_file import parse_file

def get_fixture_path(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'fixtures', filename)

def read_fixture(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def test_generate_diff_json():
    file1 = get_fixture_path('test_file1.json')
    file2 = get_fixture_path('test_file2.json')
    expected_diff_str = read_fixture(get_fixture_path('expected_diff_json.txt'))
    expected_diff = json.loads(expected_diff_str)
    diff = build_diff(parse_file(file1), parse_file(file2))
    assert diff == expected_diff

def test_generate_diff_yaml():
    file1 = get_fixture_path('test_file1.yml')
    file2 = get_fixture_path('test_file2.yml')
    expected_diff_str = read_fixture(get_fixture_path('expected_diff_json.txt'))
    diff = build_diff(parse_file(file1), parse_file(file2))
    diff_str = json.dumps(diff, indent=2, ensure_ascii=False, sort_keys=True)
    expected_diff_yaml = yaml.safe_load(expected_diff_str)
    expected_diff_yaml_str = json.dumps(expected_diff_yaml, indent=2, ensure_ascii=False, sort_keys=True)
    assert diff_str == expected_diff_yaml_str































