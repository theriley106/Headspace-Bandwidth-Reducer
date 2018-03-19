import bandwidthModifier as bM

for i in range(10):
	for var in bM.findAllMp3('static/Mp3/basics_s{}'.format(i+1)):
		print var
