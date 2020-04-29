import argparse

from data_sniffer import DataSniffer
from src_helper import SrcHelper
from voice_config_generator import VoiceConfigGenerator
from utils import save_to_file, is_valid_file
import settings


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
    files_paths = src_helper.get_daedalus_files()

    data_sniffer = DataSniffer()

    for i, file_path in enumerate(files_paths, start=1):
        if args.verbose:
            print(f'\r{i}/{len(files_paths)} {file_path}')
        data_sniffer.sniff(file_path)

    save_to_file(data_sniffer.get_dialogues_data(), settings.DIALOGUES_JSON_PATH)

    generator = VoiceConfigGenerator(args.verbose)
    generator.generate(settings.VOICES_JSON_PATH, data_sniffer.get_npc_data())


if __name__ == '__main__':
    main()
