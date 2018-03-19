import bandwidthModifier as bM

for i in range(10):
	for var in bM.findAllMp3('static/Mp3/basics_s{}'.format(i+1)):
		saveAs = var.replace('.mp3', '.json')
		silenceInfo = bM.getSilenceTimestamps(var)
		for e, var in enumerate(silenceInfo):
			try:
				if var['Start'] > var["End"] or var['End'] > silenceInfo[e+1]['Start']:
					print("error found")
			except:
				if var['Start'] > var["End"]:
					print("error found")
