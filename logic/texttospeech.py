#!/usr/bin/python3
import os
import math
from io import BytesIO
import soundfile as sf
import threading
import time
import queue
import uuid
import subprocess


class TextToSpeech:
    FILE_LOCATION = '/tmp/{}.ogg'

    def __init__(self):
        self.lock = threading.Lock()
        self.tool_path = '/home/user/bot/voice_backend.py'

    def make_text_pretty(self, text):
        new_string = "".join(filter(lambda x: x.isalpha() or x.isspace(), text))
        return " ".join(new_string.split())

    def get_voice_file(self, text):
        f = None
        proper_text = self.make_text_pretty(text)
        self.lock.acquire()
        location = self.FILE_LOCATION.format(str(uuid.uuid4()))
        cmd = [self.tool_path, location]
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,  stderr=subprocess.STDOUT) as process:
            process.communicate(input=bytes(proper_text, 'UTF-8'))
        with open(location, 'rb') as file:
            f = BytesIO(file.read())
        os.unlink(location)
        self.lock.release()
        return f

