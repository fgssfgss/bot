#!/usr/bin/python3

from .sqlite import SqliteMTProxy


class Database:
    def __init__(self, dbfile, sqlite_mode):
        self.db = SqliteMTProxy(dbfile, sqlite_mode)
        self.db.start()

    def check_word_existance(self, word):
        token = self.db.execute("SELECT count(*) FROM lexems WHERE lexeme1 = ? OR lexeme2 = ? OR lexeme3 = ?;",(word, word, word))
        res = self.db.get_result(token)
        return int(res[0])

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
