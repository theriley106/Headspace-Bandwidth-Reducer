import bandwidthModifier as bM
import re

def extractTime(string):
	return re.findall("the-basics_s\d+_(\d+)", string)

for val in bM.findAllMp3('Mp3/'):
	print extractTime(val)
