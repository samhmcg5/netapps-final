from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('image.jpg')

if __name__ == "__main__":
    app.run(host='localhost', port=9999, debug=True)