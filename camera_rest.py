from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap 
#import face_recognition
import requests
import time
import os

# Flask setup
app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['email'] == 'esimp12@vt.edu' and request.form['password'] == 'admin':
			session['logged_in'] = True
			session['user'] = request.form['email']
			return redirect(url_for('home'))		
	return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	filename = "/static/camera_image.jpg"
	filename = "/static/eric.jpg"
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	if request.method == 'POST':
		if request.form['action'] == 'logout':
			session['logged_in'] = False
			session['user'] = None
			return redirect(url_for('login'))
		elif request.form['action'] == 'photo':
			# Send initialize request
			"""r = requests.get("http://192.168.1.105:9999/")
			time.sleep(1)
			# Start camera request
			r = requests.get("http://192.168.1.105:9999/start")
			time.sleep(1)

			# Get photo request
			r = requests.get("http://192.168.1.105:9999/photo")
			
			if r.status_code == 200:
				with open('static/camera_image.jpg', 'wb') as f:
					for chunk in r:
						f.write(chunk)
			time.sleep(1)

			# Stop the camera request
			r = requests.get("http://192.168.1.105:9999/stop")"""

			pid = session.get('user')
			pid = pid.split("@")[0]
			pid = "benwh1te"
			str1 = "http://192.168.1.130:5000/getInfo?pid=%s" % (pid)
			r = requests.get(str1)
			json_data = r.json()

			print(json_data)

			status = json_data['regStatus']
			statusName = None
			player = None
			sport = None
			team = None
			location = None 
			opponent = None
			timeStr = None
			if status != 0:
				player = json_data['playerName']
				sport = json_data['sport']
				team = json_data['teamName']
				if status == 1:
					statusName = "Registered and Not Paid"
				elif status == 2:
					statusName = "Registered and Paid"
				nextGame = json_data['nextGame']
				timeStr = time.asctime(time.struct_time(nextGame['time']))
				location = nextGame['location']
				opponent = nextGame['opponent']

				# encoding stuff here

			else:
				statusName = "Not Registered"

			if player is not None and sport is not None and team is not None and location is not None and opponent is not None and timeStr is not None:
				return render_template('home.html', filename=filename, player=player, sport=sport, team=team,
				status=statusName, time=timeStr, location=location, opponent=opponent)
			else: 
				return render_template('home.html', status=statusName)

	return render_template('home.html')

if __name__ == '__main__':
	app.run()
