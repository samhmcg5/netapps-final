# Send file to the server

import socket
import sys

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

s.connect((host, port))

print( 'Sending Image')
f = open('sam2.jpg','rb')
l = f.read(1024)
while (l):
    # print( 'Sending...')
    s.send(l)
    l = f.read(1024)
f.close()
print( "Done Sending")

s.close()