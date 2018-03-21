# App.py is the backend for the API & the Web App
from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response, jsonify
# Flask is used for the web app
import os
# OS is used to transfer files and return filesize information
from mutagen.mp3 import MP3
# Mutagen is used to get Mp3 length
import bandwidthModifier
# This is the second main part of the project - the findAllMp3 function is used frequently in the web app
import json
# Json is used to read file structure
from functools import partial
# This is used to get total folder size
DIRECTORY = "static/Mp3/"
# This is directory of Mp3 files/Meditation session audio
MAX_FILES = 7
# number of sessions in the web app, can be changed but the HTML template is formatted based on MAX_FILES=7
app = Flask(__name__)
# Init the flask app

@app.route('/')
def index():
	database = []
	# This holds information on all sessions
	for i in range(7):
		# This needs to be changed if you add additional files
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
	# Returns a specific file length as json
	fileName = str(fileName.replace("-", "/"))
	# "/" can't be in a URL so a javascript function replace all backslashes with dashes
	audio = MP3(fileName)
	# Loads audio into Mutagen
	info = {}
	# This dictionary is converted to json and returned
	info["Length"] = int(audio.info.length * 1000)
	# Holds the audio length into the info dictionary.  Audio length is in Seconds, and we need ms for the startTimer javascript function.
	return jsonify(info)

def getFolderSize(p):
	# This sums up all of the file sizes in a folder.  This is useful for calculating file size differences
	prepend = partial(os.path.join, p)
	# Returns all folder
	return sum([(os.path.getsize(f) if os.path.isfile(f) else getFolderSize(f)) for f in map(prepend, os.listdir(p))])
	# Sums up all file sizes

@app.route('/getAllSize/<sessionType>/<timeVal>')
def getAllFileSize(sessionType, timeVal):
	# Returns file size of all files in a folder as JSON
	info = {}
	# This dictionary is converted to json and returned
	oldVal = os.path.getsize("{}{}/{}.mp3".format(DIRECTORY, sessionType, timeVal))
	# Old value if it were being served in the Headspace app
	info['OldValue'] = oldVal
	# Old Value is the old way of distributing audio
	newVal = getFolderSize('{}{}/{}/'.format(DIRECTORY, sessionType, timeVal))
	# New value is the sum of all partial files - the "New" way of distributing audio
	info["NewValue"] = newVal
	# Holds newVal into the info dict
	return jsonify(info)
	# Returns everything as nicely structured json


@app.route('/getStructure/<folder>/<timePeriod>')
def getStructure(folder, timePeriod):
	# This function grabs the file/JSON indicating file splits
	info = {}
	# This dictionary is converted to json and returned
	info['prevInfo'] = json.load(open("{}{}/{}.json".format(DIRECTORY, folder, timePeriod)))
	# Broken into Prev Info and New Info because audio length was related to file structure
	info['newInfo'] = []
	# New info contains file size information indexed in an identical way to the split vals in prevInfo
	for i in range(len(info['prevInfo'])):
		# Iterates through all items in prevInfo
		audio = MP3("{}{}/{}/{}.mp3".format(DIRECTORY, folder, timePeriod, i))
		# Loads audio element into Mutagen
		info['newInfo'].append(int(audio.info.length * 1000))
		# Holds the audio length into the info dictionary.  Audio length is in Seconds, and we need ms for the startTimer javascript function.
	return jsonify(info)
	# Returns as json

if __name__ == "__main__":
	app.run()



