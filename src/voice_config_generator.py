import sys
import random
import json
from pprint import pprint

from utils import save_to_file

PITCH_RANGE = (-3, 3)
SPEED_RANGE = (8, 12)  # 0.8, 1.2

FEMALE_VOICES = ('A', 'D', 'E')
MALE_VOICES = ('B',) * 9 + ('C',)

VOICE_TEMPLATE = "pl-PL-Wavenet-{voice_name}"
LANGUAGE = "pl-PL"


class VoiceConfigGenerator:
    def __init__(self, verbose):
        self.errors_count = 0
        self.verbose = verbose

    def error(self, *args, **kwargs):
        print('error:', *args, **kwargs)
        self.errors_count += 1

    def generate(self, filepath, new_data):
        with open(filepath) as file:
            current_data = json.loads(file.read())

        for row in current_data:
            row['active'] = False

        name_and_id_2_current_row = {
            f"{row['name']}|{row['identifier']}": row
            for row in current_data
            if row['identifier'] is not None
        }

        name_2_current_row = {row['name']: row for row in current_data}
        identifier_2_current_row = {
            row['identifier']: row
            for row in current_data
            if row['identifier'] is not None
        }

        new_rows_to_add = []

        for new_row in new_data:
            new_name = new_row['name']
            new_identifier = new_row['identifier']
            new_gender = new_row['gender']

            new_name_and_id = f'{new_name}|{new_identifier}'
            current_row = name_and_id_2_current_row.get(new_name_and_id)
            if current_row:
                current_row['active'] = True
                if current_row['gender'] != new_gender:
                    self.error(
                        f'NPC named `{current_row["name"]}` with id `{current_row["identifier"]}` gender '
                        f'change detection (current: {current_row["gender"]}, new: {new_gender})'
                    )
                continue

            current_row = name_2_current_row.get(new_name)
            if current_row:
                current_row['active'] = True
                if current_row.get('future') is True:
                    self.error(
                        f'NPC named `{current_row["name"]}` does have '
                        f'`"future": true`, but he exists, so please remove it'
                    )

                if current_row['identifier'] != new_identifier:
                    self.error(
                        f'NPC named `{current_row["name"]}` identifier change detection '
                        f'(current: {current_row["identifier"]}, new: {new_identifier})'
                    )

                if current_row['gender'] != new_gender:
                    self.error(
                        f'NPC `{current_row["name"]}` gender change detection '
                        f'(current: {current_row["gender"]}, new: {new_gender})'
                    )
                continue

            current_row = identifier_2_current_row.get(new_identifier)
            if current_row:
                current_row['active'] = True

                if current_row.get('future') is True:
                    self.error(
                        f'NPC with id `{current_row["identifier"]}` does have '
                        f'"future": true, please remove it'
                    )

                if current_row['name'] != new_name:
                    self.error(
                        f'NPC with id `{current_row["identifier"]}` name change detection '
                        f'(current: {current_row["name"]}, new: {new_name})'
                    )

                if current_row['gender'] != new_gender:
                    self.error(
                        f'NPC with id `{current_row["identifier"]}` gender change detection '
                        f'(current: {current_row["gender"]}, new: {new_gender})'
                    )
                continue

            new_rows_to_add.append(new_row)

        for current_row in current_data:
            if current_row['active'] is False and current_row.get('future') is not True:
                self.error(
                    f'NPC named `{current_row["name"]}` with id `{current_row["identifier"]}` '
                    f"doesn't exist in code anymore, remove it from `voices.json` "
                    f"or add flag \"future\": true, to his data"
                )

        if self.errors_count:
            print(f'{self.errors_count} errors found. '
                  f'Please fix `voices.json` and run program again')

            sys.exit(1)

        for new_row in new_rows_to_add:
            if new_row['gender'] == 'F':
                voice_name = random.choice(FEMALE_VOICES)
            else:
                voice_name = random.choice(MALE_VOICES)

            new_row['voice'] = VOICE_TEMPLATE.format(voice_name=voice_name)
            new_row['language'] = LANGUAGE
            new_row['pitch'] = random.randint(*PITCH_RANGE)
            new_row['speed'] = random.randint(*SPEED_RANGE) / 10

            if self.verbose:
                pprint(new_row)

            current_data.append(new_row)

        if new_rows_to_add:
            print(f'Added {len(new_rows_to_add)} new rows to `voices.json`:')
            save_to_file(current_data, filepath)
