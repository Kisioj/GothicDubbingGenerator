from pprint import pprint
import random
import json


pitch_range = [-3, 3]
speed_range = [8, 12]  # 0.8, 1.2

female_voices = ['A', 'D', 'E']
male_voices = ['B'] * 9 + ['C']  # ,'C'

all = '''Calvin, Gerda, Allan, Ruslanda, Hengo, Albertine, Vittorio, Hargis, Fiona, Mathias, Karsh, Elbert, Helga, Will, Lana, Jorgon, Aldora, Eliza, Vick, Timo, Frida, Dervin, Mary, Gwen, Ranko, Katrina, Zyndram, Marlon, Malvina, Tavin, Behner, Nirko, Paul, Ralf, Nick, Rygus, Louise, Barend, Otto, Matt, Gunn, Thomson, Bolec, Rigg, Burton, Gottlieb, Tiuran, Sheridan, Filibert, Karsten, Doris, Adolphine, Germund, Grimur, Iago'''.split(', ')

females = set('''Ruslanda, Fiona, Helga, Lana, Aldora, Eliza, Frida, Katrina, Malvina, Louise, Doris, Adolphine, Albertine'''.split(', '))

males = set(all) - set(females)


VOICE_TEMPLATE = "pl-PL-Wavenet-{voice}"
LANGUAGE = "pl-PL"

database = {
    'Player': {
        "voice_name": 'C',
        "pitch": -1.6,
        "speed": 1.0
    },
    'Unknown': {
        "voice_name": 'B',
        "pitch": 0.0,
        "speed": 1.0
    },
    'Alan': {
        "voice_name": 'C',
        "pitch": -4.4,
        "speed": 1.15
    },
    'Will': {
        "voice_name": 'C',
        "pitch": 3.6,
        "speed": 1.0
    },
    'Gwen': {
        "voice_name": 'B',
        "pitch": 0.0,
        "speed": 1.0
    },
    'Bolec': {
        "voice_name": 'B',
        "pitch": -1.0,
        "speed": 0.8
    },
}

for name in all:
    if name in males:
        voice_name = random.choice(male_voices)
    else:
        voice_name = random.choice(female_voices)
    pitch = random.randint(*pitch_range)
    speed = random.randint(*speed_range) / 10

    if name not in database:
        database[name] = {
            "voice_name": voice_name,
            "pitch": pitch,
            "speed": speed
        }

for name, data in database.items():
    data['voice'] = VOICE_TEMPLATE.format(voice=data.pop('voice_name'))
    data['language'] = LANGUAGE

pprint(database)

with open('output.json') as f:
    content = json.loads(f.read())

for row in content:
    name = row['name']
    data = database[name]
    row.update(data)
    row['ai_outputs'] = row.pop('ai_outputs')


with open('save.json', 'w') as f:
    f.write(json.dumps(content, ensure_ascii=False, indent=2))
