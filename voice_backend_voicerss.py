#!/usr/bin/env python3

import sys
import requests

KEY = 'KEY'
ENDPOINT = 'http://api.voicerss.org/?key={0}&с=OGG&hl=ru-ru&f=48khz_16bit_stereo&src={1}'


def main(filename):
    data = sys.stdin.readlines()
    str = ""
    for line in data:
        str += line
    try:
        url = ENDPOINT.format(KEY, str)
        data = requests.get(url, allow_redirects=True)
        if data.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in data.iter_content(chunk_size=1024):
                    f.write(chunk)
    except FileNotFoundError:
        print("ERROR")
        sys.exit(1)
    else:
        print("OK")
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    sys.exit(1)
