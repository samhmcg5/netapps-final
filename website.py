import flask
from pymongo import MongoClient
import os
import socket
import time
import face_recognition
import json

client = MongoClient()
db = client.hokieSports
teams = db.teams
users = db.users
interactions = db.interactions

app = flask.Flask(__name__)

########## MOCKING UP DATA
# def addGame():
#     for team in teams.find():
#         gameData = dict()
#         gameData['location'] = 'Field 1'
#         team['schedule'] = gameData

'''
log = {
    'action': 'newTeam'
    'info': dataInsertedIntoDatabase
    'timeStamp': time.time()
}
'''

IP = check_output(['hostname', 'I']).decode()
IP = IP.split(' ')[0]

@app.route('/')
def homepage():
    return flask.render_template('main.html', test='test')

# @app.route('/checkin', methods=['GET'])
# def checkIn():
#     return flask.render_template('checkIn.html')

@app.route('/newMember')
def newMember():
    return flask.render_template('newMember.html')

@app.route('/newTeam')
def newTeam():
    sports = ['Soccer', 'Football']
    return flask.render_template('newTeam.html', sports=sports)

@app.route('/joinTeam')
def join():
    teamArr = []
    for team in teams.find():
        teamArr.append(str(team['teamName'] + ' - ' + team['sport']))
    return flask.render_template('joinTeam.html', teams=teamArr)

# @app.route('/handleCheckInData', methods=['POST'])
# def handleCheckInData():
#     #return flask.render_template('checkIn.html')
#     print(flask.request.form['pidNumber'])
#     return flask.redirect('http://192.168.1.128:5000/checkin')
#     #check database

@app.route('/handleNewTeamData', methods=['POST'])
def handleNewTeamData():
    teamName = flask.request.form['teamName']
    teamCaptain = flask.request.form['teamCaptain']
    sport = flask.request.form['sport']
    
    data = dict()
    data['teamName'] = teamName
    data['teamCaptain'] = teamCaptain
    data['sport'] = sport
    data['schedule'] = dict()

    if teamName == '' or teamCaptain == '':
        log = dict()
        log['action'] = 'New Team failed to create'
        log['info'] = data
        log['timeStamp'] = time.time()
        interactions.insert_one(log)
        return 'Error - fill in all data forms'

    if teams.find_one({'teamName': teamName, 'sport': sport}) != None:
        log = dict()
        log['action'] = 'New Team failed to create'
        log['info'] = data
        log['timeStamp'] = time.time()
        interactions.insert_one(log)
        return 'Error - fill in all data forms'
        return 'Error - Team Name already exists'

    teams.insert_one(data)

    log = dict()
    log['action'] = 'New Team created'
    log['info'] = data
    log['timeStamp'] = time.time()
    interactions.insert_one(log)

    return flask.redirect('http://' + IP + ':5000/newTeam')
    #add to database

#change to register
#then set up new page to join a team
@app.route('/handleNewMemberData', methods=['POST'])
def handleNewMemberData():
    playerName = flask.request.form['playerName']
    pidNumber = flask.request.form['pidNumber']
    email = flask.request.form['email']
    paid = flask.request.form['payment']
    f = flask.request.files['myPhoto']

    filename = 'face.jpg'
    f.save(os.path.join('./face.jpg'))
    load = face_recognition.load_image_file('face.jpg')
    encoding = face_recognition.face_encodings(load)[0]
    os.remove('./face.jpg')

    encoding = encoding.tolist()
    print('here')
    data = dict()
    data['playerName'] = playerName
    data['pidNumber'] = pidNumber
    data['email'] = email
    data['teams'] = []
    if paid == 'payNow':
        data['paid'] = 'paid'
    elif paid == 'payLater':
        data['paid'] = 'notPaid'
    data['encoding'] = encoding

    if playerName == '' or pidNumber == '' or email == '' or f.filename == '':
        log = dict()
        log['action'] = 'New member registration failed'
        log['info'] = data
        log['timeStamp'] = time.time()
        interactions.insert_one(log)
        return "Error - fill in all data forms"

    if '.jpg' not in f.filename and '.jpeg' not in f.filename:
        log = dict()
        log['action'] = 'New member registration failed'
        log['info'] = data
        log['timeStamp'] = time.time()
        interactions.insert_one(log)
        return 'Error - must upload a file in .jpg or .jpeg format'

    users.insert_one(data)
    log = dict()
    log['action'] = 'New member registered'
    log['info'] = data
    log['timeStamp'] = time.time()
    interactions.insert_one(log)

    return flask.redirect('http://' + IP + ':5000/')

@app.route('/handleJoinTeam', methods=['POST'])
def joinTeam():
    pidNumber = flask.request.form['pidNumber']
    teamName = flask.request.form['teamName']
    teamTuple = (teamName[0:teamName.index('-')-1], teamName[teamName.index('-')+2:len(teamName)])

    player = users.find_one({'pidNumber': pidNumber})
    #log errors as well
    if player == None:
        return 'Error - register first'
    if teamTuple in player['teams']:
        return 'You have already joined this team'
    users.delete_one(player)
    player['teams'].append(teamTuple)
    users.insert_one(player)
    # find and replace call here
    data = dict()
    data['playerName'] = player['playerName']
    data['team'] = teamName

    log = dict()
    log['action'] = 'Successful team join'
    log['info'] = data
    log['timeStamp'] = time.time()
    interactions.insert_one(log)

    return flask.redirect('http://' + IP + ':5000/')

@app.route('/createLog')
def createFile():
    #maybe transfer the file to caller if added login credentials
    f = open('log.txt', 'w')
    for post in interactions.find():
        s = ''
        s = ('At ' + time.asctime(time.localtime(post['timeStamp'])) + ', action "' + post['action'] + '" was received with data: ' +
        str(post['info']) + '\n' )
        f.write(s)
    f.close()
    return flask.redirect('http://' + IP + ':5000/')

#/getInfo?pid=benwh1te'
@app.route('/getInfo')
def retData():
    retVal = dict()
    pid = flask.request.args.get('pid')
    if pid == None or pid == '':
        return 400
    player = users.find_one({'email': (pid + '@vt.edu')})
    if player == None:
        retVal['regStatus'] = 0

    #assuming that the player has joined a team
    teamName = player['teams'][0][0]
    sport = player['teams'][0][1]
    playerName = player['playerName']
    team = teams.find_one({'teamName': teamName})
    nextGame = team['schedule'][0]
    encoding = player['encoding']

    retVal['encoding'] = encoding
    retVal['playerName'] = playerName
    retVal['sport'] = sport
    retVal['teamName'] = teamName
    retVal['nextGame'] = nextGame

    if player['paid'] == 'paid':
        retVal['regStatus'] = 2
        return json.dumps(retVal)
    else:
        retVal['regStatus'] = 1
        return json.dumps(retVal)

    return json.dumps(retVal)

if(__name__) == "__main__":
    app.run(host=IP, debug=True)
