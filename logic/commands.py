#!/usr/bin/python3
import random


class CommandManager:
    def __init__(self, generator, config):
        self.generator = generator
        self.config = config
        self.enabled = {}

    @staticmethod
    def check_message_for_command(message):
        if message.lstrip()[0] == '!':
            return True  # This is command
        else:
            return False

    @staticmethod
    def send_answer(context, text):
        module = context['module']
        to = context['from']
        module.send_message(to, text)

    def parse_command(self, command, sender):
        args = command.rstrip().split(' ')
        command_name = args[0]

        if command_name == '!q':
            return self.task_gen_by_word(args[1])
        elif command_name == '!ql':
            return self.task_gen_by_word_like(args[1])
        elif command_name == '!roll':
            return self.task_roll()
        elif command_name == '!about':
            return self.task_about()
        elif command_name == '!off':
            return self.task_disable_bot(sender)
        elif command_name == '!on':
            return self.task_enable_bot(sender)
        elif command_name == '!answer_mode':
            return self.task_set_answer_mode(args[1])
        elif command_name == '!help':
            return self.task_print_help()
        else:
            return self.task_unknown_command()

    def parse_message(self, context):
        message = context['text']
        sender = context['from']

        if not self.check_message_for_command(message):
            self.generator.insert_to_db(message)
            if context['module'].get_module_name() == "jabber" and not message.startwith(
                    context['module'].options['nick']):  # only for jabber and maybe telegram, but not tested
                return
            if sender in self.enabled.keys() and not self.enabled[sender]:
                return
            text = self.generator.gen_full_rand()
            self.send_answer(context, text)
        else:
            value = self.parse_command(message.lstrip(), sender)
            if value is None:  # if command does not return anything
                return
            self.send_answer(context, value)

    def task_gen_by_word(self, word):
        text = self.generator.gen_by_word(word)
        return text

    def task_gen_by_word_like(self, word):
        text = self.generator.gen_by_word(word, True)
        return text

    def task_about(self):
        text = 'Zhelezyaka v0.0.2, written by fgssfgss'
        return text

    def task_roll(self):
        num = random.randint(0, 36)
        text = "Your roll is: " + str(num)
        return text

    def task_enable_bot(self, sender):
        self.enabled[sender] = True
        return 'Bot enabled for this chat or conference'

    def task_disable_bot(self, sender):
        self.enabled[sender] = False
        return 'Bot disabled for this chat or conference'

    def task_set_answer_mode(self, mode):
        text = 'Current mode: ' + self.config.get_mode() + ', default - bynick, other - for all'
        self.config.set_mode(mode)
        return text

    def task_print_help(self):
        text = 'Available commands: [!help] [!about] [!q] [!ql] [!roll] [!on] [!off]' \
               '\n!help - View this help' \
               '\n!about - View about message' \
               '\n!q - Generate message with some word inside' \
               '\n!ql - Generate message with some substring in random word' \
               '\n!roll - Roll a dice' \
               '\n!on - Enable bot for this conference or chat' \
               '\n!off - Disable bot for this conference or chat'
        return text

    def task_unknown_command(self):
        text = 'Unknown command'
        return text + '\n\n' + self.task_print_help()
