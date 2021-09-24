from flask import Flask, render_template, request, jsonify
import requests, json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/history/<region>/<puuid>')
def history(region, puuid):
    return requests.request("POST", 'https://api.henrikdev.xyz/valorant/v1/raw', headers={'Content-Type': 'application/json'}, data=json.dumps({"type": "matchhistory", "value": puuid, "region": region, "queries": "?queue=competitive&startIndex=0&endIndex=20"})).json()


@app.route('/api/match/<matchid>')
def match(matchid):
    return requests.request("GET", 'https://api.henrikdev.xyz/valorant/v2/match/' + matchid).json()
