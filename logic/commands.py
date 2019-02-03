#!/usr/bin/python3
import os
import random
from .texttospeech import TextToSpeech


class CommandManager:
    commands = {
                '!qvoice': ('voice', lambda this, arg, sender: this.task_gen_by_word_with_voice(arg[1])),
                '!q': ('text', lambda this, arg, sender: this.task_gen_by_word(arg[1])),
                '!ql': ('text', lambda this, arg, sender: this.task_gen_by_word_like(arg[1])),
                '!roll': ('text', lambda this, arg, sender: this.task_roll()),
                '!about': ('text', lambda this, arg, sender: this.task_about()),
                '!off': ('text', lambda this, arg, sender: this.task_disable_bot(sender)),
                '!on': ('text', lambda this, arg, sender: this.task_enable_bot(sender)),
                '!answer_mode': ('text', lambda this, arg, sender: this.task_set_answer_mode(arg[1])),
                '!help': ('text', lambda this, arg, sender: this.task_print_help())
    }

    def __init__(self, generator, config):
        self.generator = generator
        self.config = config
        self.enabled = {}
        self.tts = TextToSpeech(self.config.get_voice_backend(), self.config.get_voice_tmpdir())

    @staticmethod
    def check_message_for_command(message):
        command_symbol = message.lstrip()[0]
        if command_symbol == '!' or command_symbol == '/':
            return True  # This is command
        else:
            return False

    @staticmethod
    def send_answer(context, **kwargs):
        module = context['module']
        to = context['from']
        command_type = kwargs.get('type', 'text')
        arg = kwargs.get('arg')

        if command_type == 'text':
            module.send_message(to, arg)
        elif command_type == 'voice' and module.get_module_name() == 'telegram'\
                and arg is not None:
            module.send_voice(to, arg)

    def parse_command(self, command, sender):
        args = command.rstrip().split(' ')
        command_name = list(args[0])
        command_name[0] = '!'
        command_name = ''.join(command_name)
        if len(args) <= 1:
            args.append(None)

        if command_name in self.commands.keys():
            return self.commands[command_name][1](self, args, sender), self.commands[command_name][0]
        else:
            return self.task_unknown_command(), 'text'

    def parse_message(self, context):
        message = context['text']
        sender = context['from']

        print("[{}] {}".format(sender, message))

        if not self.check_message_for_command(message):
            self.generator.insert_to_db(message)
            if context['module'].get_module_name() == "jabber" and not message.startwith(
                    context['module'].options['nick']):  # only for jabber and maybe telegram, but not tested
                return
            if sender not in self.enabled.keys() or not self.enabled[sender]:
                return
            text = self.generator.gen_full_rand()
            self.send_answer(context, type='text', arg=text)
        else:
            value, command_type = self.parse_command(message.lstrip(), sender)
            if value is None:  # if command does not return anything
                return
            self.send_answer(context, type=command_type, arg=value)

    def task_gen_by_word(self, word):
        text = self.generator.gen_by_word(word) if word is not None else self.generator.gen_full_rand()
        return text

    def task_gen_by_word_like(self, word):
        text = self.generator.gen_by_word(word, True) if word is not None else self.generator.gen_full_rand()
        return text

    def task_gen_by_word_with_voice(self, word):
        text = self.generator.gen_by_word(word) if word is not None else self.generator.gen_full_rand()
        return self.tts.get_voice_file(text)

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
               '\n!qvoice - Generate voice message with some word inside' \
               '\n!roll - Roll a dice' \
               '\n!on - Enable bot for this conference or chat(by default disabled)' \
               '\n!off - Disable bot for this conference or chat'
        return text

    def task_unknown_command(self):
        text = 'Unknown command'
        return text + '\n\n' + self.task_print_help()
