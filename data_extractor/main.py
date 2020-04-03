import json
import sys

from data_extractor.data_sniffer import DataSniffer
from data_extractor.src_helper import SrcHelper


def main():
    _, src_path = sys.argv

    src_helper = SrcHelper(src_path)
    files_paths = src_helper.get_daedalus_files()

    data_sniffer = DataSniffer()
    # files_paths = [
    #     '/home/kisioj/Desktop/Gothic/Scripts/Content/Story/NPC/BAU_8002_Allan.d',
    #     '/home/kisioj/Desktop/Gothic/Scripts/Content/Story/Dialoge/DIA_BAU_8002_Allan.d',
    # ]
    for i, file_path in enumerate(files_paths):
        print(f'\r{i}/{len(files_paths)} {file_path}')
        data_sniffer.sniff(file_path)

    with open('output.json', 'w') as file:
        file.write(json.dumps(data_sniffer.get_data(), ensure_ascii=False, indent=4))


if __name__ == '__main__':
    main()
