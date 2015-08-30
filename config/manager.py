#!/usr/bin/python3 

import parser

class ConfigManager():
  def __init__(self, filename):
    self.data = parser.parse(filename)
    
  def get_db_path(self):
    return self.data['dbfile']
  
  def get_modules_len(self):
    return len(self.data['modules'])
  
  def get_modules_elements(self, idx):
    return self.data['modules'][idx]