from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods=["GET","POST"])
def home():
    if request.method == 'POST':
        session['username'] = request.form['username']
        print("GOT: %s" %session['username'] )
        return redirect(url_for('photo'))
    return '''
        <h1>Login Page</h1>
        <p>Enter your login ID:</p>
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/take_photo', methods=["GET","POST"])
def photo():
    return """
    <p>Taking your photo...</p>
    """


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999, debug=True)