import requests

r = requests.get("http://localhost:9999")
if r.status_code == 200:
    with open('new_image.jpg', 'wb') as f:
        for chunk in r:
            f.write(chunk)