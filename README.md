# RTSP video streaming through multiple flows

[Purpose]
---
Deliver the content of video streaming through multiple flows.

[Referenced Project]
---
https://github.com/zogvm/Video-Stream-with-RTSP-and-RTP</br>

[Operating System]
---
Ubuntu 14 & 16 were tested</br>

[Support]
---
* single/multiple flows (decided by the client)
* video formats : mkv, mp4, webm, ... (depends on OpenCV)
* video with 720p/25fps (as far as it goes)
* RTSP options : SETUP/PLAY/PAUSE/TEARDOWN
* multiple clients

[Package Installation]
---
$ sudo apt-get install python2.7 python-pip python-imaging-tk python-opencv python-imaging </br>
$ sudo pip install numpy Pillow </br>
$ sudo apt-get install python-dev libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev libjpeg8 libjpeg62-dev</br>

[Usage]
---
* **Multiple clients** </br>
  The server serves one client with fixed RTP port(s) in default.
  - If you want to serve multiple clients without fixed RTP port(s), please modify `ServerWorker.py` first </br>
  $ vi ServerWorker </br>
  Comment out the for loop in the process of PLAY request
  - If you want to change the number of clients it can serve, please modify `Server.py` </br>
  $ vi Server.py </br>
  Change the number in listen()
  
* **Start server** </br>
Format : python Server.py [server rtsp port] </br>
$ python Server.py 8554 </br>
* **Start client** </br>
Format : python ClientLauncher.py [server ip] [server rtsp port] [client rtp port] [video file] [flow number] </br>
$ python ClientLauncher.py 172.16.53.2 8554 12345 SampleVideo.mkv 2</br>

[Adjustment (optional)]
---
* **The quality of image**</br>
$ vi VideoStream.py</br>
change jpeg_quality</br>
* **The speed of playing the video**</br>
$ vi ServerWorker.py</br>
change the time in clientInfo['event'].wait()</br>

[Future Works]
---
* **For client** </br>
  - A reordering mechanism for the receiving data </br>
  - A scheduler for playing out the frames instead of the waiting time at server </br>
* **For server** </br>
  - Better compression method
