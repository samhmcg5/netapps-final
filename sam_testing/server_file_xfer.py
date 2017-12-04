# receive a file from the client, save as new_file.jpg

import socket
import sys
import json

def recvImage(fname, client):
    print( "Receiving...")
    fout = open(fname,'wb')
    l = client.recv(1024)
    while (l):
        sys.stdout.write('.')
        sys.stdout.flush()
        fout.write(l)
        l = client.recv(1024)
    fout.close()
    print("\nDone recv image")
    return fname


def recvText(client):
    text = ''
    data = ''
    while data != '!':
        data = client.recv(1).decode()
        text += data
    return text[:-1]


s = socket.socket()
host = 'localhost'
port = 12344
s.bind((host, port))

s.listen(1)

c, addr = s.accept()
print( 'Got connection from', addr)

recvImage("new_file.jpg", c)

c.close()