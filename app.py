import json
import requests
from flask import Flask, g, render_template, request, session, url_for, redirect

app = Flask(__name__)
app.secret_key = '2965096f5a5b435d77794c2ec258289a63cb8274a2eb714af2336f5bfd443b4f'


@app.before_request
def before_request():
    g.id = None
    if 'id' in session:
        g.id = session['id']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('id', None)

        username = request.form['username']
        tag = request.form['tag']
        region = request.form['region']
        r = requests.get('https://api.henrikdev.xyz/valorant/v1/account/' + username + '/' + tag).json()
        if r['status'] == '200':
            try:
                if requests.get('https://api.henrikdev.xyz/valorant/v1/mmr/' + region + '/' + username + '/' + tag).json()['status'] == '200':
                    session['id'] = region + r['data']['puuid']
                    return redirect(url_for('profile'))
            except:
                pass
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/profile')
def profile():
    if not g.id:
        return redirect(url_for('index'))
    g.region = g.id[:2]
    g.puuid = g.id[2:]
    g.name = requests.get('https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/' + g.region + '/' + g.puuid).json()['data']['name']
    g.current_tier = requests.get('https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/' + g.region + '/' + g.puuid).json()['data']['currenttier']
    g.current_tier_patched = requests.get('https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/' + g.region + '/' + g.puuid).json()['data']['currenttierpatched']
    g.ranking_in_tier = requests.get('https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/' + g.region + '/' + g.puuid).json()['data']['ranking_in_tier']
    return render_template('profile.html')


@app.route('/api/history/<region>/<puuid>')
def history(region, puuid):
    return requests.post('https://api.henrikdev.xyz/valorant/v1/raw', headers={'Content-Type': 'application/json'},
                         data=json.dumps({"type": "matchhistory", "value": puuid, "region": region,
                                          "queries": "?queue=competitive&startIndex=0&endIndex=20"})).json()


@app.route('/api/match/<matchid>')
def match(matchid):
    return requests.get('https://api.henrikdev.xyz/valorant/v2/match/' + matchid).json()
