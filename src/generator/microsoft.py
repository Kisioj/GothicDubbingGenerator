import re

from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import azure.cognitiveservices.speech as speechsdk
from time import perf_counter, sleep
import argparse
import os
from glob import glob


import utils
import settings
from generate_cache import generate_cache_json


LOCATION_REGION = "eastus"
LANGUAGE = "pl-PL"

repeat = True

def to_ssml(text, voice, speed, pitch):
    speed = int(speed*100-100)
    pitch = int(pitch*100-100)//2
    text = text.title().replace('<', '&lt;').replace('>', '&gt;')
    return f"""
<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
    <voice name="{voice}">
        <prosody rate="{speed}%" pitch="{pitch}%">{text}</prosody>
    </voice>
</speak>
"""


def is_cached(npc, ai_output, cache):
    wav_filename = ai_output['wav_filename']

    if wav_filename not in cache:
        return False

    row = [npc['speed'], npc['pitch'], npc['voice'], ai_output['text']]
    cached_row = cache[wav_filename]

    return row == cached_row


def main():
    os.system('ulimit -n 10000')

    parser = argparse.ArgumentParser(description='Gothic Dubbing Generator')
    parser.add_argument(
        '-k',
        '--key',
        help='azure text to speech service key',
        required=True,
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
    speech_config = SpeechConfig(subscription=args.key, region=LOCATION_REGION)
    speech_config.speech_synthesis_language = LANGUAGE
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    voices = utils.load_json_from_file(settings.CONVERTED_VOICES_JSON_PATH)
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

    start = perf_counter()

    i = 0
    # for i, ai_output in enumerate(ai_outputs, start=1):
    while i < len(ai_outputs):
        ai_output = ai_outputs[i]
        i += 1
        sound_filename, text, npc = ai_output
        sound_path = os.path.join(settings.WAV_DIR_PATH, sound_filename)

        if sound_filename not in wavs_to_generate:
            print(f'{i}/{ai_outputs_len} {sound_filename}.WAV - CACHED | {perf_counter()-start:.2f}')
            continue

        elif sound_filename in wavs and os.path.getsize(f'{sound_path}.WAV'):
            print(f'{i}/{ai_outputs_len} {sound_filename}.WAV - EXISTING | {perf_counter()-start:.2f}')
            continue

        else:
            # generate_advanced_voice(synthesizer, sound_path, text, npc)
            print(f'{i}/{ai_outputs_len} {sound_filename}.WAV | {perf_counter()-start:.2f}', end='')
            if sound_filename in wavs:
                print(' - OVERWRITING', end='')

        # if repeat:
        if not os.path.getsize(f'{sound_path}.WAV'):
            i -= 1
            print(' - ERROR...', end='')
            # sleep(30)

        print()

    generate_cache_json(data, wavs)


def generate_advanced_voice(synthesizer, sound_path, text, npc):
    def text_to_speech(text, voice, speed, pitch, filepath):
        if text == "...":
            text = "wielokropek"
        elif text == "?":
            text = "pytajnik"
        elif not re.search('[^\W_]', text):
            text = "cisza"

        global repeat
        ssml = to_ssml(text=text, voice=voice, speed=speed, pitch=pitch)

        # audio_config = speechsdk.audio.AudioOutputConfig(filename=filepath)
        # synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        # synthesizer.speak_ssml(ssml)


        # print(ssml)
        # audio_config = speechsdk.audio.AudioOutputConfig(filename=filepath)

        result = synthesizer.speak_ssml(ssml)#.get()
        # result = synthesizer.speak_ssml_async(ssml).get()
        # print(result, result.cancellation_details)
        if result.cancellation_details:
            repeat = True
            print(result.cancellation_details)
        else:
            repeat = False
        stream = speechsdk.AudioDataStream(result)
        stream.save_to_wav_file(filepath)
        # sleep(2.5)



    voice = npc['voice']
    pitch = npc['pitch']
    speed = npc['speed']

    wav_path = sound_path + '.WAV'
    text_to_speech(text=text, voice=voice, speed=speed, pitch=pitch, filepath=wav_path)


if __name__ == '__main__':
    main()
