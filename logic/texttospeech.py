#!/usr/bin/python3
import os
from io import BytesIO
import soundfile as sf
import threading
import time
import queue


class TextToSpeech:
    class FestivalThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.in_queue = queue.Queue()
            self.done = dict()

        def put_text(self, text):
            self.in_queue.put(text)

        def get_text(self, text):
            while True:
                if text in self.done.keys():
                    return self.done[text]
                else:
                    time.sleep(1)

        def run(self):
            import festival
            while True:
                if self.in_queue.qsize() < 1:
                    time.sleep(1)
                    continue
                else:
                    text = self.in_queue.get()
                    new_string = "".join(filter(lambda x: x.isalpha() or x.isspace(), text))
                    tmp_file = festival.textToWavFile(" ".join(new_string.split()))
                    self.done[text] = tmp_file

    def __init__(self):
        self.fest = self.FestivalThread()
        self.fest.start()

    def get_voice_file(self, text):
        f = BytesIO(b'')
        self.fest.put_text(text)
        tmp_file = self.fest.get_text(text)
        with open(tmp_file, 'rb') as fd:
            data, samplerate = sf.read(fd)
            sf.write(f, data, samplerate, format='OGG')
        os.unlink(tmp_file)
        f.seek(0)
        return f
