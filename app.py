from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/history/<region>/<puuid>')
def history(region, puuid):
    return requests.get('https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/' + region + '/' + puuid).json()


@app.route('/api/match/<matchid>')
def match(matchid):
    return requests.get('https://api.henrikdev.xyz/valorant/v2/match/' + matchid).json()
