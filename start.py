#!/usr/bin/python
## This is an example of a simple sound capture script.
##
## The script opens an ALSA pcm for sound capture. Set
## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:

import alsaaudio, time, audioop
from subprocess import call

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
inp.setperiodsize(160)

# General Settings
volume = currentVolume = 70
volumeBuffer = []
bufferSize = 300;
measure = 20

# Input volume specific (Mapping Input to Output)
# This is based on the measure
inputMin = 340 
inputMax = 3000
inputRate = ((inputMax - inputMin) / measure)
inputVolumes = range(inputMin, inputMax, inputRate)
inputVolumes = inputVolumes[::-1]

# Output to vary 20% so the rate is a bit more set
outputVolumes = range(80, 100, 1)
outputVolumes = outputVolumes[::-1]

# Set initial volume
m = alsaaudio.Mixer('Master')
m.setvolume(volume)

call(["notify-send", "Adaptive Volume Started"])
while True:
    # Read data from device
    l,data = inp.read()
    if l:
        # Return the maximum of the absolute value of all samples in a fragment.
        input = audioop.max(data, 2)
        volumeBuffer.append(input)
        if (len(volumeBuffer) >= bufferSize):
            averageVolume = (sum(volumeBuffer)/len(volumeBuffer))
            for i in range(len(inputVolumes)):
                if averageVolume >= int(inputVolumes[i]):
                    volume = int(outputVolumes[i])
                    break

            if volume != currentVolume:
                currentVolume = volume
                m = alsaaudio.Mixer('Master')
                m.setvolume(volume)

            print "IN:" + format(input, '06d') + ", AVG: " + format(averageVolume, '06d') + " OUT:" + format(volume, '03d') + "%"
            volumeBuffer.pop(0)
        else:
            print "BUFFERING: filling (",len(volumeBuffer),"/",bufferSize,") buffer"

    time.sleep(.001)
