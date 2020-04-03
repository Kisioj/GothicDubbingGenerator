# Gothic Dubbing Generator
Automatically generating dubbing for Gothic I and Gothic II using Google Text-To-Speech


### Install

First you need to install Python3 [here](https://www.python.org/).

**Alert** When installing Python on Windows you need to check `ADD PYTHON TO PATH` checkbox. Also, in command line you run python using `python` command instead of `python3` (version for Linux & macOS).

```bash
$ python3 -m pip install -r requirements.txt
```


### Data extractor
This part analyzes scripts and generates `output.json` which contains information about characters and their dialog lines.

Usage:
```bash
$ python3 data_extractor/main.py PATH_TO_GOTHIC.SRC
```
Example:
```bash
$ python3 data_extractor/main.py "/home/kisioj/Desktop/TheHistoryOfKhorinis/Scripts/Content/Gothic.src"
```


### Data updater
This part updates `output.json` and adds information about voice details of characters and saves it in `save.json`. For example, before updating, data could look like this:
```json
[
    {
        "name": "Player",
        "identifier": null,
        ...
```
and after updating it will look like this:
```json
[
  {
    "name": "Player",
    "identifier": null,
    "pitch": -1.6,
    "speed": 1.0,
    "voice": "pl-PL-Wavenet-C",
    "language": "pl-PL",
    ...
```

Usage:
```bash
$ python3 config_generator.py
```

### Dubbing generator

First you need to generate Google [Text-to-Speech](https://cloud.google.com/text-to-speech) API Key and download it in `json` format.
Instruction to generate API Key can be found [here](https://www.miarec.com/doc/administration-guide/doc997).




Usage:
```bash
$ python3 dubbing_generator/main.py PATH_TO_SAVE.JSON -k PATH_TO_API_KEY
```

Example:
```bash
$ python3 dubbing_generator/main.py save.json -k "/home/kisioj/Desktop/67308-83a2c6f03945.json"
```
