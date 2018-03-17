import os
import json
prevTime = 0.0
for i, val in enumerate(json.load(open("3.json"))):
	os.system("ffmpeg -i 3.mp3 -c copy -ss {} -to {} test/{}.mp3".format(prevTime, val["End"], i))
	prevTime = val['End']
