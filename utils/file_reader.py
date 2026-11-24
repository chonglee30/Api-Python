import json
from pathlib import Path
#BASE_DIR = Path.cwd().joinpath('..', 'tests', 'data')
BASE_DIR = Path.cwd() / 'tests' / 'data'

def read_file(fileName):
    path = get_file_with_json_extension(fileName)
    with path.open(mode='r') as file:
        return json.load(file)

def get_file_with_json_extension(fileName):
    if fileName.endswith('.json'):
        path = BASE_DIR.joinpath(fileName)
    else:
        path = BASE_DIR.joinpath(f'{fileName}.json')
    return path