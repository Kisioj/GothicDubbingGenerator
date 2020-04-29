# Gothic Dubbing Generator
Automatically generating dubbing for Gothic I and Gothic II using Google Text-To-Speech


### Install

First you need to install Python3 [here](https://www.python.org/).

**Alert** When installing Python on Windows you need to check `ADD PYTHON TO PATH` checkbox. Also, in command line you run python using `python` command instead of `python3` (version for Linux & macOS).

```bash
$ python3 -m pip install -r requirements.txt
```


### Data extractor
This part analyzes scripts and generates following files in `output/metadata/` directory:

- `dialogues.json` - informations about characters and their dialog lines 
- `voices.json` - informations about characters and their voice settings (if this file exists, it's updated - new rows are added, but old ones aren't changed)

Usage:
```bash
$ python3 src/extractor.py PATH_TO_GOTHIC.SRC [--verbose]
```

Once data is generated. You can customize `voices.json` to your needs.

### Dubbing generator

First you need to generate Google [Text-to-Speech](https://cloud.google.com/text-to-speech) API Key and download it in `json` format.
Instruction to generate API Key can be found [here](https://www.miarec.com/doc/administration-guide/doc997).

Usage:
```bash
$ python3 src/generator.py PATH_TO_API_KEY.JSON [--verbose]
```

All dialogues are generated in `output` directory.