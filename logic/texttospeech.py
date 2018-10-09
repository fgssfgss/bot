#!/usr/bin/python3
from tempfile import NamedTemporaryFile
import requests


class TextToSpeech:
    ENDPOINT = 'http://api.voicerss.org/?key={0}&с=OGG&hl=ru-ru&f=48khz_16bit_stereo&src={1}'

    def __init__(self, key):
        self.key = key

    def get_voice_file(self, text):
        quoted_text = text
        url = TextToSpeech.ENDPOINT.format(self.key, quoted_text)
        data = requests.get(url, allow_redirects=True)
        with NamedTemporaryFile(delete=False) as f:
            for chunk in data.iter_content(chunk_size=128):
                f.write(chunk)
            print(f.name)
            return f.name