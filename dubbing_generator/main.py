import argparse
import json
import os

from google.cloud import texttospeech
from gtts import gTTS
from pydub import AudioSegment


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
        '--gender', '-g',
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

    args = parser.parse_args()
    gender = GENDERS[args.gender]

    with open(args.data_path) as file:
        data = json.loads(file.read())

    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    ai_outputs = []
    for npc in data:
        for ai_output in npc['ai_outputs']:
            ai_outputs.append((ai_output['wav_filename'], ai_output['text']))

    if args.service_key:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.service_key
        for i, ai_output in enumerate(ai_outputs):
            sound_filename, text = ai_output
            sound_path = os.path.join(OUTPUT_DIR, sound_filename)
            generate_advanced_voice(sound_path, text, args.lang, gender)
            print(f'\r{i}/{len(ai_outputs)} {sound_filename}.wav')
    else:
        for i, ai_output in enumerate(ai_outputs):
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


def generate_advanced_voice(sound_path, text, lang, gender):
    wav_path = sound_path + '.wav'

    client = texttospeech.TextToSpeechClient()

    voices = tuple(client.list_voices(lang).voices)
    for voice_params in voices:
        if voice_params.ssml_gender == gender:
            break

    voice = texttospeech.types.VoiceSelectionParams(
        language_code=voice_params.language_codes[0],
        name=voice_params.name,
    )

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16,
        pitch=0,
        speaking_rate=1,
    )

    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    with open(wav_path, 'wb') as out:
        out.write(response.audio_content)


if __name__ == '__main__':
    main()
