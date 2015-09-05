# adaptive (Linux Based)
Just a script to use my microphone to automatically adjust my computer's volume

#### The idea
I love my car's adaptive radio. The faster I drive, and the more ambient noise. The higher the volume in order to hear the radio. Now it does increase relatively, and I still dictate the range volume.

#### Use Case
Living next the to train tracks is nice, but makes it hard to hear anything but a passing train. This helps by automatically increasing my volume by +-20% when there is noise outside. 

#### The script
This is a little python script uses a microphone to set your volume based on ambient noise.  

#### Pre-requisite:

```shell
# You will need to install alsa audio
# For ubuntu this is
sudo apt-get install -y python-alsaaudio
```

*NOTE:* You will also need to ensure that you have a microphone, and it will need to be the default device. 

*NOTE:* You can play with the values to for your specific microphone and environment  
