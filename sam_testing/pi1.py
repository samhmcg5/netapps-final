# Take photo and send it to pi 2

# STEPS:
# 1. upon flask login, tell camera thread to start.
# 2. camera thread sends user info to pi2.
#       -> pi2 requests an image in return
# 3. respond with a taken image, send via socket
# 4. wait for response ... (take new image, approved, denied)
# 5. exit thread, return to wait state

from threading import Thread
import sys
import cv2
import face_recognition
import socket
from flask import Flask, redirect
# from subprocess import checkoutput

PI2_IP = 'localhost'
PI2_IMAGE_PORT = 9998
PI2_CTL_PORT   = 9997

disp = None
xfer = None
image_socket = None
ctl_socket = None
app = Flask(__name__)

# Manage the camera n shit
class DisplayThread(Thread):
    def __init__(self):
        self.done = False
        self.frame = None
        self.video_capture = cv2.VideoCapture(0)
        Thread.__init__(self)
    def get_frame(self):
        return self.frame
    def run(self):
        while not self.done:
            ret, self.frame = self.video_capture.read()
            if ret:
                cv2.imshow('Video', self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.video_capture.release()
        cv2.destroyAllWindows()
        return

# # handle comms between pi1 and pi2
class transferThread(Thread):
    def __init__(self, video):
        self.video = video
        # self.ctl_s = ctl_s
        # self.img_s = img_s
        self.done = False
        self.im_name = "saved_image.jpg"
        print("Creating thread")
        sys.stdout.flush()
        Thread.__init__(self)

    def send_image(self):
        cv2.imwrite(self.im_name, self.video.get_frame())
        # f = open(self.im_name,'rb')
        # img = f.read(1024)
        # while img:
        #     self.img_s.send(img)
        #     img = f.read(1024)
        # f.close()

    # def recvText(self):
    #     text = ''
    #     data = ''
    #     while data != '!':
    #         data = self.ctl_s.recv(1).decode()
    #         text += data
    #     return text[:-1]

    def run(self):
        # get a frame of the video with video.get_frame()
        print("Starting transfer")
        sys.stdout.flush()
        self.ctl_s.send("username")
        while not self.done:
            # data = self.recvText()
            # print("-->",data)
            # if "image" in data:
            #     send_image()
            # if "good" in data:
            #     self.done = True
            #     self.video.done = True
            continue 
        return "Thread Exiting"


# Flask stuff
@app.route('/')
def hello():
    return redirect("/login", code=302)

@app.route('/login', methods=["GET","POST"])
def home():
    # Enter information, hit 'send' button
    # then redirect to Authenticate image page
    return "HOME"

@app.route('/start')
def start():
    global disp
    global xfer
    global image_socket
    global ctl_socket
    disp = DisplayThread()
    xfer = transferThread(disp)
    disp.start()
    xfer.start()
    return "RUNNING"

@app.route('/stop')
def stop():
    global disp, xfer
    if disp is not None:
        disp.done = True
    if xfer is not None:
        xfer.done = True
    return "STOPPING"

# ctl_socket = socket.socket()
# ctl_socket.connect((PI2_IP, PI2_CTL_PORT))
# print("Control Socket Connected")
# image_socket = socket.socket()
# image_socket.connect((PI2_IP, PI2_IMAGE_PORT))
# print("Image Socket Connected")

app.run(host='localhost', port=9999, debug=True)

