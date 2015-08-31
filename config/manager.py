#!/usr/bin/python3 

from .parser import Parser
import pprint

class ConfigManager():
  def __init__(self, filename):
    self.data = Parser().parse(filename)
    
  def get_db_path(self):
    return self.data['dbfile']
  
  def get_mode(self):
    return self.data['answer_mode']
  
  def set_mode(self, mode):
    self.data['answer_mode'] = mode
  
  def get_nick_list(self):
    return self.data['nicklist'].split(' ')
  
  def get_modules_len(self):
    return len(self.data['modules'])
  
  def get_modules_elements(self, idx):
    return self.data['modules'][idx]