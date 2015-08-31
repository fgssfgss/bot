#!/usr/bin/python3 

from database.sqlite import Database
from .generator import Generator
from .commands import CommandManager
from modules.vk import VKModule
from modules.jabber import JabberModule
from modules.skype import SkypeModule
import pprint

class TaskManager():
  def __init__(self):
    self.modules = []

  def set_config(self, config):
    self.config = config
    
  def callback_function(self, context):
    print(context)
    self.command_manager.parse_message(context)
    
  def run(self):
    # Helpers init
    self.database = Database(self.config.get_db_path())
    self.generator = Generator(self.database)
    self.command_manager = CommandManager(self.generator, self.config)
    
    # Modules init
    self.modules.append(VKModule())
    self.modules.append(JabberModule())
    self.modules.append(SkypeModule())
    
    for i in range(self.config.get_modules_len()):
      for j in range(3):
        if self.modules[j].get_module_name() == self.config.get_modules_elements(i)['network']:
          self.modules[j].set_options(self.config.get_modules_elements(i))

    for i in range(3):
      self.modules[i].set_callback_function(self.callback_function)
      self.modules[i].init()
      self.modules[i].start()
      
    
    
  