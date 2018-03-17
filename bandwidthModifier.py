import os
import commands
import re
from mutagen.mp3 import MP3
import time
import json

#os.rename(val, "static/Mp3/{}/{}.mp3".format(extractType(val), re.findall("pack\Dthe\D\w+_(\d+)m_en", val)[0]))
#^ lol I have no idea

'''
for val in bW.findAllMp3("static/Mp3/basics_s1"):
	if "_" in str(val).partition("s1")[2]:
		os.rename(val, "{}s1/{}".format(val.partition("s1")[0], val.partition("s1")[2].replace("_", "/"))

^ Stop coding at 3am...
'''

def checkText(text):
    return int(text) if text.isdigit() else text

def sortKey(fileName):
	head, tail = os.path.split(fileName)
	return [ checkText(c) for c in re.split('(\d+)', tail) ]

def getTime(fileName):
	return re.findall("\d+\/(\d+)", fileName)[0]

def extractType(fileName):
	return re.findall("pack\Dthe\D(\w+)_\d+m_en", fileName)[0]

def massFindMp3():
	return [val for sublist in [[os.path.join(i[0], j) for j in i[2] if j.endswith('.mp3')] for i in os.walk('./')] for val in sublist]

def renameFile(fileName):
	return "static/Mp3/{}.mp3".format(re.findall("pack\Dthe\D(\w+)_en", fileName)[0])

def findTotalSilence(audioFile):
	totalSilence = 0
	for val in getSilenceTimestamps(audioFile):
		totalSilence += val['Duration']
	return totalSilence

def findAllMp3(directory):
	listOfFiles = []
	for file in os.listdir(directory):
		if file.endswith(".mp3"):
			listOfFiles.append(os.path.join(directory, file))
	listOfFiles.sort(key=sortKey)
	return listOfFiles

def getSilencePercentage(audioFile):
	audio = MP3(audioFile)
	audioLength = audio.info.length
	return audioLength, (findTotalSilence(audioFile) / audioLength) * 100

def getSilenceTimestamps(audioFile, duration=2):
	splitPoints = []
	output, tmp = commands.getstatusoutput("ffmpeg -i {} -af silencedetect=noise=-50dB:d={} -f null -".format(audioFile, duration))
	#output, tmp = commands.getstatusoutput("sox -V3 {} newAudio.mp3 silence -l 1 0.0 -50d 1 1.0 -50d : newfile : restart".format(audioFile))
	for i, var in enumerate(str(tmp).split("\n")):
		if "_end" in str(var):
			try:
				end, duration = re.findall("\d+\.\d+", str(var))
				start = re.findall("\d+\.\d+", str(tmp.split("\n")[i-1]))[0]
				splitPoints.append({"Start": float(start), "End": float(end), "Duration": float(duration)})
			except Exception as exp:
				pass
	return splitPoints

def splitAudio(audioFile):
	try:
		audio = MP3(audioFile)
	except:
		return None
	timeStamps = getSilenceTimestamps(audioFile)
	for i, value in enumerate(timeStamps):
		outputFile = "{}_{}.mp3".format(audioFile.replace(".mp3", "").replace("/static/Mp3/", ""), i)
		#print outputFile
		if i == 0:
			splitBegin = 0
			splitEnd = value["Start"]
		else:
			try:
				startPoint = timeStamps[i+1]["Start"]
				splitBegin = value["End"] # This is the end of the silence...
				splitEnd = startPoint - value["End"] #This is the end of the sound
			except:
				splitBegin = value["End"]
				splitEnd = audio.info.length
		e = commands.getstatusoutput("ffmpeg -ss {} -t {} -i {} {}".format(splitBegin, splitEnd, audioFile, outputFile))
	return timeStamps

if __name__ == '__main__':
	audioFile = "3.mp3"
	jsonInfo = splitAudio(audioFile)
	with open('{}.json'.format(audioFile.partition(".")[0]), 'w') as fp:
		json.dump(jsonInfo, fp)
	for i, val in enumerate(jsonInfo):
		os.system("play {}_{}.mp3".format(audioFile.replace(".mp3", ""), i))
		print("Audio Clip {} Completed - Sleeping for {} Seconds".format(i, val["Duration"]))
		time.sleep(val["Duration"])

#ffmpeg -ss <silence_end - 0.25> -t <next_silence_start - silence_end + 0.25> -i input.mov word-N.mov
# 10 Minute - 8.6MB to 3.5MB - 59.3% Decrease
# 5 Minute - 6.1MB to 1.6MB - 73.77% Decrease
# 3 Minute - 4.4MB to 1.5MB - 65.91% Decrease

