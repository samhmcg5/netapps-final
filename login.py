from threading import Thread
import sys
from flask import Flask, send_file, redirect
from subprocess import check_output
import RPi.GPIO as GPIO
from zeroconf import Zeroconf, ServiceInfo
import socket   

import pygame
import pygame.camera
from pygame.locals import *

app = Flask(__name__)

IP = check_output(['hostname','-I']).decode()
IP = IP.split(' ')[1] 
PORT = 9999

#########################
###  CONFIGURE GPIO   ###
#########################
R_PIN = 16
G_PIN = 20
B_PIN = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pins = (R_PIN, G_PIN, B_PIN)

GPIO.setup(pins, GPIO.OUT)
GPIO.output(pins, GPIO.LOW) # all LOW

#########################
### ZEROCONF REGISTER ###
#########################
print("[ 01 ] Registering Zeroconf Service to %s:%i" % (IP, PORT))
desc = {'path': '/photo'}
info = ServiceInfo("_http._tcp.local.",
                   "LoginNode._http._tcp.local.",
                   socket.inet_aton(IP), PORT, 0, 0,
                   desc, "ash-2.local.")
zeroconf = Zeroconf()
zeroconf.register_service(info)

#########################
### CAMERAS 'N' SHIIT ###
#########################
class DisplayThread(Thread):
    def __init__(self):
        print("[ 02 ] Intializing the camera module")
        pygame.init()
        pygame.camera.init()
        self.cam = pygame.camera.Camera("/dev/video0",(640,480))
        print("[ 03 ] Starting camera")
        self.cam.start()
        self.frame = self.cam.get_image()
        pygame.image.save(self.frame, "image.jpg")
        Thread.__init__(self)
        print("[ 04 ] Done intializing camera")    
    def get_frame(self):
        return self.frame
    def run(self):
        while True:
            self.frame = self.cam.get_image()

# Create an instance of the camera interface
video = DisplayThread()

#########################
### HELPER FUNCTIONS  ###
#########################
def set_green():
    GPIO.output(pins, (0,1,0))

def set_yellow():
    GPIO.output(pins, (0,1,1))

def set_red():
    GPIO.output(pins, (1,0,0))

#########################
###     WEB API       ###
#########################
@app.route('/')
def begin():
    return redirect('http://%s:%i/photo' % (IP,PORT))

@app.route('/photo')
def send_photo():
    # Set GPIO to yellow
    set_yellow()
    global video
    if not video.isAlive():
        video.start()
    frame = video.get_frame()
    pygame.image.save(frame, "image.jpg")
    return send_file('image.jpg')

@app.route('/deny')
def deny_access():
    # Set GPIO to Red
    set_red()
    return "Access Denied"

@app.route('/approve')
def approve_access():
    # Set GPIO to Green
    set_green()
    return "Approved"


# Start the Web App
app.run(host=IP, port=PORT, debug=False)
# Wait for the camera thread to complete
video.join()


