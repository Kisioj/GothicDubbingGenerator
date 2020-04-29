import argparse
import json
import os
import sys
from glob import glob

from google.cloud import texttospeech

import utils
import settings


def is_cached(npc, ai_output, cache):
    wav_filename = ai_output['wav_filename']

    if wav_filename not in cache:
        return False

    row = [npc['speed'], npc['pitch'], npc['voice']]
    cached_row = cache[wav_filename]

    return row == cached_row


def generate_cache_json(data):
    cache = {}
    for row in data:
        value = (row['speed'], row['pitch'], row['voice'])
        for ai_output in row['ai_outputs']:
            key = ai_output['wav_filename']
            cache[key] = value

    utils.save_to_file(cache, settings.CACHE_JSON_PATH)


def main():
    parser = argparse.ArgumentParser(description='Gothic Dubbing Generator')
    parser.add_argument(
        'key_path',
        type=lambda src_path: utils.is_valid_file(parser, src_path),
        help='path to google service api key.json file'
    )

    parser.add_argument(
        '--reset-cache',
        action='store_true',
        help='remove cache.json before launching'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='display generation progress'
    )

    args = parser.parse_args()
    if args.key_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.key_path

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

    cache = {}
    if os.path.isfile(settings.CACHE_JSON_PATH):
        cache = utils.load_json_from_file(settings.CACHE_JSON_PATH)

    wavs = set(
        os.path.basename(path)[:-4]
        for path in glob(f"{settings.WAV_DIR_PATH}/*.WAV")
    )

    ai_outputs = []
    wavs_to_generate = set()
    for npc in data:
        for ai_output in npc['ai_outputs']:
            wav_filename = ai_output['wav_filename']
            text = ai_output['text']

            ai_outputs.append((wav_filename, text, npc))
            if not is_cached(npc, ai_output, cache):
                wavs_to_generate.add(wav_filename)

    ai_outputs_len = len(ai_outputs)

    for i, ai_output in enumerate(ai_outputs, start=1):
        sound_filename, text, npc = ai_output

        if sound_filename not in wavs_to_generate:
            print(f'{i}/{ai_outputs_len} {sound_filename}.WAV - CACHED')
            continue

        sound_path = os.path.join(settings.WAV_DIR_PATH, sound_filename)
        # generate_advanced_voice(sound_path, text, npc)
        print(f'{i}/{ai_outputs_len} {sound_filename}.WAV', end='')
        if sound_filename in wavs:
            print(' - OVERWRITING', end='')
        print()

    generate_cache_json(data)


def generate_advanced_voice(sound_path, text, npc):
    language = npc['language']
    voice_name = npc['voice']
    pitch = npc['pitch']
    speed = npc['speed']

    wav_path = sound_path + '.WAV'

    client = texttospeech.TextToSpeechClient()

    voice = texttospeech.types.VoiceSelectionParams(
        language_code=language,
        name=voice_name,
    )

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16,
        pitch=pitch,
        speaking_rate=speed,
    )

    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    with open(wav_path, 'wb') as out:
        out.write(response.audio_content)


if __name__ == '__main__':
    main()
