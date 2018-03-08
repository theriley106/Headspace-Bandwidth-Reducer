import os
import commands
import re

def getSilenceTimestamps(audioFile):
	splitPoints = []
	output, tmp = commands.getstatusoutput("ffmpeg -i {} -af silencedetect=noise=-50dB:d=2 -f null -".format(audioFile))
	#output, tmp = commands.getstatusoutput("sox -V3 {} newAudio.mp3 silence -l 1 0.0 -50d 1 1.0 -50d : newfile : restart".format(audioFile))
	for var in str(tmp).split("\n"):
		if "_end" in str(var):
			end, duration = re.findall("\d+\.\d+", str(var))
			splitPoints.append({"Start": float(end) - float(duration), "End": float(end)})
	return splitPoints

def splitAudio(audioFile):
	timeStamps = getSilenceTimestamps(audioFile)
	ffmpeg -ss <silence_end - 0.25> -t <next_silence_start - silence_end + 0.25> -i
if __name__ == '__main__':
	print getSilenceTimestamps("3MinuteBasics.mp3")

#ffmpeg -ss <silence_end - 0.25> -t <next_silence_start - silence_end + 0.25> -i input.mov word-N.mov
