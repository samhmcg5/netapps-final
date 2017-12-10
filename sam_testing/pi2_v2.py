import socket
import sys

def recv_text(client):
    text = ''
    data = ''
    while data != '!':
        data = client.recv(1).decode()
        text += data
    return text[:-1]

def recv_image(client):
    print( "Receiving...")
    fout = open("image2.jpg",'wb')
    l = client.recv(1024)
    while (l):
        sys.stdout.write('.')
        sys.stdout.flush()
        fout.write(l)
        l = client.recv(1024)
    fout.close()
    print("\nDone recv image")
    return fname

def request_image(client):
    client.send("image!".encode())

def approve(client):
    client.send("approved!".encode())

def deny(client):
    client.send("denied!".encode())

def start_camera(client):
    client.send("start!".encode())

def connect_ctl(port):
    sock = socket.socket()
    sock.bind(('localhost', port))
    sock.listen(1)
    print("Listened")
    client, addr = sock.accept() 
    print("Accepted")
    return client, addr

def connect_img(port):
    sock = socket.socket()
    sock.setblocking(0)
    sock.bind(('localhost', port))
    sock.listen(1)
    print("Listened")
    client, addr = sock.accept() 
    print("Accepted")
    return client, addr

client, addr = connect_ctl(9999)
img_client, img_addr = connect_img(9998)
data = ''
while data != 'done':
    data = input()
    if data == '1':
        request_image(client)
        recv_image(img_client)
    elif data == '2':
        approve(client)
    elif data == '3':
        deny(client)
    elif data == '4':
        start_camera(client)
    elif data == '5':
        client.send('exit!'.encode())    

