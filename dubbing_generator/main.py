import json
import os
import sys

from gtts import gTTS
from pydub import AudioSegment


def main():
    OUTPUT_DIR = 'output'
    _, json_path = sys.argv

    with open(json_path) as file:
        data = json.loads(file.read())

    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    ai_outputs = []
    for npc in data:
        for ai_output in npc['ai_outputs']:
            ai_outputs.append((ai_output['wav_filename'], ai_output['text']))

    for i, ai_output in enumerate(ai_outputs):
        sound_filename, text = ai_output

        sound_path = os.path.join(OUTPUT_DIR, sound_filename)
        mp3_path = sound_path + '.mp3'
        wav_path = sound_path + '.wav'

        tts = gTTS(text, lang='pl')
        tts.save(mp3_path)
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")
        os.remove(mp3_path)

        print(f'\r{i}/{len(ai_outputs)} {wav_path}')


if __name__ == '__main__':
    main()
