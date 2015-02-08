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

class Gen:
	def __init__(self):
		self.connection = db.connect("database.db")
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
			if time.time() - start_time > 20:
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
			
		if st == '':
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
			if time.time() - start_time > 60*1:
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
			if time.time() - start_time > 60*1:
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

			if st1 + st == '':
				return "YA POEHAL KRISHEY, NIHUYA NE RABOTAET VO MNE"
			
		return st1 + st


def main():

	login, password = 'login', 'password'
	excluded_users = '' # id or link to page 

	try:
		vk = vk_api.VkApi(login, password) # Auth
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

	g = Gen()
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
		lol = ''
		for x in range(0, len(answer['updates'])):

			if answer['updates'][x][0] == 4:

				message_text = answer['updates'][x][6]
				message_id = answer['updates'][x][1]
				message_from = answer['updates'][x][3]
				message_flags = answer['updates'][x][2]

				if message_flags & 2:
					break


				v = {
					'message_ids': message_id
				}
				resp = vk.method('messages.markAsRead', v)

				if re.findall(str(message_from), excluded_users):
					print("Excluded user, sorry...")
					break
				
				command = message_text.split(' ')
				if command[0] == '!q':
						lol = g.gen_by_word(command[1])
				elif command[0] == '!msg':
						message_from = int(re.search('[0-9]+', command[1]).group(0))
						lol = " ".join(command[2:])
						print(message_from)
						print(lol)
				else:
						g.parse_text(message_text)
						lol = g.gen_full_rand()

				if message_flags & 512:
					lol += "\n\r\n\rИ вообще я нихуя не вижу/не слышу, пидорас, зря шлешь, зря стараешься!"

				vw = {
					'user_id': message_from,
					'type': 'typing'
				}
				
				chat_from = 0
				
				if message_from >= 2000000000:
					chat_from = message_from - 2000000000

				resp = vk.method('messages.setActivity', vw)
				
				time.sleep(5)

				resp = vk.method('messages.setActivity', vw)

				time.sleep(5)

				if chat_from > 0:
					va = {
					   'chat_id': chat_from,
					   'message': lol
					}
				else:
					va = {
						'user_id': message_from,
						'message': lol
					}
				resp = vk.method('messages.send', va)

		

if __name__ == '__main__':
	main()
