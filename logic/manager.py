#!/usr/bin/python3


from database.db import Database
from .generator import Generator
from .commands import CommandManager
from modules.vk import VKModule
from modules.jabber import JabberModule
from modules.skype import SkypeModule
from modules.telegram import TeleModule
import pprint
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
                print(context)
                self.command_manager.parse_message(context)
                self.task_manager.queue.task_done()

    def __init__(self, config):
        self.config = config
        self.database = Database(self.config.get_db_path(), self.config.get_sqlite_mode())
        self.generator = Generator(self.database)
        self.command_manager = CommandManager(self.generator, self.config)
        self.modules = []
        self.queue = queue.Queue()
        self.workers = []

    def callback_function(self, context):
        self.queue.put(context)

    def run(self):
        # Helpers init
        enabled_modules = self.config.get_enabled_modules()
        modules_count = 0

        # Modules init
        if "vk" in enabled_modules:
            self.modules.append(VKModule())
            modules_count += 1
        if "jabber" in enabled_modules:
            self.modules.append(JabberModule())
            modules_count += 1
        if "skype" in enabled_modules:
            self.modules.append(SkypeModule())
            modules_count += 1
        if "telegram" in enabled_modules:
            self.modules.append(TeleModule())
            modules_count += 1

        for i in range(self.config.get_worker_thread_num()):
            self.workers.append(self.WorkerThread(self, self.command_manager))
            self.workers[i].start()

        for i in range(self.config.get_modules_len()):
            for j in range(modules_count):
                if self.modules[j].get_module_name() == self.config.get_modules_elements(i)['network']:
                    self.modules[j].set_options(self.config.get_modules_elements(i))

        for i in range(modules_count):
            self.modules[i].set_callback_function(self.callback_function)
            self.modules[i].init()
            self.modules[i].start()
