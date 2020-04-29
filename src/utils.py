import json
import os
import sys


def save_to_file(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.isfile(filepath):
        os.rename(filepath, f'{filepath}.backup')
    with open(filepath, 'w', encoding='UTF-8') as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))


def load_json_from_file(filepath):
    try:
        with open(filepath, encoding='UTF-8') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        print(f"File `{filepath}` does not exist.", file=sys.stderr)
        sys.exit(1)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist!")
    else:
        return arg