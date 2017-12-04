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

app = Flask(__name__)

# # handle comms between pi1 and pi2
class transferThread(Thread):
    def __init__(self):
        print("Creating thread")
        sys.stdout.flush()
        Thread.__init__(self)

    def run(self):
        print("Starting transfer")
        sys.stdout.flush()
        return "Thread Exiting"


# Flask stuff
@app.route('/')
def hello():
    return redirect("/login", code=302)

@app.route('/login', methods=["GET","POST"])
def home():
    xfer = transferThread()
    xfer.start()
    return "HOME"

app.run(host='localhost', port=9999, debug=True)