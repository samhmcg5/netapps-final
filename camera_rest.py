from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap 
import face_recognition
import requests
import time
import os, glob
import sys
from zeroconf import ServiceBrowser, Zeroconf
from pathlib import Path

#########################
### ZEROCONF BROWSING ###
#########################
sam_ip = None
ben_ip = None
sam_port = None
ben_port = None

class MyListener(object): 
	def add_service(self, zeroconf, type, name):
		info = zeroconf.get_service_info(type, name)
		# print (name, info.get_name(), info.server)
		# print(info.get_name())
		global sam_ip, sam_port, ben_ip, ben_port
		if "LoginNode" in info.get_name():
			address = (str(info.address[0]) + '.' +
						str(info.address[1]) + '.' +
						str(info.address[2]) + '.' +
						str(info.address[3]))

			sam_ip = address
			sam_port = info.port
		if "Database" in info.get_name():
			address = (str(info.address[0]) + '.' +
						str(info.address[1]) + '.' +
						str(info.address[2]) + '.' +
						str(info.address[3]))

			ben_ip = address
			ben_port = info.port

zeroconf = Zeroconf() 
listener = MyListener() 
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

def chaseWaterfalls():
	print("Browsing for zeroconf...")
	start_time = time.time()
	prev_time = time.time()
	global sam_ip, sam_port, ben_ip, ben_port
	while sam_ip is None:
		now = time.time()
		if now - start_time > 10:
			sys.exit("\nUnable to find LoginNode pi, exiting")
		if now - prev_time > 0.5:
			sys.stdout.write('.')
			sys.stdout.flush()
			prev_time = now
	print("\nLoginNode using addr=%s, port=%i" % (sam_ip, sam_port))
	while ben_ip is None:
		now = time.time()
		if now - start_time > 10:
			sys.exit("\nUnable to find Database pi, exiting")
		if now - prev_time > 0.5:
			sys.stdout.write('.')
			sys.stdout.flush()
			prev_time = now
	print("\nDatabase using addr=%s, port=%i" % (ben_ip, ben_port))
	zeroconf.close()

# look for the other pi...
chaseWaterfalls()

# Get initial stuck photo
sam_str = "http://%s:%s/photo" % (sam_ip, sam_port)
r = requests.get(sam_str)

# Flask setup
app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def login():
	str1 = "http://%s:%s/getUsers" % (ben_ip, ben_port)
	r = requests.get(str1)
	users = r.json()

	if request.method == 'POST':
		for key in users:
			if key == request.form['email'] and users[key] == request.form['password']:
				session['logged_in'] = True
				session['user'] = request.form['email']
				session['count'] = 0
				# Reset LED to blue
				requests.get("http://%s:%s/blue" % (sam_ip, sam_port))
				return redirect(url_for('home'))
		return render_template('index.html', error='Username not recognized!')		
	return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	matchStr = "Picture Not Taken"
	# Redirect the user to login screen if they have not logged in
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	# Post method options
	if request.method == 'POST':
		# Logout request
		if request.form['action'] == 'logout':
			session['logged_in'] = False
			session['user'] = None
			session['count'] = 0
			# Delete all images in static path
			for p in Path("./static/").glob("*.jpg"):
				p.unlink()
			return redirect(url_for('login'))
		# Take photo request
		elif request.form['action'] == 'photo':

			filename = "static/camera_image" + str(time.time()) + ".jpg"
			
			# Get photo request
			sam_str = "http://%s:%s/photo" % (sam_ip, sam_port)
			r = requests.get(sam_str)

			# Save photo
			if r.status_code == 200:
				with open(filename, 'wb') as f:
					f.write(r.content)

			pid = session.get('user')
			pid = pid.split("@")[0]
			str1 = "http://%s:%s/getInfo?pid=%s" % (ben_ip, ben_port, pid)
			r = requests.get(str1)
			json_data = r.json()

			# Encoding of known face from server
			known_image_encoding = json_data['encoding']

			# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!
			unknown_image = face_recognition.load_image_file(filename)
			try:
				unknown_image_encoding = face_recognition.face_encodings(unknown_image)[0]
				# Iterate through possible faces 
				match = False
				for face in unknown_image_encoding:
					# Now we can see the two face encodings are of the same person with `compare_faces`!
					results = face_recognition.compare_faces([known_image_encoding], unknown_image_encoding)
					for item in results:
						if item: match = True
				if match:
				    matchStr = "Match!"
				    requests.get("http://%s:%s/approve" % (sam_ip, sam_port))
				else:
					session['count'] += 1 
					matchStr = "Retry"
			except IndexError:
				match = False
				matchStr = "No Face in Image!"
				session['count'] += 1

			# Too many attemps
			if(session['count'] >= 3):
				requests.get("http://%s:%s/deny" % (sam_ip, sam_port))
				matchStr = "Denied!"
				session['logged_in'] = False
				session['user'] = None
				session['count'] = 0
				for p in Path("./static/").glob("*.jpg"):
					p.unlink()
				return redirect(url_for('login'))

			if match == True:
				player = json_data['playerName']
				sport = json_data['sport']
				team = json_data['teamName']
				status = json_data['regStatus']
				if status == 1:
					statusName = "Registered and Not Paid"
				elif status == 2:
					statusName = "Registered and Paid"
				nextGame = json_data['nextGame']
				timeStr = time.asctime(time.struct_time(nextGame['time']))
				location = nextGame['location']
				opponent = nextGame['opponent']
				return render_template('home.html', filename=filename, player=player, sport=sport, team=team,
				status=statusName, time=timeStr, location=location, opponent=opponent, match=matchStr)
			else:
				return render_template('home.html', filename=filename, match=matchStr)
	return render_template('home.html',  match=matchStr)

if __name__ == '__main__':
	app.run(host="192.168.1.113")
