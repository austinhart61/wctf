# wctf

+++ Infos +++\
- The raspberry pi's simulate a node in a network with an 'IP' and 'MAC' address. Students are to determine the makeshift packet structure and wirelessy communicate with the nodes depending on the various return codes. \
- To make the challenge harder, the nodes scramble their broadcasting frequency and baud rate. When looking on a SDR it should look like a BFSK pulsing signal. \
- application.py runs on a Raspberry Pi Zero W. Installing some kind of SSH on this is super handy to remotely admin. \
- the HC-12 likes to occasionally hang when scrambling baud rate. I have yet to determine the root cause but it would happen randomly after ~12 hours of continuously running. \
- This is a pretty basic implementation, the idea was conceived, designed, debugged (as best as possible), and rolled out in a span of 3 weeks. \


+++ To run application.py +++\

-i set the IP for the node\
-s set the HC12 SELECT gpio pin\
-c set the channel to broadcast on\
-b set the baud rate of the serial comms\
-r enable the randomizer on this node\
-d set the delay for the randomizer\
\
+++ reset the HC12 +++\
\
runs "AT+DEFAULT" resetting baud and channel\
\
+++ IP's used in this challenge +++\
97.121.215.176\
166.248.98.36\
251.236.64.145\
63.180.94.100\
167.251.78.6\
\

email ajhartshorn@wpi.edu with any questions. 
