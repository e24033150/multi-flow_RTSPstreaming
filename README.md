# multi-flow_RTSPstreaming
[Referenced Project]
https://github.com/zogvm/Video-Stream-with-RTSP-and-RTP

[Environment]
Ubuntu 14/16 was tested

[Package Installation]
$ sudo apt-get install python2.7 python-pip python-imaging-tk python-opencv
$ sudo apt-get install python-opencv python-imaging
$ sudo pip install numpy
$ sudo apt-get install python-dev libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev libjpeg8 libjpeg62-dev
$ sudo pip install Pillow

[Usage]
Start server
format : python Server.py [server rtsp port]
ex : python Server.py 8554
Start client
format : python ClientLauncher.py [server ip] [server rtsp port] [client rtp port] [video file] [flow number]
ex : python ClientLauncher.py 172.16.53.2 8554 12345 SampleVideo.mkv 2

[Adjustment(optional)]
*The quality of image
$ vi VideoStream.py
change jpeg_quality
*The speed of playing the video
$ vi ServerWorker.py
change the time in clientInfo['event'].wait(0.015)
