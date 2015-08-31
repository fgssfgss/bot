#!/usr/bin/python3 

from database.sqlite import Database
from .generator import Generator
from modules.vk import VKModule
import pprint

class TaskManager():
  def __init__(self):
    self.modules = []

  def set_config(self, config):
    self.config = config
    
  def callback_function(self, context):
    print(context)
    
  def run(self):
    # Helpers init
    self.database = Database(self.config.get_db_path())
    self.generator = Generator(self.database)
    
    # Modules init
    for i in range(1):
      self.modules.append(VKModule())
    
    for i in range(self.config.get_modules_len()):
      for j in range(1):
        if self.modules[j].get_module_name() == self.config.get_modules_elements(i)['network']:
          self.modules[j].set_options(self.config.get_modules_elements(i))

    for i in range(1):
      self.modules[i].set_callback_function(self.callback_function)
      self.modules[i].init()
      self.modules[i].start()
      
    
    
  