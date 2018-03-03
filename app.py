from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
import os
import time
import bandwidthModifier

app = Flask(__name__)

@app.route('/')
def index():
	# This is the primary page mimicing the headspace app page
	return "<h1>This Works</h1>"

@app.route('/grabFile/<fileName>', method="POST")
def grabFile(fileName):
	# This function grabs the file/JSON indicating file splits
	return "<h1>This Works</h1>"

@app.route('/playAudio/<audioFile>')
def playAudio(audioFile):
	# This function plays the audio
	return "<h1>This Works</h1>"

if __name__ == "__main__":
	app.run()
