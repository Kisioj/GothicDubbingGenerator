import argparse
import json
import os
import sys

from google.cloud import texttospeech
from gtts import gTTS
from pydub import AudioSegment

from gui.gui import Gui


OUTPUT_DIR = 'output'


def does_file_exist(parser, arg):
    if not os.path.isfile(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


GENDERS = {
    'male': 1,
    'female': 2,
}


def main():
    parser = argparse.ArgumentParser(description='Gothic Dubbing Generator')
    parser.add_argument(
        'data_path',
        help='path to json file with data',
        type=lambda x: does_file_exist(parser, x),
        metavar="FILE"
    )
    parser.add_argument('--lang', '-l', default='pl', help='dubbing language (default=pl)')
    parser.add_argument(
        '--gender', '-s',
        default='male',
        type=str,
        choices=GENDERS,
        help='voice gender (default=male)'
    )
    parser.add_argument(
        '--service-key', '-k',
        help='path to google cloud service key (.json)',
        type=lambda x: does_file_exist(parser, x),
        metavar="KEY_FILE"
    )
    parser.add_argument('--gui', '-g', action='store_true', help='run gui mode')

    args = parser.parse_args()
    gender = GENDERS[args.gender]

    if args.service_key:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.service_key

    with open(args.data_path) as file:
        data = json.loads(file.read())

    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    if args.gui:
        if args.service_key:
            gui = Gui(data, args.lang.upper(), args.gender.upper())
            gui.run()
            return
        else:
            print("Google cloud service key is required to use GUI mode!", file=sys.stderr)

    ai_outputs = []
    for npc in data:
        for ai_output in npc['ai_outputs']:
            ai_outputs.append((ai_output['wav_filename'], ai_output['text'], npc))

    if args.service_key:
        for i, ai_output in enumerate(ai_outputs):
            sound_filename, text, npc = ai_output
            sound_path = os.path.join(OUTPUT_DIR, sound_filename)
            generate_advanced_voice(sound_path, text, npc, args.lang, gender)
            print(f'\r{i}/{len(ai_outputs)} {sound_filename}.wav')
    else:
        for i, ai_output, _ in enumerate(ai_outputs):
            sound_filename, text = ai_output
            sound_path = os.path.join(OUTPUT_DIR, sound_filename)
            generate_simple_voice(sound_path, text, args.lang, gender)
            print(f'\r{i}/{len(ai_outputs)} {sound_filename}.wav')


def generate_simple_voice(sound_path, text, lang, gender):
    mp3_path = sound_path + '.mp3'
    wav_path = sound_path + '.wav'

    tts = gTTS(text, lang=lang)
    tts.save(mp3_path)
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")
    os.remove(mp3_path)


'''
# from gui.gui import create_sound


def create_sound(client, wav_path, text, language, voice, pitch, speed):
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=language,
        name=voice,
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

'''


def generate_advanced_voice(sound_path, text, npc, lang, gender):
    language = npc.get('language', lang)
    voice_name = npc.get('voice')
    pitch = npc.get('pitch', 0.0)
    speed = npc.get('speed', 1.0)


    wav_path = sound_path + '.wav'

    client = texttospeech.TextToSpeechClient()

    if not voice_name:
        voices = tuple(client.list_voices(language).voices)
        for voice_params in voices:
            if voice_params.ssml_gender == gender:
                voice_name = voice_params.name
                language = voice_params.language_codes[0]
                break

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
