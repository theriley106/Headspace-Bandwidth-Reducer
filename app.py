from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
import os
import time
import bandwidthModifier
import categorizeFiles

app = Flask(__name__)

@app.route('/')
def index():
	database = []
	# {Descrition: blah, "lengths": {3: {},  5: {}, 10: {} }}
	allInfo = bM.findAllMp3(directory)
	for i in range(categorizeFiles("Mp3/")):
		day = i + 1
		tempInfo = {"Description": "Basics Day {}".format(day), "Files": []}
		for val in allInfo:
			if val["Day"] == day
	for val in [3, 5, 10]:
		tempInfo["Files"].append({"Time": val, "Filename": str(val) + "MinuteBasics.mp3", "Type": "New"})
	database.append(tempInfo)
	tempInfo = {"Description": "Basics Day 2", "Files": []}
	for val in [3, 5, 10]:
		tempInfo["Files"].append({"Time": val, "Filename": str(val) + "MinuteBasics.mp3", "Type": "Old"})
	database.append(tempInfo)
	# This is the primary page mimicing the headspace app page
	return render_template("index.html", DATABASE=database)

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



