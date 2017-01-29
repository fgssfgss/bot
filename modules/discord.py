#!/usr/bin/python3

import asyncio
import discord
import threading
import pprint
import json
import time
import sys

# dirty hack for smile support
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


class DiscordModule(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name='discord_module')
        self.options = dict()
        self.bot = dict()

    def set_options(self, options):
        self.options = options

    def set_callback_function(self, func):
        self.callback = func

    def get_module_name(self):
        return "discord"

    def init(self):
        bot = discord.Client()

        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return

            context_message = dict()
            context_message['module'] = self
            context_message['from'] = message.channel
            context_message['text'] = message.content.translate(non_bmp_map)
            context_message['flags'] = 0
            self.callback(context_message)

        @bot.event
        async def on_ready():
            print('Logged in as')
            print(bot.user.name)
            print(bot.user.id)
            print('------')

        self.bot = bot
        return True

    def send_message(self, to, text):
        self.bot.send_message(to, text)

    def run(self):
        eventloop = asyncio.new_event_loop()
        asyncio.set_event_loop(eventloop)
        self.bot.run(self.options['token'])

