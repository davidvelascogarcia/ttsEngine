[![ttsEngine Homepage](https://img.shields.io/badge/ttsEngine-develop-orange.svg)](https://github.com/davidvelascogarcia/ttsEngine/tree/develop/programs) [![Latest Release](https://img.shields.io/github/tag/davidvelascogarcia/ttsEngine.svg?label=Latest%20Release)](https://github.com/davidvelascogarcia/ttsEngine/tags) [![Build Status](https://travis-ci.org/davidvelascogarcia/ttsEngine.svg?branch=develop)](https://travis-ci.org/davidvelascogarcia/ttsEngine)

# TTS Engine: ttsEngine (Python API)

- [Introduction](#introduction)
- [Use](#use)
- [Requirements](#requirements)
- [Status](#status)
- [Related projects](#related-projects)


## Introduction

`ttsEngine` module use `pyttsx3` and `gTTS` in `python`. This module performs TTS and converts recieved text to voice. Also use `YARP` to receive text to synthesize by network. This module also publish TTS results in `YARP` port. If network connection is available uses `gTTS` system voice, if not, uses system default voice.


## Use

`ttsEngine` requires text like input to be synthesized.
The process to running the program:

1. Execute [programs/ttsEngine.py](./programs), to start de program.
```python
python ttsEngine.py
```
2. Connect text source.
```bash
yarp connect /yourport/data:o /ttsEngine/data:i
```

NOTE:

- Data results are published on `/ttsEngine/data:o`

## Requirements

`ttsEngine` requires:

* [Install YARP 2.3.XX+](https://github.com/roboticslab-uc3m/installation-guides/blob/master/install-yarp.md)
* [Install pip](https://github.com/roboticslab-uc3m/installation-guides/blob/master/install-pip.md)
* Install gTTS:
```bash
pip3 install gTTS
```
* Install pyttsx3:

(Using YARP with Python 2.7 bindings)
```bash
pip2 install pyttsx3
```

(Using YARP with Python 3 bindings)
```bash
pip3 install pyttsx3
```

Using `Microsoft Windows` also needs:
```bash
pip3 install pypiwin32
```

Tested on: `windows 10`, `ubuntu 14.04`, `ubuntu 16.04`, `ubuntu 18.04`, `lubuntu 18.04` and `raspbian`.


## Status

[![Build Status](https://travis-ci.org/davidvelascogarcia/ttsEngine.svg?branch=develop)](https://travis-ci.org/davidvelascogarcia/ttsEngine)

[![Issues](https://img.shields.io/github/issues/davidvelascogarcia/ttsEngine.svg?label=Issues)](https://github.com/davidvelascogarcia/ttsEngine/issues)

## Related projects

* [pyttsx3: python speech](https://pypi.org/project/pyttsx3/)

