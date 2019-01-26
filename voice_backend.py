#!/usr/bin/env python3

import os
import sys
import math
import soundfile as sf
import festival


def main(filename):
	data = sys.stdin.readlines()
	str = ""
	for line in data:
		str += line
	tmp_file = festival.textToWavFile(str)
	try:
		with open(tmp_file, 'rb') as wav_file:
			wav_data, samplerate = sf.read(wav_file)
			sf.write(filename, wav_data, samplerate, format='OGG')
		os.unlink(tmp_file)
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
