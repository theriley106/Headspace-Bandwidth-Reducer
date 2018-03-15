from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
import os
import time
import bandwidthModifier
from categorizeFiles import *
import operator
DIRECTORY = "static/Mp3/"
MAX_FILES = 7
app = Flask(__name__)

@app.route('/')
def index():
	database = []
	# {Descrition: blah, "lengths": {3: {},  5: {}, 10: {} }}
	allInfo = extractAll(DIRECTORY)
	for i in range(1,11):
		folder = DIRECTORY + "basics_s{}".format(i)
		tempInfo = {"Folder": folder, "Description": "Basics Day {}".format(i), "Files": []}
		for val in allInfo:
			if val["Day"] == day:
				time = val["Time"]
				fileName = val["FileName"]
				info = bandwidthModifier.splitAudio(fileName)
				elemName = fileName.replace(".mp3", "").replace("/", "")
				if info != None:
					print("added")
					tempInfo["Files"].append({"Info": info, "Elem": elemName, "Time": time, "Filename": fileName})
		tempInfo["Files"].sort(key=operator.itemgetter('Time'))
		database.append(tempInfo)
	return render_template("index.html", DATABASE=database[:MAX_FILES])

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



