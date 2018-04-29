#!/usr/bin/python3

import json


class ConfigManager:
    def __init__(self, filename):
        self.data = self.parse(filename)

    @staticmethod
    def parse(filename):
        with open(filename) as file:
            data = json.load(file)
            return data

    def get_db_path(self):
        return self.data['dbfile']

    def get_mode(self):
        return self.data['answer_mode']

    def set_mode(self, mode):
        self.data['answer_mode'] = mode

    def get_modules_len(self):
        return len(self.data['modules'])

    def get_modules_elements(self, idx):
        return self.data['modules'][idx]

    def get_enabled_modules(self):
        return self.data['enabled_modules']

    def get_sqlite_mode(self):
        return int(self.data['sqlite_mode'])

    def get_worker_thread_num(self):
        return int(self.data['worker_threads'])
