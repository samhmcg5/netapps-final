import flask
from pymongo import MongoClient
import os

client = MongoClient()
db = client.hokieSports
teams = db.teams
users = db.users

app = flask.Flask(__name__)

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

@app.route('/checkin', methods=['GET'])
def checkIn():
    return flask.render_template('checkIn.html')

@app.route('/newMember')
def newMember():
    teamArr = []
    for team in teams.find():
        teamArr.append(str(team['teamName'] + ' - ' + team['sport']))
    return flask.render_template('newMember.html', teams=teamArr)

@app.route('/newTeam')
def newTeam():
    sports = ['Soccer', 'Volleyball']
    return flask.render_template('newTeam.html', sports=sports)

@app.route('/handleCheckInData', methods=['POST'])
def handleCheckInData():
    #return flask.render_template('checkIn.html')
    print(flask.request.form['pidNumber'])
    return flask.redirect('http://localhost:5000/checkin')
    #check database

@app.route('/handleNewTeamData', methods=['POST'])
def handleNewTeamData():
    teamName = flask.request.form['teamName']
    teamCaptain = flask.request.form['teamCaptain']
    if teamName == '' or teamCaptain == '':
        return 'Error - fill in all data forms'
    sport = flask.request.form['sport']
    data = dict()
    data['teamName'] = teamName
    data['teamCaptain'] = teamCaptain
    data['sport'] = sport
    print(data)
    teams.insert_one(data)
    return flask.redirect('http://localhost:5000/newTeam')
    #level = flask.request.form['level']
    #add to database

@app.route('/handleNewMemberData', methods=['POST'])
def handleNewMemberData():
    playerName = flask.request.form['playerName']
    pidNumber = flask.request.form['pidNumber']
    email = flask.request.form['email']
    teamName = flask.request.form['teamName']
    f = flask.request.files['myPhoto']
    filename = 'test.jpg'
    f.save(os.path.join('./test.jpg'))
    return flask.redirect('http://localhost:5000/')
    #add to database

if(__name__) == "__main__":
    app.run(host='localhost', debug=True)