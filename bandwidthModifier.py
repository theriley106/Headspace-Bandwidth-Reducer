import os
import commands
import re
import eyed3

def getSilenceTimestamps(audioFile):
	splitPoints = []
	output, tmp = commands.getstatusoutput("ffmpeg -i {} -af silencedetect=noise=-50dB:d=2 -f null -".format(audioFile))
	#output, tmp = commands.getstatusoutput("sox -V3 {} newAudio.mp3 silence -l 1 0.0 -50d 1 1.0 -50d : newfile : restart".format(audioFile))
	for i, var in enumerate(str(tmp).split("\n")):
		if "_end" in str(var):
			end, duration = re.findall("\d+\.\d+", str(var))
			start = re.findall("\d+\.\d+", str(tmp.split("\n")[i-1]))[0]
			splitPoints.append({"Start": float(start), "End": float(end), "Duration": float(duration)})
	return splitPoints

def splitAudio(audioFile):
	timeStamps = getSilenceTimestamps(audioFile)
	for i, value in enumerate(timeStamps):
		outputFile = "newFile{}.mp3".format(i)
		if i == 0:
			splitBegin = 0
			splitEnd = value["Start"]
		else if i == len(timeStamps):
			startPoints = timeStamps[i+1]["Start"]
			splitBegin = value["End"] # This is the end of the silence...
			splitEnd = startPoint - value["End"] #This is the end of the sound
		else:

		os.system("ffmpeg -ss {} -t {} -i {} {}".format(splitBegin, splitEnd, audioFile, outputFile))
if __name__ == '__main__':
	print splitAudio("3MinuteBasics.mp3")

#ffmpeg -ss <silence_end - 0.25> -t <next_silence_start - silence_end + 0.25> -i input.mov word-N.mov
