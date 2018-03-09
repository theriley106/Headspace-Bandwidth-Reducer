import os
import commands
import re
from mutagen.mp3 import MP3
import time

def getSilenceTimestamps(audioFile, duration=2):
	splitPoints = []
	output, tmp = commands.getstatusoutput("ffmpeg -i {} -af silencedetect=noise=-50dB:d={} -f null -".format(audioFile, duration))
	#output, tmp = commands.getstatusoutput("sox -V3 {} newAudio.mp3 silence -l 1 0.0 -50d 1 1.0 -50d : newfile : restart".format(audioFile))
	for i, var in enumerate(str(tmp).split("\n")):
		if "_end" in str(var):
			end, duration = re.findall("\d+\.\d+", str(var))
			start = re.findall("\d+\.\d+", str(tmp.split("\n")[i-1]))[0]
			splitPoints.append({"Start": float(start), "End": float(end), "Duration": float(duration)})
	return splitPoints

def splitAudio(audioFile):
	audio = MP3(audioFile)
	timeStamps = getSilenceTimestamps(audioFile)
	for i, value in enumerate(timeStamps):
		outputFile = "newFile{}.mp3".format(i)
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
		commands.getstatusoutput("ffmpeg -ss {} -t {} -i {} {}".format(splitBegin, splitEnd, audioFile, outputFile))
	return timeStamps
if __name__ == '__main__':
	for i, val in enumerate(splitAudio("3MinuteBasics.mp3")):
		os.system("play newFile{}.mp3".format(i))
		print("Audio Clip {} Completed - Sleeping for {} Seconds".format(i, val["Duration"]))
		time.sleep(val["Duration"])

#ffmpeg -ss <silence_end - 0.25> -t <next_silence_start - silence_end + 0.25> -i input.mov word-N.mov
