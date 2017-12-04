from pymongo import MongoClient
import time

client = MongoClient()

db = client.hokieSports
teams = db.teams
users = db.users
interactions = db.interactions

teams.delete_many({})
users.delete_many({})
interactions.delete_many({})

gameOne = dict()
gameOne['opponent'] = 'testTeam2'
gameOne['location'] = 'Field 1'
gameOne['time'] = time.strptime('Mon Dec 4 18:30:00 2017')
#time.asctime(time.strptime('Mon Dec 4 18:30:00 2017')) produces the string

teamOne = dict()
teamOne['teamName'] = 'testTeam1'
teamOne['teamCaptain'] = 'captain1'
teamOne['sport'] = 'Soccer'
teamOne['schedule'] = [gameOne]

gameOne = dict()
gameOne['opponent'] = 'testTeam1'
gameOne['location'] = 'Field 1'
gameOne['time'] = time.strptime('Mon Dec 4 18:30:00 2017')

teamTwo = dict()
teamTwo['teamName'] = 'testTeam2'
teamTwo['teamCaptain'] = 'captain2'
teamTwo['sport'] = 'Soccer'
teamTwo['schedule'] = [gameOne]

teams.insert_one(teamOne)
teams.insert_one(teamTwo)

