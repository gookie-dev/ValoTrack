from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/history/<region>/<puuid>')
def history(region, puuid):
    return requests.get('https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/' + region + '/' + puuid).json()
