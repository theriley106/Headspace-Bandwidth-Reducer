# Headspace-Bandwidth-Reducer
Proposal to the Headspace App to reduce server costs

### Proposal

The average size of the audio downloaded from the Headspace app is [REPLACE WITH ACTUAL NUMBER].  Based on the fundamental purpose of a guided meditation app, a majority of these audio files contain long durations of complete silence.  Analyzing <b>1607</b> audio files, we can see that an average of <b>43.77%</b> of each HeadSpace Audio file is complete silence (Defined as -50 decibals).

By seperating the files at points of extended silence, we can reduce server-side bandwidth usage by more than 73%.  Based on the tools created in this project, we can programatically seperate audio files based on silence duration.

I have created a proof of concept application that successfully reduces audio related Bandwidth costs...


[![N|Solid](static/AudioExample3.png)](#)
<p align="center"><b>basics_s1/3.mp3 (Initial Length: 270.40 | Trimmed Length: 128.95 | Total Silence: 141.45 Seconds or 52.31%)</b></p>

[![N|Solid](static/AudioExample5.png)](#)
<p align="center"><b>Note the long durations of extended silence in the 3 Minute audio file</b></p>

[![N|Solid](static/AudioExample10.png)](#)
<p align="center"><b>Note the long durations of extended silence in the 3 Minute audio file</b></p>
