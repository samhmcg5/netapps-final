from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap 
import face_recognition
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
			session['user'] = 'eric'
			return redirect(url_for('home'))		
	return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	filename = "/static/" + session.get('user') + ".jpg"
	filename = "/static/camera_image.jpg"
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	if request.method == 'POST':
		if request.form['action'] == 'logout':
			session['logged_in'] = False
			session['user'] = None
			return redirect(url_for('login'))
		elif request.form['action'] == 'photo':
			# Send initialize request
			r = requests.get("http://192.168.1.105:9999/")
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
			r = requests.get("http://192.168.1.105:9999/stop")

			return render_template('home.html', filename=filename)
	return render_template('home.html')

if __name__ == '__main__':
	app.run(host="192.168.1.125")
