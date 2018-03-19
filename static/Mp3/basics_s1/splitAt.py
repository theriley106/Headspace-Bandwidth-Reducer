import os
import json

def genNew(num):

	prevTime = 0.0
	os.system("rm -rf {}".format(num))
	os.system("mkdir {}".format(num))
	for i, val in enumerate(json.load(open("{}.json".format(num)))):
		if float(val["Start"]) < float(prevTime):
			raw_input("continue? " + str(val["Start"]) + " : " + str(prevTime))
		os.system("ffmpeg -i {}.mp3 -c copy -ss {} -to {} {}/{}.mp3".format(num, prevTime, val["Start"], num, i))
		prevTime = val['End']
if __name__ == '__main__':
	genNew(raw_input("Num: "))
