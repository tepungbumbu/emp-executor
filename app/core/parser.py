import json

def parse_emp(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
