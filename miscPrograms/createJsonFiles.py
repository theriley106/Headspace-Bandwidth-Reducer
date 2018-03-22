import bandwidthModifier as bM
import json

for i in range(10):
	for var in bM.findAllMp3('static/Mp3/basics_s{}'.format(i+1)):
		saveAs = var.replace('.mp3', '.json')
		silenceInfo = bM.getSilenceTimestamps(var)
		prevTime = 0.0
		for e, var in enumerate(silenceInfo):
			if float(var["Start"]) < float(prevTime) or float(var['Start']) > float(var["End"]) or abs(float(var['End']) - float(var["Start"])) > 60:
				silenceInfo.remove(var)
			prevTime = var['End']
		with open(saveAs, 'w') as fp:
			json.dump(silenceInfo, fp)
