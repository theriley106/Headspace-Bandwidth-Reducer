from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response, jsonify
import os
from mutagen.mp3 import MP3
import time
import bandwidthModifier
from categorizeFiles import *
import operator
import json
from functools import partial
DIRECTORY = "static/Mp3/"
MAX_FILES = 7
app = Flask(__name__)

@app.route('/')
def index():
	database = []
	# {Descrition: blah, "lengths": {3: {},  5: {}, 10: {} }}
	for i in range(1,11):
		folder = DIRECTORY + "basics_s{}".format(i)
		permInfo = {"Folder": folder, "Description": "Basics Day {}".format(i), "Files": []}
		for val in bandwidthModifier.findAllMp3(folder):
			fileInfo = {}
			timeVal = bandwidthModifier.getTime(val)
			fileInfo["Duration"] = timeVal
			fileInfo["FullFile"] = val
			fileInfo["SessionType"] = folder[::-1].partition("/")[0][::-1]
			print fileInfo["SessionType"]
			fileInfo["Time"] = timeVal
			fileInfo["PartialFiles"] = []
			fileInfo['Elem'] = fileInfo["FullFile"].replace(".mp3", "").replace("/", "")
			print '{}/{}.json'.format(folder, timeVal)
			json_data = json.load(open('{}/{}.json'.format(folder, timeVal)))
			for countVal, fileName in enumerate(bandwidthModifier.findAllMp3(folder + "/{}/".format(timeVal))):
				tempInfo = {}
				tempInfo["FileName"] = fileName
				tempInfo["Duration"] = json_data[countVal-1]["Duration"]
				tempInfo["Start"] = json_data[countVal-1]["Start"]
				tempInfo["End"] = json_data[countVal-1]["End"]
				fileInfo["PartialFiles"].append(tempInfo)
			permInfo["Files"].append(fileInfo)
		database.append(permInfo)
	return render_template("index.html", DATABASE=database[:MAX_FILES])

@app.route('/getLength/<fileName>')
def getFileLength(fileName):
	fileName = str(fileName.replace("-", "/"))
	print fileName
	audio = MP3(fileName)
	info = {}
	info["Length"] = int(audio.info.length * 1000)
	print info
	return jsonify(info)

def getFolderSize(p):
   prepend = partial(os.path.join, p)
   return sum([(os.path.getsize(f) if os.path.isfile(f) else getFolderSize(f)) for f in map(prepend, os.listdir(p))])

@app.route('/getAllSize/<sessionType>/<timeVal>')
def getAllFileSize(sessionType, timeVal):
	info = {}
	oldVal = os.path.getsize("{}{}/{}.mp3".format(DIRECTORY, sessionType, timeVal))
	info['OldValue'] = oldVal
	print('{}{}/{}/'.format(DIRECTORY, sessionType, timeVal))
	newVal = getFolderSize('{}{}/{}/'.format(DIRECTORY, sessionType, timeVal))
	info["NewValue"] = newVal
	return jsonify(info)


@app.route('/getStructure/<folder>/<timePeriod>')
def getStructure(folder, timePeriod):
	# This function grabs the file/JSON indicating file splits
	info = {}
	info['prevInfo'] = json.load(open("{}{}/{}.json".format(DIRECTORY, folder, timePeriod)))
	info['newInfo'] = []
	for i in range(len(info['prevInfo'])):
		audio = MP3("{}{}/{}/{}.mp3".format(DIRECTORY, folder, timePeriod, i))
		info['newInfo'].append(int(audio.info.length * 1000))
	return jsonify(info)

@app.route('/grabFile/<fileName>', methods=["POST"])
def grabFile(fileName):
	# This function grabs the file/JSON indicating file splits
	return "<h1>This Works</h1>"

@app.route('/playAudio/<audioFile>')
def playAudio(audioFile):
	# This function plays the audio
	return "<h1>This Works</h1>"

if __name__ == "__main__":
	app.run()



