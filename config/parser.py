#!/usr/bin/python3

import json
from pprint import pprint

def parse(filename):
  with open(filename) as file:
    data = json.load(file)
    pprint(data)
    return data
