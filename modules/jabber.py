#!/usr/bin/python3 

import threading
import pprint
import time
import sleekxmpp

class JabberModule(threading.Thread, sleekxmpp.ClientXMPP):
  def __init__(self):
    threading.Thread.__init__(self, name='jabber_module')
    self.options = dict()
  
  def set_options(self, options):
    self.options = options
    
  def set_callback_function(self, func):
    self.callback = func
    
  def get_module_name(self):
    return "jabber"
    
  def init(self):
    print(self.options)
    sleekxmpp.ClientXMPP.__init__(self, self.options['jid'], self.options['password']) # deferred call of constructor, sorry 
    self.add_event_handler("session_start", self.start_session)
    #self.add_event_handler("groupchat_message", self.receive_message)
    self.add_event_handler("message", self.receive_message)
    self.register_plugin('xep_0030')
    self.register_plugin('xep_0045')
    self.register_plugin('xep_0199')
    return True
    
  def start_session(self, event):
    self.get_roster()
    self.send_presence()
    for i in range(len(self.options['conferences'])):
      self.plugin['xep_0045'].joinMUC(self.options['conferences'][i], self.options['nick'], wait=True)
    
  def send_message(self, to, text):
    if 'conference' in to:
      t = 'groupchat'
    else:
      t = 'chat'
    super(sleekxmpp.ClientXMPP, self).send_message(mto = to, mbody = text, mtype = t)
  
  def receive_message(self, msg):
    if msg['mucnick'] == self.options['nick']:
      return
    
    if msg['body'] == 'The nickname you are using is not registered': # dirty hack
      return
      
    context_message = dict()
    context_message['module'] = self
    context_message['from'] = msg['from'].bare
    context_message['text'] = msg['body']
    context_message['flags'] = 0 # not used
    
    self.callback(context_message)
    return
  
  def run(self):
    if self.connect():
      self.process(block = True)
