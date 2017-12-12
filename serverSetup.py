from pymongo import MongoClient
import time
import face_recognition

client = MongoClient()

db = client.hokieSports
teams = db.teams
users = db.users
interactions = db.interactions

# empties out the database
teams.delete_many({})
users.delete_many({})
interactions.delete_many({})

gameOne = dict()
gameOne['opponent'] = 'testTeam2'
gameOne['location'] = 'Field 1'
gameOne['time'] = time.strptime('Mon Dec 4 18:30:00 2017')
#time.asctime(time.strptime('Mon Dec 4 18:30:00 2017')) produces the string


## HOME OR AWAY

teamOne = dict()
teamOne['teamName'] = 'testTeam1'
teamOne['teamCaptain'] = 'captain1'
teamOne['sport'] = 'Soccer'
teamOne['schedule'] = [gameOne]

gameOne = dict()
gameOne['opponent'] = 'testTeam1'
gameOne['location'] = 'Field 1'
gameOne['time'] = time.strptime('Mon Dec 18 18:30:00 2017')

teamTwo = dict()
teamTwo['teamName'] = 'testTeam2'
teamTwo['teamCaptain'] = 'captain2'
teamTwo['sport'] = 'Soccer'
teamTwo['schedule'] = [gameOne]

logOne = dict()
logOne['action'] = 'New Team created'
logOne['info'] = teamOne
logOne['timeStamp'] = time.time()

logTwo = dict()
logTwo['action'] = 'New Team created'
logTwo['info'] = teamTwo
logTwo['timeStamp'] = time.time()

teams.insert_one(teamOne)
teams.insert_one(teamTwo)
interactions.insert_one(logOne)
interactions.insert_one(logTwo)

squid = dict()
squid['playerName'] = 'Sam Mcghee'
squid['pidNumber'] = 111111111
squid['email'] = 'shmv@vt.edu'
squid['teams'] = [('testTeam1', 'Soccer')]
squid['paid'] = 'notPaid'
squid['password'] = 'password'
loaded = face_recognition.load_image_file('./test_faces/images/sam1.jpg')
squid['encoding'] = face_recognition.face_encodings(loaded)[0].tolist()
users.insert_one(squid)

eric = dict()
eric['playerName'] = 'Eric Simpson'
eric['pidNumber'] = 222222222
eric['email'] = 'esimp12@vt.edu'
eric['teams'] = [('testTeam1', 'Soccer')]
eric['paid'] = 'paid'
eric['password'] = 'password'
loaded = face_recognition.load_image_file('./test_faces/images/eric.jpg')
eric['encoding'] = face_recognition.face_encodings(loaded)[0].tolist()
users.insert_one(eric)

alex = dict()
alex['playerName'] = 'Alex Devero'
alex['pidNumber'] = 333333333
alex['email'] = 'alexd95@vt.edu'
alex['teams'] = [('testTeam2', 'Soccer')]
alex['paid'] = 'paid'
alex['password'] = 'password'
loaded = face_recognition.load_image_file('./test_faces/images/alex.jpg')
alex['encoding'] = face_recognition.face_encodings(loaded)[0].tolist()
users.insert_one(alex)

