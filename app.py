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
songs = [{"lat": "37.8716", "lng": "-122.2727", "songName": "Billie Jean", "artistName": "Michael Jackson", "youtubeLink": "https://www.youtube.com/watch?v=Zi_XLOBDo_Y"},
        {"lat": "37.3382", "lng": "-121.8863", "songName": "Big Pimpin'", "artistName": "Jay Z", "youtubeLink": "https://www.youtube.com/watch?v=Cgoqrgc_0cM"},
        {"lat": "36.9741", "lng": "-122.0308", "songName": "Everybody Wants to Rule the World", "artistName": "Tears for Fears", "youtubeLink": "https://www.youtube.com/watch?v=ST86JM1RPl0"},
        {"lat": "36.0083", "lng": "-119.9618", "songName": "American Ride", "artistName": "Toby Keith", "youtubeLink": "https://www.youtube.com/watch?v=zNDcAWNscg8"},
        {"lat": "34.4208", "lng": "-119.6982", "songName": "Headlines", "artistName": "Drake", "youtubeLink": "https://www.youtube.com/watch?v=cimoNqiulUE"},
        {"lat": "34.0522", "lng": "-118.2437", "songName": "Jumpman", "artistName": "Drake", "youtubeLink": "https://www.youtube.com/watch?v=NiM5ARaexPE"}]


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
    emit('transmit_songs', {"data": songs})

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