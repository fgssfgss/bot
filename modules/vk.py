#!/usr/bin/python3 

import vk_api
import threading
import requests
import pprint
import json
import time

class VKModule(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self, name='vk_module')
    self.options = dict()
    self.ts = ''
    self.server = ''
    self.key = ''
  
  def set_options(self, options):
    self.options = options
    
  def set_callback_function(self, func):
    self.callback = func
    
  def get_module_name(self):
    return "vk"
    
  def init(self):
    try:
      print(self.options)
      #client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH
      if self.options['token'] == None:
        self.vk = vk_api.VkApi(login = self.options['login'], password = self.options['password'])
      else:
        self.vk = vk_api.VkApi(app_id = 5839853, client_secret = "NvPKHWzkXiFRjcyKkKV8", token = self.options['token'])
      self.vk.authorization()
    except vk_api.AuthorizationError as error_msg:
      print(error_msg) 
      return False
    
    pollserveropts = {
	'use_ssl': 0,
	'pts': 0
    }
    response = self.vk.method('messages.getLongPollServer', pollserveropts)
    print(response)
    self.ts = response['ts']
    self.server = response['server']
    self.key = response['key']
    
    return True
    
  def send_message(self, to, text):
    activityopts = {
      'user_id': to,
      'type': 'typing'
    }
    chat_id = 0
    
    if to >= 2000000000:
      chat_id = to - 2000000000
      
    self.vk.method('messages.setActivity', activityopts)
    time.sleep(5)
    
    self.vk.method('messages.setActivity', activityopts)
    time.sleep(5)
    
    if chat_id > 0:
      messageopts = {
	'chat_id': chat_id,
	'message': text
      }
    else:
      messageopts = {
	'user_id': to,
	'message': text
      }
    self.vk.method('messages.send', messageopts)
  
  def mark_as_read(self, message_id):
    markopts = {
      'message_ids': message_id
    }
    self.vk.method('messages.markAsRead', markopts)
  
  def receive_message(self):
    http = requests.Session()
    answer = http.get('http://{0}?act=a_check&key={1}&ts={2}&wait=25&mode=2'.format(self.server, self.key, self.ts)).content.decode("utf-8")
    
    if 'failed' in answer:
      return
    
    information = json.loads(answer)
    self.ts = information['ts']
    
    for i in range(0, len(information['updates'])):
      if information['updates'][i][0] == 4: # this is incoming/outcoming messages
        context_message = dict()
        context_message['module'] = self
        context_message['from'] = information['updates'][i][3]
        context_message['text'] = information['updates'][i][6]
        context_message['flags'] = information['updates'][i][2]
        message_id = information['updates'][i][1]
        
        if context_message['flags'] & 2: # outcoming messages
          continue
        if context_message['text'] is None:
          continue
        
        self.mark_as_read(message_id)
        self.callback(context_message) # call callback function in manager
    return
  
  def run(self):
    while True:
      self.receive_message()
  