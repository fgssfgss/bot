#!/usr/bin/python3
import os
import sys
from io import BytesIO
import threading
import uuid
import subprocess


class TextToSpeech:
    FILE_NAME = '{}.ogg'

    def __init__(self, backend=None, tmp_dir=None):
        self.lock = threading.Lock()
        self.tool_path = backend if backend is not None else '/home/user/bot/voice_backend.py'
        self.tmp_dir = tmp_dir if tmp_dir is not None else '/tmp'

    def make_text_pretty(self, text):
        new_string = "".join(filter(lambda x: x.isalpha() or x.isspace(), text))
        return " ".join(new_string.split())

    def get_voice_file(self, text):
        f = None
        proper_text = self.make_text_pretty(text)
        self.lock.acquire()
        filename = self.FILE_NAME.format(str(uuid.uuid4()))
        location = os.path.join(self.tmp_dir, filename)
        cmd = [sys.executable, self.tool_path, location]
        with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stdin=subprocess.PIPE,  stderr=subprocess.STDOUT) as process:
            process.communicate(input=bytes(proper_text, 'UTF-8'))
        with open(location, 'rb') as file:
            f = BytesIO(file.read())
        os.unlink(location)
        self.lock.release()
        return f

