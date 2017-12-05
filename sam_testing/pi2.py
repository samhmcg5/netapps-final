import socket

PI2_IP = 'localhost'
PI2_IMAGE_PORT = 9998
PI2_CTL_PORT   = 9997


def recv_image(fname, client):
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

def request_image(client):
    client.send("image!".encode())
    return

def recvText(client):
    text = ''
    data = ''
    while data != '!':
        data = client.recv(1).decode()
        text += data
    return text[:-1]

print("Starting")
ctl_sock = socket.socket()
ctl_sock.bind((PI2_IP, PI2_CTL_PORT))
ctl_sock.listen(1)
ctl_client, ctl_addr = ctl_sock.accept() 
print("Control Socket Connected")

img_sock = socket.socket()
img_sock.bind((PI2_IP, PI2_IMAGE_PORT))
img_sock.listen(1)
img_client, img_addr = img_sock.accept() 
print("Image Socket Connected")


data = recvText(ctl_sock)
print("--> received:\t",data)
request_image()
recv_image("new_image.jpg", img_sock)
ctl_sock.send("good!".encode())