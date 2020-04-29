import os
from glob import glob

import settings
import utils


def main():
    cache = {}
    if os.path.isfile(settings.CACHE_JSON_PATH):
        cache = utils.load_json_from_file(settings.CACHE_JSON_PATH)
    cache = set(cache)
    wavs = set(
        os.path.basename(path)[:-4]
        for path in glob(f"{settings.WAV_DIR_PATH}/*.WAV")
    )
    for filename in (wavs - cache):
        print(f'{settings.WAV_DIR_PATH}/{filename}.WAV')



if __name__ == '__main__':
    main()
