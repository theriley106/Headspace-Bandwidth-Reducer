from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
import os
import time

app = Flask(__name__)

@app.route('/')
def download_csv():
	return "<h1>This Works</h1>"

if __name__ == "__main__":
	app.run()
