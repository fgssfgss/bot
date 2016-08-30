#!/usr/bin/python3 

class Generator():
  def __init__(self, db):
    self.db = db
    self.max = 5000 # symbols
    
  def gen_full_rand(self):
    phrase = ''
    last = False
    words = self.db.fetch_three_words()
    while not last:
      print(words)
      phrase = phrase + str(words[1]) + ' '
      if '#end#' in words:
        last = True
      words = self.db.fetch_three_words(first = words[1], second = words[2])
    return phrase
      
  
  def gen_by_word(self, word_gen):
    left_part = ''
    right_part = ''
    left = False
    right = False

    try:
      init_words = self.db.fetch_three_words(word = word_gen)
    except LookupError as e:
      return 'Not found!'
      
    
    left_words = init_words
    while not left:
      print(left_words)
      left_part = str(left_words[1]) + ' ' + left_part
      if '#beg#' in left_words:
        left = True
      left_words = self.db.fetch_three_words(second = left_words[0], third = left_words[1])
      if len(left_part) >= (self.max/2): # cyclic out
        left = True
    
    right_words = init_words
    while not right:
      print(right_words)
      right_part = right_part + str(right_words[1]) + ' '
      if '#end#' in right_words:
        right = True
      right_words = self.db.fetch_three_words(first = right_words[1], second = right_words[2])
      if len(right_part) >= (self.max/2): # cyclic out
        right = True
    
    return left_part + right_part
