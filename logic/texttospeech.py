#!/usr/bin/python3
import os
from io import BytesIO
import festival
import soundfile as sf


class TextToSpeech:
    def __init__(self, key):
        self.key = key

    def get_voice_file(self, text):
        f = BytesIO(b'')
        tmp_file = festival.textToWavFile(text)
        with open(tmp_file, 'rb') as fd:
            data, samplerate = sf.read(fd)
            sf.write(f, data, samplerate, format='OGG')
        os.unlink(tmp_file)
        f.seek(0)
        return f