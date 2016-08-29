#!/usr/bin/python3 

from database.sqlite import Database
from .generator import Generator
from .commands import CommandManager
from modules.vk import VKModule
from modules.jabber import JabberModule
from modules.skype import SkypeModule
from modules.telegram import TeleModule
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
    self.database = Database(self.config.get_db_path(), self.config.get_sqlite_mode())
    self.generator = Generator(self.database)
    self.command_manager = CommandManager(self.generator, self.config)
    enabled_modules = self.config.get_enabled_modules()
    modules_count = 0
    
    # Modules init
    if "vk" in enabled_modules:
      self.modules.append(VKModule())
      modules_count = modules_count + 1
    if "jabber" in enabled_modules:
      self.modules.append(JabberModule())
      modules_count = modules_count + 1
    if "skype" in enabled_modules:
      self.modules.append(SkypeModule())
      modules_count = modules_count + 1
    if "telegram" in enabled_modules:
      self.modules.append(TeleModule())
      modules_count = modules_count + 1
    
    for i in range(self.config.get_modules_len()):
      for j in range(modules_count):
        if self.modules[j].get_module_name() == self.config.get_modules_elements(i)['network']:
          self.modules[j].set_options(self.config.get_modules_elements(i))

    for i in range(modules_count):
      self.modules[i].set_callback_function(self.callback_function)
      self.modules[i].init()
      self.modules[i].start()
      
    
    
  
