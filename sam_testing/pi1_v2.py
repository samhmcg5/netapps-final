from threading import Thread
import sys
import cv2
import time
import sys
from flask import Flask, send_file

app = Flask(__name__)


#########################
### CAMERAS 'N' SHIIT ###
#########################
class DisplayThread(Thread):
    def __init__(self):
        self.done = True
        self.exit = False
        self.frame = None
        Thread.__init__(self)
    
    def get_frame(self):
        return self.frame
    def begin_capture(self):
        self.done = False;
    def end_capture(self):
        self.done = True;
    def run(self):
        while not self.exit:
            if not self.done:
                self.video_capture = cv2.VideoCapture(0)
                while not self.done:
                    ret, self.frame = self.video_capture.read()
                    if ret:
                        cv2.imshow('Video', self.frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                self.video_capture.release()
                cv2.destroyAllWindows()


video = DisplayThread()

@app.route('/')
def begin():
    global video
    if not video.isAlive():
        video.start()
    return "initialized"

@app.route('/photo')
def send_photo():
    global video
    frame = video.get_frame()
    cv2.imwrite("image.jpg", frame)
    return send_file('image.jpg')

@app.route('/start')
def start_cam():
    global video
    video.begin_capture()
    return "Starting"

@app.route('/stop')
def stop_cam():
    global video
    video.end_capture()
    return "Stopping"


# if __name__ == '__main__':
# video.start()
app.run(host='192.168.1.105', port=9999, debug=False)
video.join()


