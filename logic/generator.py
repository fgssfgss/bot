#!/usr/bin/python3


class Generator:
    def __init__(self, db):
        self.db = db
        self.max = 200

    def insert_to_db(self, text):
        self.db.insert_text(text)

    def gen_full_rand(self):
        phrase = ''
        last = False
        words = self.db.fetch_three_words()

        if len(words) < 3:
            return "Nothing to say!"

        while not last:
            #print(words)
            phrase = phrase + str(words[1]) + ' '
            if '#end#' in words:
                last = True
            words = self.db.fetch_three_words(first=words[1], second=words[2])
        return phrase

    def gen_by_word(self, word_gen, substr=False):
        left_part = []
        right_part = []
        left = False
        right = False

        try:
            init_words = self.db.fetch_three_words(word=word_gen, substr=substr)
        except LookupError as e:
            return 'Not found!'

        if init_words[0] == '#beg#' and init_words[2] == '#end#':
            return init_words[1]
        if init_words[0] == '#beg#':
            left_part.append(init_words[1])
            left = True
        elif init_words[2] == '#end#':
            right_part.append(init_words[1])
            right = True
        else:
            left_part.append(init_words[1])

        left_words = init_words
        while not left:
            left_words = self.db.fetch_three_words(second=left_words[0], third=left_words[1])
            #print(left_words)
            left_part.append(left_words[1])
            if left_words[0] == '#beg#':
                left = True
                break
            if len(left_part) >= self.max:
                left = True

        right_words = init_words
        while not right:
            right_words = self.db.fetch_three_words(first=right_words[1], second=right_words[2])
            #print(right_words)
            right_part.append(right_words[1])
            if right_words[2] == '#end#':
                right = True
                break
            if len(right_part) >= self.max:
                right = True

        left_part.reverse()
        result = left_part + right_part
        return " ".join(result)
