import argparse
import os

from data_sniffer import DataSniffer
from src_helper import SrcHelper
from voice_config_generator import VoiceConfigGenerator
from utils import save_to_file


DIALOGUES_JSON_PATH = 'output/metadata/dialogues.json'
VOICES_JSON_PATH = 'output/metadata/voices.json'


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist!")
    else:
        return arg


def main():
    parser = argparse.ArgumentParser(
        description='Extract data from Daedalus project',
    )

    parser.add_argument(
        'src_path',
        type=lambda src_path: is_valid_file(parser, src_path),
        help='path to .src file'
    )

    parser.add_argument(
        '--reset-voices',
        action='store_true',
        help='regenerate voices.json'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='display parsing progress'
    )

    args = parser.parse_args()

    src_helper = SrcHelper(args.src_path)
    # files_paths = [
    #     '/home/kisioj/Desktop/TheHistoryOfKhorinis/Scripts/Content/Story/NPC/Village/BAU_8220_Will.d',
    #     '/home/kisioj/Desktop/TheHistoryOfKhorinis/Scripts/Content/Story/NPC/Village/BAU_8002_Allan.d',
    #     '/home/kisioj/Desktop/TheHistoryOfKhorinis/Scripts/Content/Story/Dialoge/Village/DIA_BAU_8002_Allan.d',
    # ]
    files_paths = src_helper.get_daedalus_files()

    data_sniffer = DataSniffer()

    for i, file_path in enumerate(files_paths, start=1):
        if args.verbose:
            print(f'\r{i}/{len(files_paths)} {file_path}')
        data_sniffer.sniff(file_path)

    save_to_file(data_sniffer.get_dialogues_data(), DIALOGUES_JSON_PATH)

    generator = VoiceConfigGenerator(args.verbose)
    generator.generate(VOICES_JSON_PATH, data_sniffer.get_npc_data())


if __name__ == '__main__':
    main()
