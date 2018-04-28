#!/usr/bin/python3
import random


class CommandManager:
    def __init__(self, generator, config):
        self.generator = generator
        self.config = config
        self.enabled = True

    def check_message_for_command(self, message):
        if message.lstrip()[0] == '!':
            return True  # This is command
        else:
            return False

    def send_answer(self, context, text):
        module = context['module']
        to = context['from']
        module.send_message(to, text)

    def parse_command(self, command):
        args = command.split(' ')
        command_name = args[0]

        if command_name == '!q':
            return self.task_gen_by_word(args[1])
        elif command_name == '!roll':
            return self.task_roll()
        elif command_name == '!about':
            return self.task_about()
        elif command_name == '!off':
            return self.task_disable_bot()
        elif command_name == '!on':
            return self.task_enable_bot()
        elif command_name == '!answer_mode':
            return self.task_set_answer_mode(args[1])
        elif command_name == '!help':
            return self.task_print_help()
        else:
            return self.task_unknown_command()

    def parse_message(self, context):
        message = context['text']

        if not self.check_message_for_command(message):
            self.generator.insert_to_db(message)
            if context['module'].get_module_name() == "jabber" and not message.startwith(
                    context['module'].options['nick']):  # only for jabber and maybe telegram, but not tested
                return
            if not self.enabled:
                return
            text = self.generator.gen_full_rand()
            self.send_answer(context, text)
        else:
            value = self.parse_command(message)
            if value is None:  # if command does not return anything
                return
            if not self.enabled:
                return
            self.send_answer(context, value)

    def task_gen_by_word(self, word):
        text = self.generator.gen_by_word(word)
        return text

    def task_about(self):
        text = 'Zhelezyaka v0.0.2, written by fgssfgss'
        return text

    def task_roll(self):
        num = random.randint(0, 36)
        text = "Your roll is: " + str(num)
        return text

    def task_enable_bot(self):
        self.enabled = True
        return

    def task_disable_bot(self):
        self.enabled = False
        return

    def task_set_answer_mode(self, mode):
        text = 'Current mode: ' + self.config.get_mode() + ', default - bynick, other - for all'
        self.config.set_mode(mode)
        return text

    def task_print_help(self):
        text = 'Available commands: [!help] [!about] [!q] [!roll] [!on] [!off]'
        return text

    def task_unknown_command(self):
        text = 'Unknown command'
        return text
