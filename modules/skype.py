#!/usr/bin/python3 

# stub
import threading


class SkypeModule(threading.Thread):
    pass

# very broken, works on linux only with dbus
"""

import pprint
import time
import dbus.service
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gi.repository.GObject as gobject

class SkypeModule(threading.Thread, dbus.service.Object):
  def __init__(self):
    threading.Thread.__init__(self, name='skype_module')
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    dbus.service.Object.__init__(self, bus, "/com/Skype/Client")
    skypeObj = bus.get_object("com.Skype.API", "/com/Skype")
    self.skype = dbus.Interface(skypeObj, dbus_interface="com.Skype.API")
    self.send("NAME skype.py")
    self.send("PROTOCOL 7")
    self.options = dict()
  
  def set_options(self, options):
    self.options = options
    
  def set_callback_function(self, func):
    self.callback = func
    
  def get_module_name(self):
    return "skype"
    
  def init(self):
    print(self.options)
    return True
    
  @dbus.service.method(dbus_interface='com.Skype.API.Client')
  def Notify(self, message_text):
    print(message_text)
    command = message_text.split(' ')
    if command[0] == 'CHATMESSAGE':
      self.receive_message(command[1])
    
  def send(self, cmd):
    return self.skype.Invoke(cmd)
    
  def send_message(self, to, text):
    self.send("CHATMESSAGE %s %s"%(to, text))
  
  def receive_message(self, message_id):
    chatname = self.send("GET CHATMESSAGE %s CHATNAME"%(message_id)).split('CHATNAME ')[1]
    message = self.send("GET CHATMESSAGE %s BODY"%(message_id)).split('BODY ')[1]
    author = self.send("GET CHATMESSAGE %s FROM_DISPNAME"%(message_id)).split('FROM_DISPNAME ')[1]
    
    print(chatname)
    print(author)
    print(message)
    
    context_message = dict()
    context_message['module'] = self
    context_message['from'] = chatname
    context_message['text'] = message
    context_message['flags'] = 0
    
    self.prev_id = message_id
    
    self.callback(context_message)
    
    return
  
  def run(self):
    loop = gobject.MainLoop()
    loop.run()
 """
