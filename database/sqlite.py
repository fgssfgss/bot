#!/usr/bin/python3

import sqlite3
import ctypes
import threading
import queue
import uuid
from ctypes.util import find_library

class SqliteMTProxy(threading.Thread):
  def __init__(self, dbfile, sqlite_mode):
    threading.Thread.__init__(self, name = "sqlite mt proxy")
    if sqlite_mode != -1:
      sqlite_lib = ctypes.CDLL(find_library('sqlite3'))
      sqlite_lib.sqlite3_config(sqlite_mode)
    connection = sqlite3.connect(dbfile, check_same_thread=False)
    self.cursor = connection.cursor()
    self.lock = threading.Lock()
    self.task_queue = queue.Queue()
    self.results = dict()

  def execute(self, script, args = None):
    token = str(uuid.uuid4())
    self.task_queue.put(item={'script': script, 'args': args, 'token' : token})
    return token

  def get_result(self, token):
    while not token in self.results:
      pass
    return self.results[token]

  def run(self):
    while True:
      task = self.task_queue.get()
      #print(task['script'])
      #print(task['args'])
      if task['args'] == None:
        result = self.cursor.execute(task['script'])
      else:
        result = self.cursor.execute(task['script'], task['args'])
      self.results[task['token']] = result.fetchone()
      self.task_queue.task_done()