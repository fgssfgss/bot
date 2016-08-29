#!/usr/bin/python3 

import telebot
import threading
import pprint
import json
import time

class TeleModule(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self, name='telegram_module')
    self.options = dict()
    self.bot = dict()
  
  def set_options(self, options):
    self.options = options
    
  def set_callback_function(self, func):
    self.callback = func
    
  def get_module_name(self):
    return "telegram"
    
  def init(self):
    bot = telebot.TeleBot(self.options['token'])
    @bot.message_handler(content_types=["text"])
    def receive_message(message): 
      context_message = dict()
      context_message['module'] = self
      context_message['from'] = message.chat.id
      context_message['text'] = message.text
      context_message['flags'] = 0 
		
      self.callback(context_message)
      return
    self.bot = bot
    return True
    
  def send_message(self, to, text):
    self.bot.send_message(to, text)
    

  
  def run(self):
    self.bot.polling(none_stop=True)
  
