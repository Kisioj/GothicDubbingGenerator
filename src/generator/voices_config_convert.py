import json
import os
import random

from utils import save_to_file, is_valid_file

VOICES_PATH = "output/metadata/voices.json"
CONVERTED_VOICES_PATH = "output/metadata/converted_voices.json"
VOICE_MALE = "pl-PL-MarekNeural"
VOICE_FEMALE1 = "pl-PL-AgnieszkaNeural"
VOICE_FEMALE2 = "pl-PL-ZofiaNeural"
VOICES_FEMALE = [VOICE_FEMALE1, VOICE_FEMALE2]

def data_to_dict(data):
    data_dict = {}
    for row in data:
        key = f"{row['identifier']}|{row['name']}"
        assert key
        assert key not in data_dict
        data_dict[key] = row

    return data_dict



def fix_raw_data(data):
    for row in data:
        # identifier = row['identifier']
        name = row['name']
        gender = row['gender']
        assert name
        assert gender in ('M', 'F')
        # if not identifier:
        #     row['identifier'] = name.upper()

        if gender == 'M':
            row['voice'] = VOICE_MALE
            if name == 'Player':
                row['pitch'] = 1
                row['speed'] = 1
            elif name == 'Unknown':
                row['pitch'] = 0.8
                row['speed'] = 1.2
            else:
                if random.randint(0, 1) == 0:
                    row['pitch'] = random.randint(70, 80) / 100
                else:
                    row['pitch'] = random.randint(120, 140) / 100
                row['speed'] = random.randint(90, 120) / 100

        elif gender == 'F':
            row['voice'] = random.choice(VOICES_FEMALE)
            row['pitch'] = random.randint(80, 120) / 100
            row['speed'] = random.randint(90, 120) / 100


if os.path.exists(CONVERTED_VOICES_PATH):
    with open(CONVERTED_VOICES_PATH) as file:
        converted_data = json.loads(file.read())
else:
    converted_data = []

converted_data_dict = data_to_dict(converted_data)


with open(VOICES_PATH) as file:
    data = json.loads(file.read())
    fix_raw_data(data)

data_dict = data_to_dict(data)


for key in data_dict:
    if key not in converted_data_dict:
        converted_data_dict[key] = data_dict[key]

converted_data = [value for value in converted_data_dict.values()]

save_to_file(converted_data, CONVERTED_VOICES_PATH)
