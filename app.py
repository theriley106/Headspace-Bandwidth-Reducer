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
	# This holds information on all sessions
	for i in range(10):
		folder = DIRECTORY + "basics_s{}".format(i+1)
		# This is that static directory that stores all mp3 files
		permInfo = {"Folder": folder, "Description": "Basics Day {}".format(i+1), "Files": []}
		# This is the general structure that's used in the Jinja template
		for val in bandwidthModifier.findAllMp3(folder):
			# This iterates through all mp3 files in the static/basics_s* folder
			fileInfo = {}
			# Dictionary will be filled with information from each file rather than each session
			timeVal = bandwidthModifier.getTime(val)
			# This would convert basics_s1/3.json into 3
			fileInfo["Duration"] = timeVal
			'''
			^^^ Duration is the "Estimated" length for the clip.  I don't really know the best way to say
			 this, but it is the  categorized time on headspace.  ie 3 minutes, 5 minutes, 10 minutes, etc.
			 '''
			fileInfo["FullFile"] = val
			# This is the actual file location
			fileInfo["SessionType"] = folder[::-1].partition("/")[0][::-1]
			# This extracts the session name from the full file name.  ie: basics_s1
			fileInfo["Time"] = timeVal
			# This is the same value as Duration
			fileInfo["PartialFiles"] = []
			'''
			^^^ This is a list of file parts.  This is the entire concept of the program.
			splitting single mp3 files into multiple parts seperated by intervals of complete silence.
			'''
			fileInfo['Elem'] = fileInfo["FullFile"].replace(".mp3", "").replace("/", "")
			# Elem is how each button/audio file is differentiated in HTML
			json_data = json.load(open('{}/{}.json'.format(folder, timeVal)))
			# This is the structure of the mp3 file.  Silence duration, silence start, silence end, etc.
			for countVal, fileName in enumerate(bandwidthModifier.findAllMp3(folder + "/{}/".format(timeVal))):
				'''
				This iterates over all mp3 files that are PARTS of the main mp3 file.
				So the main mp3 file was split into parts, and these are all the individual pieces of that main file.
				The file structure is:
				main file: DIRECTORY/SessionType/Duration.mp3
				partial files: DIRECTORY/SessionType/Duration/X.mp3 - with x being the range of silence intervals.
				'''
				tempInfo = {}
				# Dictionary that is replaced on each loop
				tempInfo["FileName"] = fileName
				# This is the filename of the partial file
				tempInfo["Duration"] = json_data[countVal-1]["Duration"]
				# Index of the JSON file starts at 1
				tempInfo["Start"] = json_data[countVal-1]["Start"]
				# Index of the JSON file starts at 1
				tempInfo["End"] = json_data[countVal-1]["End"]
				# Index of the JSON file starts at 1
				fileInfo["PartialFiles"].append(tempInfo)
				# Appends all of the info to fileInfo['PartialFiles']
			permInfo["Files"].append(fileInfo)
			# Perm info holds information on all files within a session
		database.append(permInfo)
		# Database holds info on all sessions
	return render_template("index.html", DATABASE=database[:MAX_FILES])
	# Max files can be changed, but the HTML template is formatted based on a quantity 7 sessions

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



