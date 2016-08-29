#!/usr/bin/python3 

import sqlite3
import ctypes
from ctypes.util import find_library

class Database():
  def __init__(self, dbfile, sqlite_mode):
    if sqlite_mode != -1:
      sqlite_lib = ctypes.CDLL(find_library('sqlite3'))
      sqlite_lib.sqlite3_config(sqlite_mode)
    connection = sqlite3.connect(dbfile, check_same_thread=False)
    self.db = connection.cursor()
    
  def fetch_row_with_words(self, first = '', second = '', third = ''):
    if not first and not second and not third:
      return self.db.execute("SELECT * FROM lexems WHERE lexeme1 = '#beg#' ORDER BY RANDOM() LIMIT 0,1;")
      
    elif not first:
      return self.db.execute("SELECT * FROM lexems WHERE lexeme2 = ? AND lexeme3 = ? ORDER BY `count` DESC LIMIT 0,10;", (second, third))

    elif not third:
      return self.db.execute("SELECT * FROM lexems WHERE lexeme1 = ? AND lexeme2 = ? ORDER BY `count` DESC LIMIT 0,10;", (first, second))
    
    else:
      return self.db.execute("SELECT * FROM lexems WHERE lexeme1 = ? OR lexeme2 = ? OR lexeme3 = ? ORDER BY RANDOM() LIMIT 0,1;", (first, second, third))
    
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
      result = self.fetch_row_with_words(word, word, word)
      for row in result:
        answer = []
        answer.append(row[0])
        answer.append(row[1])
        answer.append(row[2])
        return answer
