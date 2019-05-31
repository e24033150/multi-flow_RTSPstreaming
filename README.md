# multi-flow_RTSPstreaming

Referenced Project
---
https://github.com/zogvm/Video-Stream-with-RTSP-and-RTP</br>

Environment
---
Ubuntu 14 & 16 were tested</br>

Package Installation
---
$ sudo apt-get install python2.7 python-pip python-imaging-tk python-opencv python-imaging </br>
$ sudo pip install numpy Pillow </br>
$ sudo apt-get install python-dev libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev libjpeg8 libjpeg62-dev</br>

Usage
---
* Start server </br>
format : python Server.py [server rtsp port] </br>
$ python Server.py 8554 </br>
* Start client </br>
format : python ClientLauncher.py [server ip] [server rtsp port] [client rtp port] [video file] [flow number] </br>
$ python ClientLauncher.py 172.16.53.2 8554 12345 SampleVideo.mkv 2</br>

Adjustment(optional)
---
* The quality of image</br>
$ vi VideoStream.py</br>
change jpeg_quality</br>
* The speed of playing the video</br>
$ vi ServerWorker.py</br>
change the time in clientInfo['event'].wait(0.015)</br>
