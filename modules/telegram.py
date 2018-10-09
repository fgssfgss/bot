#!/usr/bin/python3

import sys
import os
import threading

import telebot
# dirty hack for smile support
from telebot.apihelper import ApiException

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


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
            context_message['text'] = message.text.translate(non_bmp_map)
            context_message['flags'] = 0

            self.callback(context_message)
            return

        self.bot = bot
        return True

    def send_message(self, to, text):
        try:
            self.bot.send_message(to, text)
        except ApiException as e:
            print("Cannot send message, maybe too long?")

    def send_voice(self, to, file):
        try:
            with open(file, 'rb') as fd:
                self.bot.send_voice(to, fd)
            os.remove(file)

        except ApiException as e:
            print("Cannot send message")
            raise e

    def run(self):
        while True:
            try:
                self.bot.polling(none_stop=True)
            except:
                print('Some connection problems with Telegram')
