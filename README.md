# Headspace-Bandwidth-Reducer
Proposal to the Headspace App to reduce server costs

### Proposal

The average size of the audio downloaded from the Headspace app is [REPLACE WITH ACTUAL NUMBER].  Based on the fundamental purpose of a guided meditation app, a majority of these audio files contain long durations of complete silence.  Analyzing [ACTUAL NUMBER] audio files, we can see that an average of [ACTUAL PERCENTAGE] of each HS Audio file is complete silence (Defined as X decibals).

By seperating the files at points of extended silence, we can reduce server-side bandwidth usage by [ACTUAL PERCENTAGE].  Using open sources libraries like [SOX OR WHATEVER PROPOSED OS LIBRARY], we can programatically seperate audio files based on silence duration.

I have created a proof of concept application that successfully reduces audio related Bandwidth costs...
