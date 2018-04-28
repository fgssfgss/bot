#!/usr/bin/python3
import os
import sqlite3
import ctypes
import threading
import queue
import uuid
from ctypes.util import find_library


class SqliteMTProxy(threading.Thread):
    def __init__(self, dbfile, sqlite_mode):
        threading.Thread.__init__(self, name="sqlite mt proxy")
        if sqlite_mode != -1:
            sqlite_lib = ctypes.CDLL(find_library('sqlite3'))
            sqlite_lib.sqlite3_config(sqlite_mode)
        init = not os.path.isfile(dbfile)
        connection = sqlite3.connect(dbfile, check_same_thread=False)
        self.cursor = connection.cursor()
        if init:
            print("no db, init new one")
            self.cursor.execute(
                "CREATE TABLE lexems (`lexeme1` TEXT, `lexeme2` TEXT, `lexeme3` TEXT, `count` INT NOT NULL DEFAULT '0', UNIQUE (`lexeme1`, `lexeme2`, `lexeme3`));")

        self.cursor.execute("PRAGMA synchronous = OFF")
        self.cursor.execute("PRAGMA journal_mode = MEMORY")
        self.cond = threading.Condition()
        self.task_queue = queue.Queue()
        self.results = dict()

    def execute(self, script, args=None):
        token = str(uuid.uuid4())
        self.task_queue.put(item={'type': 'exec', 'script': script, 'args': args, 'token': token})
        return token

    def insert(self, script):
        self.task_queue.put(item={'type': 'insert', 'script': script})
        return

    def get_result(self, token):
        self.cond.acquire()
        while token not in self.results:
            self.cond.wait()
        self.cond.release()
        return self.results[token]

    def run(self):
        while True:
            task = self.task_queue.get()
            if task['type'] == 'insert':
                self.cursor.executescript(task['script'])
            else:
                if task['args'] is None:
                    result = self.cursor.execute(task['script'])
                else:
                    result = self.cursor.execute(task['script'], task['args'])
                self.cond.acquire()
                self.results[task['token']] = result.fetchone()
                self.cond.notify()
                self.cond.release()
            self.task_queue.task_done()
