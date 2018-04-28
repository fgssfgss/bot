#!/usr/bin/python3
import queue
import threading
import time

from .sqlite import SqliteMTProxy


class Database:
    class InsertThread(threading.Thread):
        def __init__(self, db):
            threading.Thread.__init__(self, name='insert thread')
            self.queue = queue.Queue()
            self.db = db

        def insert(self, text):
            self.queue.put(text)

        def parse_and_gen_query(self, text):
            start_time = time.time()
            query = ''
            text = text.replace("'", "\`")
            words = text.split(' ')
            words.insert(0, '#beg#')
            words.append('#end#')
            words = [' ' if s == '' else s for s in words]
            for x in range(0, len(words) - 2, 1):
                if time.time() - start_time > 10:
                    print("Parse_Text | Too long...")
                    break
                query += "INSERT OR IGNORE INTO lexems (`lexeme1`,`lexeme2`,`lexeme3`) VALUES(\'{0}\', \'{1}\', \'{2}\');\n".format(
                    words[x], words[x + 1], words[x + 2])
                query += "UPDATE lexems SET count = count+1 WHERE lexeme1 = \'{0}\' AND lexeme2 = \'{1}\' AND lexeme3 = \'{2}\';\n".format(
                    words[x], words[x + 1], words[x + 2])
            if len(query) != 0:
                self.db.insert(query)

        def run(self):
            while True:
                text = self.queue.get()
                self.parse_and_gen_query(text)
                self.queue.task_done()

    def __init__(self, dbfile, sqlite_mode):
        self.db = SqliteMTProxy(dbfile, sqlite_mode)
        self.db.start()

        self.inserter = self.InsertThread(self.db)
        self.inserter.start()

    def check_word_existance(self, word):
        token = self.db.execute("SELECT count(*) FROM lexems WHERE lexeme1 = ? OR lexeme2 = ? OR lexeme3 = ?;",(word, word, word))
        res = self.db.get_result(token)
        return int(res[0])

    def insert_text(self, text):
        self.inserter.insert(text)

    def fetch_row_with_words(self, first=None, second=None, third=None):
        if first is None and second is None and third is None:
            token = self.db.execute("SELECT * FROM lexems WHERE lexeme1 = '#beg#' ORDER BY RANDOM() LIMIT 0,1;")
            return self.db.get_result(token)

        elif first is None:
            token = self.db.execute("SELECT * FROM lexems WHERE lexeme2 = ? AND lexeme3 = ? ORDER BY RANDOM() DESC LIMIT 0,10;",(second, third))
            return self.db.get_result(token)

        elif third is None:
            token = self.db.execute("SELECT * FROM lexems WHERE lexeme1 = ? AND lexeme2 = ? ORDER BY RANDOM() DESC LIMIT 0,10;",(first, second))
            return self.db.get_result(token)

        else:
            token = self.db.execute("SELECT * FROM lexems WHERE lexeme1 = ? OR lexeme2 = ? OR lexeme3 = ? ORDER BY RANDOM() LIMIT 0,1;",(first, second, third))
            return self.db.get_result(token)

    def fetch_three_words(self, first=None, second=None, third=None, word=None):
        if word is None:
            row = self.fetch_row_with_words(first, second, third)
            answer = []
            if row is None:
                return answer
            answer.append(row[0])
            answer.append(row[1])
            answer.append(row[2])
            return answer

        else:
            if self.check_word_existance(word) == 0:
                raise LookupError
            row = self.fetch_row_with_words(word, word, word)
            answer = []
            if row is None:
                return answer
            answer.append(row[0])
            answer.append(row[1])
            answer.append(row[2])
            return answer
