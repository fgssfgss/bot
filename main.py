#!/usr/bin/python3
 
import sys
from logic.manager import TaskManager
from config.manager import ConfigManager

class Main():
  def __init__(self):
    if len(sys.argv) < 2:
      self.config_filename = 'config.json'
    else:
      self.config_filename = str(sys.argv[1])
  
  def run(self):
    self.config_manager = ConfigManager(self.config_filename)
    self.task_manager = TaskManager()
    self.task_manager.set_config(self.config_manager)
    self.task_manager.run()
  
if __name__ == "__main__":
  Main().run()
