from pymongo import MongoClient
import socket
import time

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
teams = db.teams

while 1:
    client, address = s.accept()
    data = client.recv(size)

    data = '123456789'
    player = users.find_one({'pidNumber': data})
    if player == None:
        client.send('Player not registered')
    teamName = player['teams'][0][0]
    sport = player['teams'][0][1]

    team = teams.find_one({'teamName': teamName})
    nextGame = team['schedule'][0]
    opponent = nextGame['opponent']
    location = nextGame['location']
    tog = nextGame['time'] #time of game

    #placeholder for now
    client.send('abcdefghijklmnopqrstuvwxyz')
    client.close()