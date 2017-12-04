from pymongo import MongoClient
import socket

host = ''
port = 9669
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)

client = MongoClient()
db = client.hokieSports
users = db.users
interactions = db.interactions

while 1:
    client, address = s.accept()
    data = client.recv(size)

    data = 905865206
    player = users.find_one({'pidNumber': data})
    if player != None:
        client.send(player['encoding'])
    else:
        client.send('Player not registered')
    client.close()