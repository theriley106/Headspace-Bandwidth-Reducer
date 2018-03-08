import os

def splitAudio(audioFile):
	os.system("sox -V3 {} newAudio.mp3 silence 1 0.5 2% 1 2.0 2% : newfile : restart".format(audioFile))

if __name__ == '__main__':
	splitAudio(raw_input("Audio File: "))
