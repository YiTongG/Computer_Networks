from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/time')
def current_time():
    currTime = datetime.datetime.now()
    return str(currTime)
    #The return type must be a string, dict, tuple, Response instance, or WSGI callable, but it was a datetime

app.run(host='0.0.0.0', port=8080, debug=True)
