import os
from glob import glob

import settings
import utils


def generate_cache_json(data, wavs):
    cache = {}
    for row in data:
        value = (row['speed'], row['pitch'], row['voice'])
        for ai_output in row['ai_outputs']:
            key = ai_output['wav_filename']
            if key not in wavs:
                continue
            cache[key] = (*value, ai_output['text'])

    utils.save_to_file(cache, settings.CACHE_JSON_PATH)


def main():
    voices = utils.load_json_from_file(settings.VOICES_JSON_PATH)
    name_and_id_2_voice = {
        f"{voice['name']}|{voice['identifier']}": voice
        for voice in voices
    }

    data = utils.load_json_from_file(settings.DIALOGUES_JSON_PATH)
    for row in data:
        name_and_id = f"{row['name']}|{row['identifier']}"
        voice = name_and_id_2_voice[name_and_id]
        row.update(voice)

    wavs = set(
        os.path.basename(path)[:-4]
        for path in glob(f"{settings.WAV_DIR_PATH}/*.WAV")
    )

    generate_cache_json(data, wavs)


if __name__ == '__main__':
    main()
