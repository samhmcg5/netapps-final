from threading import Thread
import sys
import cv2
import socket
import time
from collections import deque
import sys

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


############################
### DATA TRANSFER TO PI2 ###
############################
# class RecieveThread(Thread):
#     def __init__(self, sock, queue):
#         self.sock = sock
#         self.queue = queue
#         Thread.__init__(self)
#     def run(self):
#         while True:
#             text = ''
#             data = ''
#             while data is not '!':
#                 data = self.sock.recv(1).decode()
#                 text += data
#             text = text[:-1]
#             self.queue.append(text)

class TransferThread(Thread):
    def __init__(self, ip, port_c, port_img):
        self.ip = ip
        self.port_c = port_c
        self.port_img = port_img
        self.ctl_sock = socket.socket()
        self.img_sock = socket.socket()
        self.exit = False
        # self.queue = deque()
        Thread.__init__(self)
        self.video = DisplayThread()

    def connect_sockets(self):
        print("Connecting to server")
        self.ctl_sock.connect((self.ip, self.port_c))
        self.img_sock.connect((self.ip, self.port_img))

    def send_image(self):
        print("sending image")
        frame = self.video.get_frame()
        cv2.imwrite("image.jpg", frame)
        f = open("image.jpg",'rb')
        img = f.read(1024)
        while img:
            self.img_sock.send(img)
            img = f.read(1024)
        f.close()

    def close_camera(self):
        print("Closing Camera")
        self.video.end_capture()

    def start_camera(self):
        print("Starting Camera")
        self.video.begin_capture()

    def recv_control(self):
        text = ''
        data = ''
        while data is not '!':
            data = self.ctl_sock.recv(1).decode()
            text += data
        return text[:-1]

    def run(self):
        self.video.start()
        print("Starting TransferThread")
        while not self.exit:
            text = self.recv_control()
            print(text)
            if text == 'image':
                self.send_image()
            elif text == 'approved':
                self.close_camera()
            elif text == 'denied':
                self.close_camera()
            elif text == 'start':
                self.start_camera()
            elif text == 'exit':
                break


#########################
###        MAIN       ###
#########################
if __name__ == '__main__':
    xfer = TransferThread('localhost', 9999, 9998)
    xfer.connect_sockets()
    xfer.start()
