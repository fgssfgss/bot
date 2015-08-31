#!/usr/bin/python3 

class Generator():
  def __init__(self, db):
    self.db = db
    
  def gen_full_rand(self):
    phrase = ''
    last = False
    words = db.fetch_three_words()
    while not last:
      st = st + words[1] + ' '
      if '#end#' in words:
        last = True
      words = db.fetch_three_words(first = words[1], second = words[2])
    return phrase
      
  
  def gen_by_word(self, word_gen):
    left_part = ''
    right_part = ''
    left = False
    right = False
    
    init_words = db.fetch_three_words(word = word_gen)
    
    left_words = init_words
    while not left:
      left = left_words[1] + ' ' + left
      if '#beg#' in left_words:
        left = True
      left_words = db.fetch_three_words(second = words[0], third = words[1])
    
    right_words = init_words
    while not right:
      right = right + right_words[1] + ' '
      if '#end#' in right_words:
        right = True
      right_words = db.fetch_three_words(first = words[1], second = words[2])
    
    return left_part + right_part
