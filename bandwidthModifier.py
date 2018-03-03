import os

def splitAudio(audioFile):
	os.system("sox -V3 {} output.mp3 silence 1 3.0 0.1% 1 0.3 0.1% : newfile : restart".format(audioFile))
