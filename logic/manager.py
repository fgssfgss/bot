#!/usr/bin/python3
import logging

from database.db import Database
from .generator import Generator
from .commands import CommandManager
from modules.vk import VKModule
from modules.jabber import JabberModule
from modules.telegram import TeleModule
from modules.discord import DiscordModule
import threading
import queue


class TaskManager:
    class WorkerThread(threading.Thread):
        def __init__(self, task_manager, command_manager):
            threading.Thread.__init__(self, name='worker thread')
            self.command_manager = command_manager
            self.task_manager = task_manager

        def run(self):
            while True:
                context = self.task_manager.queue.get()
                self.command_manager.parse_message(context)
                self.task_manager.queue.task_done()

    def __init__(self, config):
        self.config = config
        self.generator = Generator(self.config)
        self.command_manager = CommandManager(self.generator, self.config)
        self.modules = []
        self.queue = queue.Queue()
        self.workers = []

    def callback_function(self, context):
        self.queue.put(context)

    def run(self):
        logging.info('Starting bot')

        # Helpers init
        enabled_modules = self.config.get_enabled_modules()

        # Modules init
        if "vk" in enabled_modules:
            self.modules.append(VKModule())
        if "jabber" in enabled_modules:
            self.modules.append(JabberModule())
        if "telegram" in enabled_modules:
            self.modules.append(TeleModule())
        if "discord" in enabled_modules:
            self.modules.append(DiscordModule())

        for i in range(self.config.get_worker_thread_num()):
            self.workers.append(self.WorkerThread(self, self.command_manager))
            self.workers[i].start()

        for i in range(self.config.get_modules_len()):
            for j in range(len(self.modules)):
                if self.modules[j].get_module_name() == self.config.get_modules_elements(i)['network']:
                    self.modules[j].set_options(self.config.get_modules_elements(i))

        for i in range(len(self.modules)):
            self.modules[i].set_callback_function(self.callback_function)
            self.modules[i].init()
            self.modules[i].start()
