import json
import os


def save_to_file(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.isfile(filepath):
        os.rename(filepath, f'{filepath}.backup')
    with open(filepath, 'w', encoding='UTF-8') as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist!")
    else:
        return arg