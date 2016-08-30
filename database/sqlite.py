#!/usr/bin/python3 

import sqlite3
import ctypes
import threading
from ctypes.util import find_library

class Database():
  def __init__(self, dbfile, sqlite_mode):
    if sqlite_mode != -1:
      sqlite_lib = ctypes.CDLL(find_library('sqlite3'))
      sqlite_lib.sqlite3_config(sqlite_mode)
    connection = sqlite3.connect(dbfile, check_same_thread=False)
    self.db = connection.cursor()
    self.lock = threading.Lock()

  def check_word_existance(self, word):
    try:
      self.lock.acquire(True)
      self.db.execute("SELECT count(*) FROM lexems WHERE lexeme1 = ? OR lexeme2 = ? OR lexeme3 = ?;", (word, word, word))
      return int(self.db.fetchone()[0])
    finally:
      self.lock.release()
    
  def fetch_row_with_words(self, first = '', second = '', third = ''):
    if not first and not second and not third:
      try:
        self.lock.acquire(True)
        return self.db.execute("SELECT * FROM lexems WHERE lexeme1 = '#beg#' ORDER BY RANDOM() LIMIT 0,1;")
      finally:
        self.lock.release()
      
    elif not first:
      try:
        self.lock.acquire(True)
        return self.db.execute("SELECT * FROM lexems WHERE lexeme2 = ? AND lexeme3 = ? ORDER BY `count` DESC LIMIT 0,10;", (second, third))
      finally:
        self.lock.release()

    elif not third:
      try:
        self.lock.acquire(True)
        return self.db.execute("SELECT * FROM lexems WHERE lexeme1 = ? AND lexeme2 = ? ORDER BY `count` DESC LIMIT 0,10;", (first, second))
      finally:
        self.lock.release()
    
    else:
      try:
        self.lock.acquire(True)
        return self.db.execute("SELECT * FROM lexems WHERE lexeme1 = ? OR lexeme2 = ? OR lexeme3 = ? ORDER BY RANDOM() LIMIT 0,1;", (first, second, third))
      finally:
        self.lock.release()
    
  def fetch_three_words(self, first = '', second = '', third = '', word = ''):
    if not word:
      result = self.fetch_row_with_words(first, second, third)
      for row in result:
        answer = []
        answer.append(row[0])
        answer.append(row[1])
        answer.append(row[2])
        return answer
      
    else:
      if self.check_word_existance(word) == 0:
        raise LookupError
      result = self.fetch_row_with_words(word, word, word)
      for row in result:
        answer = []
        answer.append(row[0])
        answer.append(row[1])
        answer.append(row[2])
        return answer
