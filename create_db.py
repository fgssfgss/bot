import sqlite3
import time
import vk_api
import re

conn = sqlite3.connect("new_bugurt.db")
db = conn.cursor()
db.execute("CREATE TABLE lexems (`lexeme1` TEXT, `lexeme2` TEXT, `lexeme3` TEXT, `count` INT NOT NULL DEFAULT '0', UNIQUE (`lexeme1`, `lexeme2`, `lexeme3`));")

def parse_text(text):
    start_time = time.time()
    query = ''
    text = text.replace("'", "\`")
    words = text.split(' ')
    words.insert(0, '#beg#')
    words.append('#end#')
    for x in range(0, len(words) - 2, 1):
        if time.time() - start_time > 10:
            print("Parse_Text | Too long...")
            break
        query += "INSERT OR IGNORE INTO lexems (`lexeme1`,`lexeme2`,`lexeme3`) VALUES(\'{0}\', \'{1}\', \'{2}\');\n".format(words[x], words[x + 1], words[x + 2])
        query += "UPDATE lexems SET count = count+1 WHERE lexeme1 = \'{0}\' AND lexeme2 = \'{1}\' AND lexeme3 = \'{2}\';\n".format(words[x], words[x + 1], words[x + 2])
    if len(query) != 0:
        print(query)
        db.executescript(query)

# from 730 post need resume and comment line above
vk = vk_api.VkApi(app_id = 5839853, client_secret = "NvPKHWzkXiFRjcyKkKV8", token = "blablabla")
vk.authorization()
tools = vk_api.VkTools(vk)
wall = tools.get_all('wall.get', 100, {'domain': "bugurt_thread"})
print('Posts count:', wall['count'])
print(wall["items"][0]['text'])
for i in range(0, int(wall['count'])):
    print(i)
    parse_text(wall['items'][i]['text'])

