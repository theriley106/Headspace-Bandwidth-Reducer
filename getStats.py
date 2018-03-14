import bandwidthModifier as bM
import json
allStats = []
allFiles = len(bM.findAllMp3("/media/christopher/USB20FD/HeadSpace"))
for i, var in enumerate(bM.findAllMp3("/media/christopher/USB20FD/HeadSpace")):
	try:
		audioLength, percentage = bM.getSilencePercentage(var)
		allStats.append({"Length": audioLength, "Percentage": percentage, "Filename": var})
		with open('allStats.json', 'w') as fout:
			json.dump(allStats, fout)
		print("{} - {} - {} / 2093".format(var, percentage, i))
	except Exception as exp:
		print exp
