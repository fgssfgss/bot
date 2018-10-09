#!/usr/bin/python3
from io import BytesIO
import requests


class TextToSpeech:
    ENDPOINT = 'http://api.voicerss.org/?key={0}&с=OGG&hl=ru-ru&f=48khz_16bit_stereo&src={1}'

    def __init__(self, key):
        self.key = key

    def get_voice_file(self, text):
        quoted_text = text
        url = TextToSpeech.ENDPOINT.format(self.key, quoted_text)
        data = requests.get(url, allow_redirects=True)
        f = BytesIO(b'')
        if data.status_code == 200:
            for chunk in data.iter_content(chunk_size=1024):
                f.write(chunk)
            f.seek(0)
            return f
        else:
            return None