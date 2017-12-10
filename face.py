import face_recognition
import requests
import time

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

# Mock PID value
pid = "benwh1te"

# Send request to known faces server with PID
str1 = "http://192.168.1.128:5000/getInfo?pid=%s" % (pid)
r = requests.get(str1)
json_data = r.json()

#print(json_data)

# Encoding of known face from server
known_image_encoding = json_data['encoding']

# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!
unknown_image = face_recognition.load_image_file("static/camera_image.jpg")
try:
	unknown_image_encoding = face_recognition.face_encodings(unknown_image)[0]
	# Now we can see the two face encodings are of the same person with `compare_faces`!
	results = face_recognition.compare_faces([known_image_encoding], unknown_image_encoding)

	count = 0
	if results[0] == True:
	    print("Match")
	elif count < 10:
	    print("Retry")
	else:
		print("Denied")
except IndexError:
	print("No face in image!")
