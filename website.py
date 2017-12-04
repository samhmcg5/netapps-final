import flask
from pymongo import MongoClient
import os
import socket
#import face_recognition

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
{
    "name": "Bennett White",
    "pin": 123456789,
    "pid": "benwh1te",
    "teams": [
        {
            "teamName": "Netapp Bois",
            "sport": "Indoor Soccer"
        },
        {
            "teamName": "VolleyBallers",
            "sport": "Flag Football"
        }
    ],
    "paid": 1
}
'''

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
#     return flask.redirect('http://localhost:5000/checkin')
#     #check database

@app.route('/handleNewTeamData', methods=['POST'])
def handleNewTeamData():
    teamName = flask.request.form['teamName']
    teamCaptain = flask.request.form['teamCaptain']
    if teamName == '' or teamCaptain == '':
        return 'Error - fill in all data forms'
    sport = flask.request.form['sport']
    if teams.find_one({'teamName': teamName, 'sport': sport}) != None:
        return 'Error - Team Name already exists'
    data = dict()
    data['teamName'] = teamName
    data['teamCaptain'] = teamCaptain
    data['sport'] = sport
    data['schedule'] = dict()
    print(data)
    teams.insert_one(data)
    return flask.redirect('http://localhost:5000/newTeam')
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

    if playerName == '' or pidNumber == '' or email == '' or f.filename == '':
        return "Error - fill in all data forms"

    if '.jpg' not in f.filename or '.jpeg' not in f.filename:
        return 'Error - must upload a file in .jpg or .jpeg format'

    filename = 'face.jpg'
    f.save(os.path.join('./face.jpg'))
    #load = face_recognition.load_image_file('face.jpg')
    #encoding = face_recognition.face_encodings(load)[0]
    os.remove('./face.jpg')
    data = dict()
    data['playerName'] = playerName
    data['pidNumber'] = pidNumber
    data['email'] = email
    data['teams'] = []
    if paid == 'payNow':
        data['paid'] = 'paid'
    elif paid == 'payLater':
        data['paid'] = 'notPaid'
    
    #data['encoding'] = encoding
    users.insert_one(data)

    return flask.redirect('http://localhost:5000/')

@app.route('/handleJoinTeam', methods=['POST'])
def joinTeam():
    pidNumber = flask.request.form['pidNumber']
    teamName = flask.request.form['teamName']

    player = users.find_one({'pidNumber': pidNumber})
    if player == None:
        return 'Error - register first'
    if teamName in player['teams']:
        return 'You have already joined this team'
    player['teams'].append(teamName)

    return flask.redirect('http://localhost:5000/')


if(__name__) == "__main__":
    app.run(host='localhost', debug=True)