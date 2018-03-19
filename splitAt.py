import os
import json
import re

def checkText(text):
    return int(text) if text.isdigit() else text

def sortKey(fileName):
	head, tail = os.path.split(fileName)
	return [ checkText(c) for c in re.split('(\d+)', tail) ]

def findAllJson(directory):
	listOfFiles = []
	for file in os.listdir(directory):
		if file.endswith(".json"):
			listOfFiles.append(os.path.join(directory, file))
	listOfFiles.sort(key=sortKey)
	return listOfFiles

def genNew(jsonFile):
	directory = jsonFile[::-1].partition('/')[2][::-1]
	num = jsonFile.replace(directory, "").replace(".json", "")
	prevTime = 0.0
	os.system("rm -rf {}".format(jsonFile.replace(".json", "")))
	os.system("mkdir {}".format(jsonFile.replace(".json", "")))
	for i, val in enumerate(json.load(open(jsonFile))):
		if float(val["Start"]) < float(prevTime):
			raw_input("continue? " + str(val["Start"]) + " : " + str(prevTime))
		os.system("ffmpeg -i {}/{}.mp3 -c copy -ss {} -to {} {}/{}/{}.mp3".format(directory, num, prevTime, val["Start"], directory, num, i))
		prevTime = val['End']
if __name__ == '__main__':
	genNew("static/Mp3/basics_s1/3.json")
	'''for i in range(10):
		for var in findAllJson('static/Mp3/basics_s{}'.format(i+1)):
			print var'''
