import bandwidthModifier as bM
import re

def extractTime(string):
	# Regex to extract time from file
	return re.findall("the-basics_s\d+_(\d+)", string)[0]

def extractDay(string):
	# Regex to extract day from file
	return re.findall("the-basics_s(\d+)_", string)[0]

for val in bM.findAllMp3('Mp3/'):
	print extractDay(val)
