from flask import Flask, render_template, jsonify, request, send_from_directory
from flask.ext.socketio import SocketIO, emit

import time
import json
import threading
import random

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = 'uploaded_assets'

socketio = SocketIO(app)

'''
def process(data):
    keyword = False
    for k in keywords:
        if k in data['text'].lower():
            keyword = k
    if not keyword or data['user']['lang'] != 'en':
        return
    tweet = {'name': data['user']['screen_name'], 
            'text': data['text'], 
            'url': 'https://twitter.com/statuses/' + str(data['id']), 
            'time': data['created_at'], 
            'favorites': data['favorite_count'], 
            'retweets': data['retweet_count'], 
            'keyword': keyword}
    print(tweet['time'])
    print('@%s: %s' % (data['user']['screen_name'], data['text'].encode('ascii', 'ignore')))
    #broadcast the tweet to all connected clients
    socketio.emit('new_tweet', tweet)
'''



#Routes----------------------------------------------------

@app.route("/")
def index():
    #return get_tweets()
    return render_template("index.html")

@app.route("/images/<filename>")
def get_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

#------------------------------------------------------------
#Websocket messages------------------------------------------
'''
@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)
'''
@socketio.on('connect')
def test_connect():
    print("CLIENT CONNECTED")
    emit('transmit_entities', {"data": "payload"})

@socketio.on("version_verification")
def print_client_version(message):
    print("client version:" + message["version"])

@socketio.on('disconnect')
def test_disconnect():
    print('CLIENT DISCONNECTED')

@socketio.on("entites_received")
def entities_received():
    print("CLIENT RECEIVED ENTITIES")

#------------------------------------------------------------

if __name__=="__main__":
    socketio.run(app, host="0.0.0.0")