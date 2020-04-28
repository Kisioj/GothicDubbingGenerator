from pprint import pprint
import random
import json


pitch_range = [-3, 3]
speed_range = [8, 12]  # 0.8, 1.2

female_voices = ['A', 'D', 'E']
male_voices = ['B'] * 9 + ['C']  # ,'C'

all = '''Player, Unknown, Gottlieb, Tiuran, Stary Liam, Sheridan, Filibert, Karsten, Doris, Adolphine, Germund, Grimur, Iago, Maxymilian, Zarządca, Goran, Santiago, Herold, Karter, Orel, Yves, Foster, Sorel, Odrin, Marco, Bogdan, Ludwig, Fernando, Gareth, Zarządca, Manderly, Patracjan, Dilbert, Fedner, Heiko, Alina, Staruszka, Jarod, Fynn, Torlof, Gerrit, Janus, Raza, Bohir, Kellan, Warin, Wynn, Nils, Herszlik, Odo, Carius, Ramsey, Ingrid, Berg, Herman, Strażnik bramy, Łuczarz, Kanut, Strażnik bramy, Lucas, Strażnik bramy, Caron, Gerstand, Mik, Serg, Lorenzo, Ingo, Strażnik bramy, Erik, Sedreil, Fabian, Carlos, Bernard, Sandalfon, Złotnik, Ramiro, Forneus, Ramon, Cortez, Malcolm, Trizzio, Adam, Samael, Azrael, Dan, Bardiel, Strażnik miejski, Varrok, Gwardzista, Winstan, Ostrin, Strażnik miejski, Benno, Oktav, Hestrian, Strażnik miejski, Strażnik miejski, Odon, Gwardzista, Teo, Simon, Ignacio, Raff, Beinard, Skryba Maciej, Strażnik miejski, Edra, Strażnik miejski, Ogrodnik, Zastępca Gubernatora, Strażnik miejski, Strażnik miejski, Tankred, Gwardzista, Torrez, Gwardzista, Calvin, Gerda, Allan, Ruslanda, Hengo, Albertine, Vittorio, Hargis, Fiona, Mathias, Karsh, Elbert, Helga, Will, Lana, Jorgon, Aldora, Eliza, Timo, Frida, Dervin, Mary, Gwen, Ranko, Katrina, Zyndram, Marlon, Malvina, Tavin, Behner, Nirko, Paul, Ralf, Rygus, Louise, Barend, Otto, Matt, Gunn, Thomson, Bolec, Rigg, Burton'''.split(', ')

females = set('''Gerda, Ruslanda, Mary, Fiona, Helga, Lana, Aldora, Eliza, Frida, Katrina, Malvina, Louise, Doris, Adolphine, Albertine, Edra, Ingrid, Caron, Alina, Staruszka, Yasmin'''.split(', '))

males = set(all) - set(females)


VOICE_TEMPLATE = "pl-PL-Wavenet-{voice}"
LANGUAGE = "pl-PL"

# database = {
#     'Player': {
#         "voice_name": 'C',
#         "pitch": -1.6,
#         "speed": 1.0
#     },
#     'Unknown': {
#         "voice_name": 'B',
#         "pitch": 0.0,
#         "speed": 1.0
#     },
#     'Alan': {
#         "voice_name": 'C',
#         "pitch": -4.4,
#         "speed": 1.15
#     },
#     'Will': {
#         "voice_name": 'C',
#         "pitch": 3.6,
#         "speed": 1.0
#     },
#     'Gwen': {
#         "voice_name": 'B',
#         "pitch": 0.0,
#         "speed": 1.0
#     },
#     'Bolec': {
#         "voice_name": 'B',
#         "pitch": -1.0,
#         "speed": 0.8
#     },

database = {
    'Adolphine': {'pitch': -3, 'speed': 0.9, 'voice_name': 'D'},
    'Albertine': {'pitch': -3, 'speed': 1.1, 'voice_name': 'D'},
    'Aldora': {'pitch': 1, 'speed': 1.1, 'voice_name': 'A'},
    'Allan': {'pitch': -2, 'speed': 1.2, 'voice_name': 'B'},
    'Barend': {'pitch': 1, 'speed': 0.9, 'voice_name': 'B'},
    'Behner': {'pitch': -2, 'speed': 1.1, 'voice_name': 'B'},
    'Bolec': {'pitch': -1.0, 'speed': 0.8, 'voice_name': 'B'},
    'Burton': {'pitch': 3, 'speed': 0.8, 'voice_name': 'B'},
    'Calvin': {'pitch': 2, 'speed': 0.8, 'voice_name': 'C'},
    'Dervin': {'pitch': -1, 'speed': 1.2, 'voice_name': 'C'},
    'Doris': {'pitch': 1, 'speed': 1.0, 'voice_name': 'A'},
    'Elbert': {'pitch': 1, 'speed': 1.0, 'voice_name': 'B'},
    'Eliza': {'pitch': -2, 'speed': 1.1, 'voice_name': 'D'},
    'Filibert': {'pitch': -2, 'speed': 1.2, 'voice_name': 'B'},
    'Fiona': {'pitch': 2, 'speed': 0.8, 'voice_name': 'E'},
    'Frida': {'pitch': 3, 'speed': 1.2, 'voice_name': 'D'},
    'Gerda': {'pitch': -2, 'speed': 1.0, 'voice_name': 'D'},
    'Germund': {'pitch': 3, 'speed': 1.0, 'voice_name': 'B'},
    'Gottlieb': {'pitch': -2, 'speed': 1.2, 'voice_name': 'B'},
    'Grimur': {'pitch': 1, 'speed': 1.0, 'voice_name': 'B'},
    'Gunn': {'pitch': 2, 'speed': 1.0, 'voice_name': 'B'},
    'Gwen': {'pitch': 0.0, 'speed': 1.0, 'voice_name': 'B'},
    'Hargis': {'pitch': 3, 'speed': 0.9, 'voice_name': 'C'},
    'Helga': {'pitch': 3, 'speed': 1.0, 'voice_name': 'A'},
    'Hengo': {'pitch': -2, 'speed': 1.1, 'voice_name': 'B'},
    'Iago': {'pitch': 3, 'speed': 1.1, 'voice_name': 'B'},
    'Jorgon': {'pitch': -1, 'speed': 1.1, 'voice_name': 'B'},
    'Karsh': {'pitch': -2, 'speed': 1.1, 'voice_name': 'B'},
    'Karsten': {'pitch': -3, 'speed': 1.2, 'voice_name': 'B'},
    'Katrina': {'pitch': 1, 'speed': 0.8, 'voice_name': 'D'},
    'Lana': {'pitch': -3, 'speed': 1.0, 'voice_name': 'D'},
    'Louise': {'pitch': 2, 'speed': 1.1, 'voice_name': 'D'},
    'Malvina': {'pitch': -3, 'speed': 1.2, 'voice_name': 'E'},
    'Marlon': {'pitch': 2, 'speed': 1.2, 'voice_name': 'B'},
    'Mary': {'pitch': 1, 'speed': 1.1, 'voice_name': 'D'},
    'Mathias': {'pitch': 0, 'speed': 1.0, 'voice_name': 'B'},
    'Matt': {'pitch': 1, 'speed': 1.1, 'voice_name': 'B'},
    'Nick': {'pitch': 2, 'speed': 1.0, 'voice_name': 'B'},
    'Nirko': {'pitch': -2, 'speed': 1.0, 'voice_name': 'B'},
    'Otto': {'pitch': -3, 'speed': 1.1, 'voice_name': 'B'},
    'Paul': {'pitch': -2, 'speed': 1.0, 'voice_name': 'B'},
    'Player': {'pitch': -1.6, 'speed': 1.0, 'voice_name': 'C'},
    'Ralf': {'pitch': 2, 'speed': 0.8, 'voice_name': 'B'},
    'Ranko': {'pitch': -2, 'speed': 0.8, 'voice_name': 'B'},
    'Rigg': {'pitch': 3, 'speed': 1.0, 'voice_name': 'B'},
    'Ruslanda': {'pitch': 2, 'speed': 0.9, 'voice_name': 'D'},
    'Rygus': {'pitch': -1, 'speed': 1.0, 'voice_name': 'B'},
    'Sheridan': {'pitch': 2, 'speed': 1.2, 'voice_name': 'B'},
    'Tavin': {'pitch': -3, 'speed': 0.8, 'voice_name': 'B'},
    'Thomson': {'pitch': 3, 'speed': 1.2, 'voice_name': 'B'},
    'Timo': {'pitch': 1, 'speed': 0.8, 'voice_name': 'B'},
    'Tiuran': {'pitch': 3, 'speed': 1.2, 'voice_name': 'B'},
    'Unknown': {'pitch': 0.0, 'speed': 1.0, 'voice_name': 'B'},
    'Vick': {'pitch': -1, 'speed': 0.9, 'voice_name': 'B'},
    'Vittorio': {'pitch': -1, 'speed': 1.2, 'voice_name': 'B'},
    'Will': {'pitch': 3.6, 'speed': 1.0, 'voice_name': 'C'},
    'Zyndram': {'pitch': 3, 'speed': 1.0, 'voice_name': 'B'},
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
