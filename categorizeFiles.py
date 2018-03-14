import bandwidthModifier as bM
import re

def extractTime(string):
	# Regex to extract time from file
	return int(re.findall("the-basics_s\d+_(\d+)", string)[0])

def extractDay(string):
	# Regex to extract day from file
	return int(re.findall("the-basics_s(\d+)_", string)[0])

def extractTotalDay(directory):
	days = []
	for var in bM.findAllMp3(directory):
		days.append(int(extractDay(var)))
	days.sort()
	return list(days)[::-1][0]

def extractAll(directory):
	info = []
	for val in bM.findAllMp3(directory):
		info.append({"FileName": val, "Day": extractTotalDay(val), "Time": extractTime(val)})
	return info
