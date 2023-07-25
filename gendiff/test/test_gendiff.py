import json
from gendiff.scripts.gendiff import generate_diff


def test_generate_diff():
    file_path1 = "gendiff/tests/fixtures/file1.json"
    file_path2 = "gendiff/tests/fixtures/file2.json"
    with open("gendiff/tests/fixtures/expected_diff.json") as file:
        expected_diff = json.load(file)

    diff = generate_diff(file_path1, file_path2)
    assert diff == expected_diff
