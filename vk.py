# -*- coding: utf-8 -*-

# shitcode, but works :D

import vk_api
import requests
import json
import time
import threading as thread
import sqlite3 as db
import re
import string
import time
from queue import Queue

q = Queue()
excluded_users = '' # id or link to page 

class Gen:
	def __init__(self):
		self.connection = db.connect("database.db", check_same_thread=False)
		self.c = self.connection.cursor()

	def parse_text(self, text):
		start_time = time.time()
		query = ''
		words = text.split(' ')
		words.insert(0, '#beg#')
		words.append('#end#')
		for x in range(0, len(words)-2, 1):
			if time.time() - start_time > 10:
				print("Parse_Text | Too long...")
				break
			query += "INSERT OR IGNORE INTO lexems (`lexeme1`,`lexeme2`,`lexeme3`) VALUES(\'{0}\', \'{1}\', \'{2}\');\n".format(words[x], words[x+1], words[x+2])
			query += "UPDATE lexems SET count = count+1 WHERE lexeme1 = \'{0}\' AND lexeme2 = \'{1}\' AND lexeme3 = \'{2}\';\n".format(words[x], words[x+1], words[x+2])
		if len(query) != 0:
			self.c.executescript(query)

	def gen_full_rand(self):
		start_time = time.time()
		st = ''
		lexeme_a = ''
		lexeme_b = ''
		last = False
		result = self.c.execute("SELECT * FROM lexems WHERE lexeme1 = '#beg#' ORDER BY RANDOM() LIMIT 0,1;")
		while last != True:
			if time.time() - start_time > 5:
				print("Gen_full_rand | Too long...")
				break
			for row in result:
				lexeme_a, lexeme_b = row[1], row[2]
				st = st + row[1] + ' '
				for s in row[1:3]:
					if s == '#end#':
						last = True
						break
			result = self.c.execute("SELECT * FROM lexems WHERE lexeme1 = ? AND lexeme2 = ? ORDER BY RANDOM() LIMIT 0,1;", (lexeme_a, lexeme_b))
			
		if st == '' or len(st) > 4050:
			return "YA PIDORAS COMPUTERNIY"
		
		return st

	def gen_by_word(self, word):
		start_time = time.time()
		st = ''
		st1 = ''
		lexeme_a = ''
		lexeme_b = ''
		first = False
		last = False
		cp = False
		r_save = []

		result = self.c.execute("SELECT * FROM lexems WHERE lexeme1 = ? OR lexeme2 = ? OR lexeme3 = ? ORDER BY RANDOM() LIMIT 0,1;", (word, word, word))
		while first != True:
			if time.time() - start_time > 5:
				print("Gen_by_word | First Part  | Too long...")
				break
			
			for row in result:
				if cp == False:
					r_save = row
					cp = True
				lexeme_a, lexeme_b = row[0], row[1]
				if lexeme_a == '#beg#' or lexeme_a == '':
					first = True
					break
				st1 = lexeme_a + ' ' + st1
				break

			result = self.c.execute("SELECT * FROM lexems WHERE lexeme2 = ? AND lexeme3 = ? ORDER BY `count` DESC LIMIT 0,10;", (lexeme_a, lexeme_b))

		start_time = time.time()

		while last != True:
			if time.time() - start_time > 5:
				print("Gen_by_word | Second Part | Too long...")
				break
			
			for row in result:
				if cp == True:
					row = r_save
					cp = False
				lexeme_a, lexeme_b = row[1], row[2]
				if lexeme_b == '#end#' or lexeme_b == '':
					last = True
				st = st + lexeme_a + ' '
				break

			result = self.c.execute("SELECT * FROM lexems WHERE lexeme1 = ? AND lexeme2 = ? ORDER BY `count` DESC LIMIT 0,10;", (row[1], row[2]))

			if st1 + st == '' or len(st1 + st) > 4050:
				return "YA POEHAL KRISHEY, NIHUYA NE RABOTAET VO MNE"
			
		return st1 + st

class Answerer(thread.Thread):
	def __init__(self, vk):
		self.lol = ''
		self.vk = vk
		self.gen = Gen()
		thread.Thread.__init__(self)

	def run(self):
		global q
		while True:
			args = q.get()
			self.message_text = args[6]
			self.message_id = args[1]
			self.message_from = args[3]
			self.message_flags = args[2]
			global excluded_users
			if self.message_flags & 2:
				q.task_done()
				continue
			v = {
				'message_ids': self.message_id
			}
			resp = self.vk.method('messages.markAsRead', v)
			if re.findall(str(self.message_from), excluded_users):
				print("Excluded user, sorry...")
				q.task_done()
				continue
			command = self.message_text.split(' ')
			if command[0] == '!q':
				self.lol = self.gen.gen_by_word(command[1])
			elif command[0] == '!msg':
				self.message_from = int(re.search('[0-9]+', command[1]).group(0))
				self.lol = " ".join(command[2:])
				print(self.message_from)
				print(self.lol)
			else:
				self.gen.parse_text(self.message_text)
				self.lol = self.gen.gen_full_rand()
			if self.message_flags & 512:
				self.lol += "\n\r\n\rИ вообще я нихуя не вижу/не слышу, пидорас, зря шлешь, зря стараешься!"
			vw = {
				'user_id': self.message_from,
				'type': 'typing'
			}
			chat_from = 0
			if self.message_from >= 2000000000:
				chat_from = self.message_from - 2000000000
			resp = self.vk.method('messages.setActivity', vw)
			time.sleep(5)
			resp = self.vk.method('messages.setActivity', vw)
			time.sleep(5)
			if chat_from > 0:
				va = {
					'chat_id': chat_from,
					'message': self.lol
				}
			else:
				va = {
					'user_id': self.message_from,
					'message': self.lol
				}
			resp = self.vk.method('messages.send', va)
			self.lol = ''
			q.task_done()
			time.sleep(0.05)

class Bot:
	def __init__(self):
		self.login, self.password = 'login', 'password'

	def main(self):
		try:
			vk = vk_api.VkApi(self.login, self.password) # Auth
		except vk_api.AuthorizationError as error_msg:
			print(error_msg) # in case of error print message
			return 
		values = {
			'use_ssl': 0,
			'pts': 0
		}
		response = vk.method('messages.getLongPollServer', values)
		http = requests.Session()
		ts = response['ts']
		server = response['server']
		key = response['key']
		global q
		g = Gen()
		for i in range(8):
			t = Answerer(vk)
			t.daemon = True
			t.start()
		print("Start!")
		while True:
			r = http.get('http://{0}?act=a_check&key={1}&ts={2}&wait=25&mode=2'.format(server, key, ts))
			ans = r.content.decode("utf-8")
			if "failed" in ans:
				response = vk.method('messages.getLongPollServer', values)
				ts = response['ts']
				server = response['server']
				key = response['key']
				continue
			answer = json.loads(ans)
			ts = answer['ts']
			for x in range(0, len(answer['updates'])):
				if answer['updates'][x][0] == 4:
					q.put(answer['updates'][x])

if __name__ == '__main__':
	Bot().main()
